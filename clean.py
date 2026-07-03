"""raw.csv → data/clean.parquet. Deterministic, idempotent. Prints per-fix counts as JSON."""
import json
import duckdb

FIXES_SQL = """
create table cleaned as
with base as (
  select * from read_csv_auto('data/raw.csv', all_varchar=true)
),
dedup as (
  select * from (
    select *, row_number() over (partition by unique_key order by created_date) rn from base
  ) where rn = 1
)
select
  unique_key,
  try_cast(created_date as timestamp)                       as created_date,
  case when try_cast(closed_date as timestamp) >= try_cast(created_date as timestamp)
       then try_cast(closed_date as timestamp) end          as closed_date,
  upper(trim(agency))                                       as agency,
  trim(regexp_replace(complaint_type, '\\s+', ' ', 'g'))    as complaint_type,
  trim(coalesce(descriptor, ''))                            as descriptor,
  case when upper(trim(coalesce(borough,''))) in
            ('BROOKLYN','QUEENS','MANHATTAN','BRONX','STATEN ISLAND')
       then upper(trim(borough)) else 'UNSPECIFIED' end     as borough,
  case when regexp_matches(trim(coalesce(incident_zip,'')), '^\\d{5}$')
       then trim(incident_zip) end                          as incident_zip,
  trim(coalesce(city, ''))                                  as city,
  upper(trim(coalesce(status,'')))                          as status,
  case when try_cast(latitude as double) between 40.4 and 41.0
        and try_cast(longitude as double) between -74.3 and -73.6
       then try_cast(latitude as double) end                as latitude,
  case when try_cast(latitude as double) between 40.4 and 41.0
        and try_cast(longitude as double) between -74.3 and -73.6
       then try_cast(longitude as double) end               as longitude
from dedup
"""

def main() -> None:
    con = duckdb.connect()
    raw = con.execute("select count(*) from read_csv_auto('data/raw.csv', all_varchar=true)").fetchone()[0]
    con.execute(FIXES_SQL)
    out = con.execute("select count(*) from cleaned").fetchone()[0]
    fixes = {
        "rows_in": raw, "rows_out": out, "duplicates_removed": raw - out,
        "boroughs_normalized": con.execute(
            "select count(*) from read_csv_auto('data/raw.csv', all_varchar=true) t "
            "where upper(trim(coalesce(t.borough,''))) not in "
            "('BROOKLYN','QUEENS','MANHATTAN','BRONX','STATEN ISLAND','UNSPECIFIED')").fetchone()[0],
        "invalid_zips_nulled": con.execute(
            "select count(*) from read_csv_auto('data/raw.csv', all_varchar=true) t "
            "where coalesce(t.incident_zip,'') <> '' and not regexp_matches(trim(t.incident_zip), '^\\d{5}$')").fetchone()[0],
        "out_of_bbox_coords_nulled": con.execute(
            "select count(*) from read_csv_auto('data/raw.csv', all_varchar=true) t "
            "where coalesce(cast(t.latitude as varchar),'') <> '' and not "
            "(try_cast(t.latitude as double) between 40.4 and 41.0 and try_cast(t.longitude as double) between -74.3 and -73.6)").fetchone()[0],
    }
    con.execute("copy cleaned to 'data/clean.parquet' (format parquet)")
    print(json.dumps(fixes))

if __name__ == "__main__":
    main()

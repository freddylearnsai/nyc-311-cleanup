"""Validation rules. Each: (name, SQL predicate over table t) — TRUE means the row PASSES."""
RULES = [
    ("created_date parses",   "try_cast(t.created_date as timestamp) is not null"),
    ("complaint_type present", "t.complaint_type is not null and length(trim(t.complaint_type)) > 0"),
    ("borough is known",      "upper(trim(coalesce(t.borough,''))) in "
                              "('BROOKLYN','QUEENS','MANHATTAN','BRONX','STATEN ISLAND','UNSPECIFIED')"),
    ("zip is 5 digits or empty", "coalesce(t.incident_zip,'') = '' or regexp_matches(trim(t.incident_zip), '^\\d{5}$')"),
    ("coords in NYC bbox or empty",
     "(coalesce(cast(t.latitude as varchar),'') = '' and coalesce(cast(t.longitude as varchar),'') = '') or "
     "(try_cast(t.latitude as double) between 40.4 and 41.0 and try_cast(t.longitude as double) between -74.3 and -73.6)"),
    ("closed not before created",
     "try_cast(t.closed_date as timestamp) is null or try_cast(t.created_date as timestamp) is null or "
     "try_cast(t.closed_date as timestamp) >= try_cast(t.created_date as timestamp)"),
]
DUPE_KEY = "unique_key"

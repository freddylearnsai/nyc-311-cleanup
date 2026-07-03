"""Download one month of NYC 311 service requests to data/raw.csv (paginated)."""
import csv, io, sys, time, urllib.parse, urllib.request

BASE = "https://data.cityofnewyork.us/resource/erm2-nwe9.csv"
WHERE = "created_date between '2026-05-01T00:00:00' and '2026-05-31T23:59:59'"
FIELDS = ("unique_key,created_date,closed_date,agency,complaint_type,descriptor,"
          "borough,incident_zip,city,status,latitude,longitude")
PAGE = 50000

def page_url(offset: int) -> str:
    q = {"$where": WHERE, "$select": FIELDS, "$order": "unique_key", "$limit": PAGE, "$offset": offset}
    return f"{BASE}?{urllib.parse.urlencode(q)}"

def main() -> None:
    rows, offset, header = 0, 0, None
    with open("data/raw.csv", "w", newline="") as out:
        w = csv.writer(out)
        while True:
            with urllib.request.urlopen(page_url(offset), timeout=120) as r:
                text = r.read().decode()
            page = list(csv.reader(io.StringIO(text)))
            if not page: break
            if header is None:
                header = page[0]; w.writerow(header)
            body = page[1:]
            if not body: break
            w.writerows(body); rows += len(body); offset += PAGE
            print(f"fetched {rows} rows...", file=sys.stderr)
            if len(body) < PAGE: break
            time.sleep(1)  # be polite to the unauthenticated API
    print(rows)

if __name__ == "__main__":
    main()

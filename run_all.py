"""Timed end-to-end run: before-check → clean → after-check → receipts.md."""
import json, subprocess, time

def py(*args: str) -> str:
    return subprocess.run([".venv/bin/python", *args], check=True, capture_output=True, text=True).stdout

t0 = time.time()
before = json.loads(py("checks.py", "data/raw.csv", "before"))
fixes = json.loads(py("clean.py"))
after = json.loads(py("checks.py", "data/clean.parquet", "after"))
mins = round((time.time() - t0) / 60, 1)

receipts = f"""# Receipts — NYC 311 cleanup (May 2026 slice)

Measured from the actual run on this repo. Reproduce with `python run_all.py`.

| Receipt | Value |
| --- | --- |
| Rows in (raw) | {before['rows']} |
| Rows out (clean) | {fixes['rows_out']} |
| Duplicate keys removed | {fixes['duplicates_removed']} |
| Boroughs normalized | {fixes['boroughs_normalized']} |
| Invalid zips nulled | {fixes['invalid_zips_nulled']} |
| Out-of-bbox coords nulled | {fixes['out_of_bbox_coords_nulled']} |
| % passing all rules — before | {before['pct_passing_all']}% |
| % passing all rules — after | {after['pct_passing_all']}% |
| Pipeline runtime (fetch excluded) | {mins} min |

Rule-by-rule detail: [before](reports/before-report.md) · [after](reports/after-report.md)
"""
open("receipts.md", "w").write(receipts)
print(receipts)

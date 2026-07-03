"""Run RULES over a data file → markdown report + JSON totals."""
import json, sys
import duckdb
from rules import RULES, DUPE_KEY

def run(path: str, label: str) -> dict:
    con = duckdb.connect()
    src = f"read_csv_auto('{path}', all_varchar=true)" if path.endswith(".csv") else f"read_parquet('{path}')"
    con.execute(f"create view t as select * from {src}")
    total = con.execute("select count(*) from t").fetchone()[0]
    dupes = total - con.execute(f"select count(distinct {DUPE_KEY}) from t").fetchone()[0]
    results = []
    for name, pred in RULES:
        passing = con.execute(f"select count(*) from t where {pred}").fetchone()[0]
        results.append({"rule": name, "passing": passing, "pct": round(100 * passing / total, 2)})
    all_pass = con.execute(
        "select count(*) from t where " + " and ".join(f"({p})" for _, p in RULES)).fetchone()[0]
    out = {"label": label, "rows": total, "duplicate_keys": dupes,
           "rules": results, "rows_passing_all": all_pass,
           "pct_passing_all": round(100 * all_pass / total, 2)}
    lines = [f"# {label} report", "", f"Rows: **{total}**  ·  Duplicate `{DUPE_KEY}`s: **{dupes}**", "",
             "| Rule | Passing | % |", "| --- | --- | --- |"]
    lines += [f"| {r['rule']} | {r['passing']} | {r['pct']}% |" for r in results]
    lines += ["", f"**Rows passing all rules: {all_pass} ({out['pct_passing_all']}%)**", ""]
    with open(f"reports/{label}-report.md", "w") as f: f.write("\n".join(lines))
    return out

if __name__ == "__main__":
    print(json.dumps(run(sys.argv[1], sys.argv[2])))

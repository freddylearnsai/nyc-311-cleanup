# nyc-311-cleanup

A documented, repeatable cleaning pipeline for one month of NYC 311 service requests — built in public by [freddyxai](https://freddyxai.com/work-with-me).

**Receipts:** see [receipts.md](receipts.md) — every number measured from the run.

Built by [freddyxai](https://freddyxai.com) — your data team, on demand. This is the shape of a [$500 starter cleanup](https://freddyxai.com/work-with-me): one dataset, cleaned and validated, with the report to prove it.

## Reproduce

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python fetch.py        # downloads data/raw.csv (May 2026 slice)
.venv/bin/python run_all.py      # before-report → clean → after-report → receipts.md
```

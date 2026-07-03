# nyc-311-cleanup

A documented, repeatable cleaning pipeline for one month of NYC 311 service requests — built in public by [freddyxai](https://freddyxai.com/work-with-me).

Status: build in progress. Receipts land in `receipts.md` when the run completes.

## Reproduce

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python fetch.py        # downloads data/raw.csv (May 2026 slice)
.venv/bin/python run_all.py      # before-report → clean → after-report → receipts.md
```

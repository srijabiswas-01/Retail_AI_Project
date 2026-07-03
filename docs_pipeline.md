# Pipeline Integration Guide

Use `run_pipeline.py` to run project stages in a controlled order.

## Common Commands

Run the complete pipeline:

```powershell
.\.venv\Scripts\python.exe run_pipeline.py
```

Run a fast integration pass without heavy LSTM/recommendation similarity builds:

```powershell
.\.venv\Scripts\python.exe run_pipeline.py --skip-heavy
```

Run selected stages:

```powershell
.\.venv\Scripts\python.exe run_pipeline.py --stages features inventory database
```

## Available Stages

- `etl`
- `features`
- `forecasting`
- `inventory`
- `recommendation`
- `customer`
- `database`

Stage definitions live in `pipeline_config.py`.

## Shared Configuration

Project paths are centralized in:

```text
src/config/paths.py
```

CSV helpers and column validation are centralized in:

```text
src/utils/io.py
```

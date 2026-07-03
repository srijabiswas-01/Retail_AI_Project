import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

from pipeline_config import DEFAULT_STAGE_ORDER, PIPELINE_STAGES
from src.config.paths import PROJECT_ROOT, ensure_project_directories


def run_script(script: str) -> None:
    script_path = PROJECT_ROOT / script
    if not script_path.exists():
        raise FileNotFoundError(f"Pipeline script not found: {script_path}")

    start = time.perf_counter()
    print(f"\n[RUN] {script}")
    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        str(PROJECT_ROOT)
        if not existing_pythonpath
        else f"{PROJECT_ROOT}{os.pathsep}{existing_pythonpath}"
    )

    subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT,
        check=True,
        env=env,
    )

    elapsed = time.perf_counter() - start
    print(f"[DONE] {script} ({elapsed:.1f}s)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the Retail AI project pipeline in a controlled order."
    )
    parser.add_argument(
        "--stages",
        nargs="+",
        choices=list(PIPELINE_STAGES.keys()),
        default=DEFAULT_STAGE_ORDER,
        help="Pipeline stages to run. Defaults to the complete pipeline.",
    )
    parser.add_argument(
        "--skip-heavy",
        action="store_true",
        help="Skip recommendation similarity build and LSTM training for faster iteration.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ensure_project_directories()

    print("Retail AI pipeline")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Stages: {', '.join(args.stages)}")

    for stage in args.stages:
        print(f"\n=== Stage: {stage} ===")
        scripts = PIPELINE_STAGES[stage]

        for script in scripts:
            if args.skip_heavy and script in {
                "forecasting/lstm_model.py",
                "recommendation/recommendation_engine.py",
            }:
                print(f"[SKIP] {script}")
                continue

            run_script(script)

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()

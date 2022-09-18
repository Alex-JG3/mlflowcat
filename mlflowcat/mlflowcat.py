import re


def is_valid_run_id(run_id: str):
    """Return True if `run_id` is a valid mlflow run_id."""
    pattern = r"^[0-9a-z]{32}$"
    return bool(re.match(pattern, run_id))

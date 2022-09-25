import random
import string
import pytest
from mlflowcat import mlflowcat


@pytest.mark.parametrize(
    "run_id",
    [
        "73bf7b7b884a4f35be4d3c0b045a6898",
        "34hdf5hjfds890ffhj321kfdsf0vhbjd",
        pytest.param(
            "34hdf5hjfds890ffhj321kfdsf0vhb", marks=pytest.mark.xfail  # too short
        ),
        pytest.param(
            "34hdf5hjfds890ffhj321kfdsf0vhbjdkc", marks=pytest.mark.xfail  # too long
        ),
        pytest.param(
            "73bf7b7b884_4f35be4d3c0b045a6898",  # illegal '_' character
            marks=pytest.mark.xfail,
        ),
        pytest.param(
            "73bf7b7b884a4f35b.4d3c0b045a6898",  # illegal '.' character
            marks=pytest.mark.xfail,
        ),
        pytest.param(
            "73Bf7b7b884f4f35be4d3c0b045a6898",  # illegal capital 'B'
            marks=pytest.mark.xfail,
        ),
    ],
)
def test_is_valid_run_id(run_id):
    run_id = "73bf7b7b884a4f35be4d3c0b045a6898"
    assert mlflowcat.is_valid_run_id(run_id)


@pytest.fixture
def test_create_run(tmp_path):
    """Create a toy mlflow run"""
    run_id = "".join(
        [random.choice(string.ascii_letters + string.digits) for _ in range(32)]
    ).lower()

    run_path = tmp_path / run_id
    params_path = run_path / "params"
    metrics_path = run_path / "metrics"

    run_path.mkdir()
    params_path.mkdir()
    metrics_path.mkdir()

    for i in range(10):
        param_path = params_path / f"param_{i}"
        with param_path.open("w", encoding="utf-8") as f:
            f.write(f"value_{i}")

    return run_path


def test_mlflow_cat(test_create_run):
    run_path = test_create_run
    mlflowcat.mlflowcat(run_path)


@pytest.mark.parametrize(
    "dictionary",
    [
        {
            "key_1": "value_1",
            "key_2": "value_2",
            "key_3": "value_3",
            "key_4": "value_4",
        }
    ],
)
def test_table(dictionary):
    table = mlflowcat.Table()
    table.write_dictionary_to_table(dictionary)
    print("\n")
    print(table.table.getvalue())

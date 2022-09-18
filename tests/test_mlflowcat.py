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

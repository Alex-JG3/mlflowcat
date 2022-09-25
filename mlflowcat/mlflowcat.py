import io
import re
import pathlib


def is_valid_run_id(run_id: str):
    """Return True if `run_id` is a valid mlflow run_id."""
    pattern = r"^[0-9a-z]{32}$"
    return bool(re.match(pattern, run_id))


def mlflowcat(path_to_run: pathlib.Path):
    run_id = path_to_run.name

    if not is_valid_run_id(run_id):
        raise RuntimeError(f"{path_to_run.name} is not a valid run ID")

    get_params(path_to_run)


def get_params(path_to_run):
    path_to_params = path_to_run / "params"
    name_to_value = {}

    for p in path_to_params.glob("*"):
        name = p.name
        with open(p) as f:
            value = next(f)
            name_to_value[name] = value

            # Check that the parameter file has only one line
            try:
                value = next(f)
            except StopIteration:
                pass
            else:
                raise RuntimeError("Parameter files should only have one line")


class Table:
    def __init__(
        self,
        column_width: int = 10,
        cell_padding: int = 1,
        left_padding: int = 2,
    ):
        self.table = io.StringIO()
        self.column_width = column_width
        self.cell_padding = cell_padding
        self.left_padding = left_padding

    def _write_key_value_to_table(self, key: str, value: str):
        key = key.ljust(self.column_width)
        value = value.ljust(self.column_width)
        left_pad = " " * self.left_padding
        cell_pad = " " * self.cell_padding
        row = (
            left_pad
            + "|"
            + cell_pad
            + key
            + cell_pad
            + "|"
            + cell_pad
            + value
            + cell_pad
            + "|\n"
        )
        self.table.write(row)

    def _write_top_to_table(
        self,
    ):
        left_pad = " " * self.left_padding
        line = "-" * (2 * self.cell_padding + self.column_width)
        top = left_pad + "+" + line + "+" + line + "+\n"
        self.table.write(top)

    def write_dictionary_to_table(self, dictionary: dict[str, str]):
        self._write_top_to_table()
        for key, value in dictionary.items():
            self._write_key_value_to_table(key, value)
        self._write_top_to_table()

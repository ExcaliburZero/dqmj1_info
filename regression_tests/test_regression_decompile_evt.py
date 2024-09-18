import inspect
import sys

from .util import Util, rel_data, update_baselines


class TestRegressionDecompileEvtBasic(Util.TestRegression):
    name = "decompile_evt_basic"
    command = [
        "dqmj1_decompile_evt",
        "--evt_filepaths",
        rel_data("basic.evt"),
        "--output_directory",
        ".",
        "--character_encoding",
        "North America / Europe",
    ]
    expected_files = [("basic.evt.dqmj1_script", "r")]
    expected_status_code = 0


if __name__ == "__main__":
    tests = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj) and obj != Util:
            tests.append(obj)

    update_baselines(tests)

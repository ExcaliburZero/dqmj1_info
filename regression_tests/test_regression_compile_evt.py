import inspect
import sys

from .util import Util, rel_data, update_baselines


class TestRegressionCompileEvtBasic(Util.TestRegression):
    name = "compile_evt_basic"
    command = [
        "dqmj1_compile_evt",
        "--script_filepaths",
        rel_data("basic.dqmj1_script"),
        "--output_directory",
        ".",
        "--character_encoding",
        "North America / Europe",
    ]
    expected_files = [("basic.evt", "rb")]
    expected_status_code = 0


if __name__ == "__main__":
    tests = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj) and obj != Util:
            tests.append(obj)

    update_baselines(tests)

from typing import List, Optional, Tuple

import os
import pathlib
import shutil
import subprocess
import unittest


def rel_data(filepath: str) -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", filepath)


class Util:
    class TestRegression(unittest.TestCase):
        name: str
        command: List[str]
        expected_files: List[Tuple[str, str]]
        expected_status_code: int
        stdin: Optional[List[str]] = None

        def test(self) -> None:
            work_dir = self.get_work_dir()
            self.setup_dir(work_dir)

            status_code = self.run_command(work_dir)
            self.assertEqual(self.expected_status_code, status_code)

            # Note: Only check against baselines on non-Windows OSs, since windows has some
            # differences that I don't want to add support for smartly diffing yet.
            if not os.name == "nt":
                self.diff_against_baselines(work_dir)

        def get_work_dir(self) -> pathlib.Path:
            return (
                pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
                / "work_dirs"
                / self.name
            )

        def get_baseline_dir(self) -> pathlib.Path:
            return (
                pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
                / "baselines"
                / self.name
            )

        def setup_dir(
            self, work_dir: pathlib.Path, clear_if_exists: bool = True
        ) -> None:
            if work_dir.exists() and clear_if_exists:
                shutil.rmtree(work_dir)

            work_dir.mkdir(parents=True, exist_ok=not clear_if_exists)

        def run_command(self, work_dir: pathlib.Path) -> int:
            process = subprocess.Popen(
                self.command,
                cwd=work_dir,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if self.stdin is not None:
                stdout, stderr = process.communicate(
                    input="\n".join(self.stdin).encode("utf-8")
                )
            else:
                stdout, stderr = process.communicate()

            print("Stdout:")
            print(stdout.decode("utf8"))
            print("Stderr:")
            print(stderr.decode("utf8"))

            return process.returncode

        def diff_against_baselines(self, work_dir: pathlib.Path) -> None:
            baseline_dir = self.get_baseline_dir()
            self.assertTrue(baseline_dir.exists())

            for filename, open_mode in self.expected_files:
                actual = work_dir / filename
                baseline = baseline_dir / filename

                self.assertTrue(actual.exists())
                self.assertTrue(baseline.exists())

                with open(baseline, open_mode) as baseline_stream:
                    with open(actual, open_mode) as actual_stream:
                        self.assertEqual(list(baseline_stream), list(actual_stream))

        def update_baseline(self) -> None:
            work_dir = self.get_work_dir()
            self.setup_dir(work_dir)

            self.run_command(work_dir)

            baseline_dir = self.get_baseline_dir()
            self.setup_dir(baseline_dir)

            shutil.copytree(work_dir, baseline_dir, dirs_exist_ok=True)


def update_baselines(tests: List[type[Util.TestRegression]]) -> None:
    for test in tests:
        print(f"Updating baseline: {test.name}")
        t = test()
        t.update_baseline()

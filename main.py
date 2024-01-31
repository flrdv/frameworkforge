import dataclasses
import os
import shutil
import string
import subprocess
import time

import internal.si as si

FRAMEWORKS_DIR = "frameworks"
CASES_DIR = "cases"


class Framework:
    def __init__(self, language: str, name: str):
        self.language = language
        self.name = name
        self.stdout: str | None = None
        self.process: subprocess.Popen | None = None

    def __enter__(self):
        self.process = subprocess.Popen(
            ["go", "run", "."],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.path.join(FRAMEWORKS_DIR, self.language, self.name),
            shell=True,
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stdout = self.process.stdout.read()
        self.process.kill()


def get_frameworks(language: str) -> list[str]:
    return os.listdir(os.path.join(FRAMEWORKS_DIR, language))


def get_cases() -> list[str]:
    return os.listdir(CASES_DIR)


def run_wrk(
        duration: int = 10,
        threads: int = 12,
        clients: int = 1000,
        case: str = "",
        addr: str = "http://localhost:8080"
) -> str:
    cmd = ["wrk", f"-t{threads}", f"-c{clients}", f"-d{duration}s"]
    if len(case) > 0:
        cmd.append(f"-s{case}")

    return subprocess.check_output(
        cmd + [addr],
    ).decode()


# @dataclasses.dataclass
# class Latency:
#     avg: int
#     max: int


@dataclasses.dataclass
class Report:
    rps: float
    avg_latency: float
    max_latency: float


def parse_wrk_output(out: str) -> Report:
    lines = out.splitlines(keepends=False)
    latency_line, rps_line = lines[3], lines[7]
    _, avg, _, maximal, _ = filter(bool, latency_line.split())
    avg_latency, max_latency = si.parse(avg), si.parse(maximal)
    rps = float(rps_line.split(": ")[1])

    return Report(
        rps=rps,
        avg_latency=avg_latency,
        max_latency=max_latency,
    )


def main():
    results: dict[str, dict[str, Report]] = {}

    for framework in get_frameworks("go"):
        print(f"{framework}:")
        results[framework] = {}

        for case in get_cases():
            print(f"  {case}:")
            f = Framework("go", framework)
            with f:
                report = parse_wrk_output(run_wrk(
                    case=os.path.join(CASES_DIR, case),
                ))

                results[framework][case] = report
                print(f"    Requests/sec: {report.rps}")
                print(f"    Latency: "
                      f"avg={si.serialize(report.avg_latency)} "
                      f"max={si.serialize(report.max_latency)}")

        print(end="\n\n")


if __name__ == "__main__":
    main()

import os
import shutil
import subprocess
import time

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


def main():
    for framework in get_frameworks("go"):
        print(f"{framework}:")

        for case in get_cases():
            print(f"case {case}:")
            f = Framework("go", framework)
            with f:
                print(run_wrk(
                    case=os.path.join(CASES_DIR, case),
                ))


if __name__ == "__main__":
    main()

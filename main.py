from pathlib import Path
from typing import List
import requests
import subprocess
from core.logic import RestoreStatus, restore
from core.package import Package
from core.parser import parse

SLN_PATH: Path = Path(__file__).parent / "test_data" / "NuGetTestProject.sln"
DOWNLOAD_PACKAGES_DIR: Path = Path(__file__).parent / "downloaded_packages"
CSPROJ_PATH: Path = (
    Path(__file__).parent / "test_data" / "NuGetTestProject" / "NuGetTestProject.csproj"
)


def main() -> None:
    csproj_content: str = open(CSPROJ_PATH, "r", encoding="utf-8").read()

    while True:
        restore_status: RestoreStatus = restore(SLN_PATH, csproj_content)
        if restore_status.success:
            print(
                f"Restore completed: {restore_status.restored_packages} packages restored, "
                f"{restore_status.downloaded_packages} packages downloaded."
            )
            break
        else:
            print("Restore failed, retrying...")


if __name__ == "__main__":
    main()

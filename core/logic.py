from dataclasses import dataclass
from pathlib import Path
import subprocess
from typing import List, Optional

from core.package import Package, get_url
from core.parser import parse, parse_version_from_csproj
from core.utils import download_package, download_package_versions


@dataclass
class RestoreStatus:
    success: bool
    restored_packages: int
    downloaded_packages: int


def restore(sln_path: Path, csproj_content: Optional[str]) -> RestoreStatus:
    packages: List[Package] = get_packages_to_restore(sln_path)

    if not packages:
        return RestoreStatus(
            success=True,
            restored_packages=0,
            downloaded_packages=0,
        )

    for package in packages:
        if not package.version and csproj_content:
            version_in_csproj: Optional[str] = parse_version_from_csproj(
                csproj_content, package.name
            )
            if version_in_csproj:
                package = Package(name=package.name, version=version_in_csproj)

        handle_package(package, Path("./downloaded_packages"))

    return RestoreStatus(
        success=True,
        restored_packages=len(packages),
        downloaded_packages=0,
    )


def handle_package_with_version(package: Package, packages_destination: Path) -> bool:
    print(f"Processing package: {package.name} {package.version}")
    nupkg_url: str = get_url(package)
    file_name: str = f"{package.name}.{package.version}.nupkg"
    print(f"Downloading from URL: {nupkg_url}")
    try:
        download_package(nupkg_url, packages_destination, file_name)
    except Exception as e:
        print(f"Failed to download package {package.name} {package.version}: {e}")
        return False
    return True


def handle_package(package: Package, packages_destination: Path) -> bool:
    print(f"Processing package: {package.name} {package.version}")
    if package.version:
        return handle_package_with_version(package, packages_destination)

    print(f"Processing package without version: {package.name}")
    versions: List[str] = download_package_versions(package)

    for version in versions:
        package_with_version = Package(name=package.name, version=version)
        handle_package_with_version(package_with_version, packages_destination)

    return True


def get_restore_logs(sln_path: Path) -> str:
    cmd: subprocess.CompletedProcess[bytes] = subprocess.run(
        [
            "dotnet",
            "restore",
            str(sln_path),
        ],
        stdout=subprocess.PIPE,
    )
    return str(cmd.stdout, encoding="utf-8")


def parse_restore_logs(logs: str) -> list[Package]:
    packages: List[Package] = parse(logs)
    return packages


def get_packages_to_restore(sln_path: Path) -> list[Package]:
    logs: str = get_restore_logs(sln_path)
    packages: List[Package] = parse_restore_logs(logs)
    return packages


def get_urls_from_packages(packages: List[Package]) -> List[str]:
    urls: list[str] = []
    for package in packages:
        url: str = f"https://www.nuget.org/api/v2/package/{package.name}"
        if package.version:
            url += f"/{package.version}"
        urls.append(url)
    return urls

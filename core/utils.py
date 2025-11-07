from pathlib import Path
import requests

from core.package import Package, get_nuget_index_url


def download_package(url: str, dest: Path, file_name: str) -> Path:
    local_path = dest / file_name
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    return local_path


def download_package_versions(package: Package) -> list[str]:
    versions_url = get_nuget_index_url(package)
    try:
        response: requests.Response = requests.get(versions_url)
        response.raise_for_status()
        versions_data = response.json()
        versions = versions_data.get("versions", [])
    except Exception as e:
        print(f"Failed to fetch versions for package {package}: {e}")
        return []
    return versions

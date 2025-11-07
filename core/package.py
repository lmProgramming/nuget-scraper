from dataclasses import dataclass
from typing import List, Optional

NUGET_URL = "https://www.nuget.org/api/v3-flatcontainer"


@dataclass(frozen=True)
class Package:
    name: str
    version: Optional[str] = None


def get_urls(packages: List[Package]) -> List[str]:
    urls: list[str] = []
    for package in packages:
        url: str = f"htttps://www.nuget.org/api/v2/package/{package.name}"
        if package.version:
            url += f"/{package.version}"
        urls.append(url)
    return urls


def get_nuget_index_url(package: Package) -> str:
    return f"{NUGET_URL}/{package.name}/index.json"


def get_url(package: Package) -> str:
    url: str = (
        f"{NUGET_URL}/{package.name}/{package.version}/{package.name}.{package.version}.nupkg"
    )
    if package.version:
        url += f"/{package.version}"
    return url

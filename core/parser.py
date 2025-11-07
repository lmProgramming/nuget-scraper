import re
from typing import Optional, List
import xml.etree.ElementTree as ET

from core.package import Package


def parse_version_from_csproj(csproj_xml: str, package_name: str) -> Optional[str]:
    root = ET.fromstring(csproj_xml)

    for pr in root.iter():
        if not pr.tag.endswith("PackageReference"):
            continue

        include_name = pr.attrib.get("Include") or pr.attrib.get("Update")
        if include_name != package_name:
            continue

        version_attr = pr.attrib.get("Version")
        if version_attr:
            return version_attr.strip()

        for child in pr:
            if child.tag.endswith("Version") and child.text:
                text = child.text.strip()
                if text:
                    return text

    return None


def parse(text: str) -> List[Package]:
    if not text:
        return []

    results_set = set()

    def add(name: str, version: Optional[str]):
        results_set.add(Package(name=name.rstrip("."), version=version))

    def extract_version_from_constraint(constraint: str) -> Optional[str]:
        match = re.search(r"\d+(?:\.\d+)+", constraint)
        return match.group(0) if match else None

    unable_find_re = re.compile(
        r"Unable to find package\s+(?P<name>[A-Za-z0-9][A-Za-z0-9\.\-\+\_]*)(?:\s+with version\s+\((?P<constraint>[^)]+)\))?",
        re.IGNORECASE,
    )

    depends_on_re = re.compile(
        r"depends on\s+(?P<name>[A-Za-z0-9][A-Za-z0-9\.\-\+\_]*)(?:\s*\((?P<constraint>[^)]+)\))?",
        re.IGNORECASE,
    )

    downgrade_re = re.compile(
        r"Detected package downgrade:\s+(?P<name>[A-Za-z0-9][A-Za-z0-9\.\-\+\_]*)(?:\s+from\s+(?P<from>\d+(?:\.\d+)+)\s+to\s+(?P<to>\d+(?:\.\d+)+))?",
        re.IGNORECASE,
    )

    name_version_re = re.compile(
        r"\b(?P<name>[A-Za-z0-9][A-Za-z0-9\.\-\+\_]*)\b\s+(?P<version>\d+(?:\.\d+)+)\b",
        re.IGNORECASE,
    )

    def parse_chain_line(line: str):
        parts = [part.strip() for part in line.split("->")]
        for part in parts[1:]:
            if not part:
                continue
            match_version = re.match(
                r"^(?P<name>[A-Za-z0-9][A-Za-z0-9\.\-\+\_]*)\s+(?P<version>\d+(?:\.\d+)+)",
                part,
            )
            if match_version:
                name = match_version.group("name")
                version = match_version.group("version")
                add(name, version)
            else:
                name_only = part.strip()
                add(name_only, None)

            match_constraint_version = re.match(
                r"^(?P<name>[A-Za-z0-9][A-Za-z0-9\.\-\+\_]*)\s+\((?P<constraint>[^)]+)\)",
                part,
            )
            if match_constraint_version:
                name = match_constraint_version.group("name")
                constraint = match_constraint_version.group("constraint")
                version = extract_version_from_constraint(constraint)
                add(name, version)

            bare = re.match(
                r"^(?P<name>[A-Za-z0-9][A-Za-z0-9\.\-\+\_]*)$",
                part,
            )
            if bare:
                name = bare.group("name")
                add(name, None)

    for raw_line in text.splitlines():
        line = raw_line.strip().lower()
        if not line:
            continue

        m = unable_find_re.search(line)
        if m:
            name = m.group("name")
            constraint = m.group("constraint")
            version = (
                extract_version_from_constraint(constraint) if constraint else None
            )
            add(name, version)
            continue

        md = depends_on_re.search(line)
        if md:
            name = md.group("name")
            constraint = md.group("constraint")
            version = (
                extract_version_from_constraint(constraint) if constraint else None
            )
            add(name, version)
            # do not continue, as it may also have "was not found" or "resolves"

        m_downgrade = downgrade_re.search(line)
        if m_downgrade:
            name = m_downgrade.group("name")
            from_version = m_downgrade.group("from")
            to_version = m_downgrade.group("to")
            add(name, from_version)
            add(name, to_version)

        if ("was not found" in line) or ("resolved to" in line):
            for mv in name_version_re.finditer(line):
                name = mv.group("name")
                version = mv.group("version")
                add(name, version)

        if "NU1605" in line and "->" in line:
            parse_chain_line(line)
        elif "->" in line and ("error" in line or "warning" in line):
            parse_chain_line(line)

    return sorted(results_set, key=lambda p: (p.name.lower(), p.version or ""))

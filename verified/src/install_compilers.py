import os
from solcx import install_solc, get_installed_solc_versions
import re


def get_solidity_versions_from_folders(directory):
    """Extracts Solidity compiler versions from folder names"""
    versions = set()  # Use a set to avoid duplicate versions
    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        if os.path.isdir(path):
            # Extract the version assuming the folder name ends with a version number
            match = re.search(r"\d+\.\d+\.\d+$", item)
            if match:
                versions.add(match.group(0))
    return versions


def install_solidity_versions(versions):
    """Installs given Solidity compiler versions if they aren't already installed"""
    installed_versions = get_installed_solc_versions()
    for version in versions:
        if version not in installed_versions:
            print(f"Installing Solidity version {version}...")
            install_solc(version)


directory = "contracts"
versions = get_solidity_versions_from_folders(directory)
print(f"The following Solidity versions are required: {versions}")
install_solidity_versions(versions)
print(f"All required Solidity versions installed.")

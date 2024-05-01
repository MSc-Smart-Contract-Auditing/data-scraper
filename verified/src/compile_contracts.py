from solcx import compile_files, install_solc, get_solc_version, set_solc_version
import os
import json
from pathlib import Path


def compile_contract_directory(directory, version):

    # Extract the version from the directory name
    version = str(directory).split("-")[-1]
    print(f"Compiling {directory}...")
    print(f"Using Solidity version {version}")

    # Ensure the compiler version is installed and set it
    set_solc_version(version)

    # List all .sol files in the directory
    sol_files = [f for f in os.listdir(directory) if f.endswith(".sol")]
    sol_paths = [directory / filename for filename in sol_files]
    # Compile all Solidity files and request the AST
    compiled_contracts = compile_files(sol_paths, output_values=["ast"])
    compiled_dir = directory / "out"
    os.makedirs(compiled_dir, exist_ok=True)

    for contract_path, contract_data in compiled_contracts.items():
        contract_name = contract_path.split(":")[-1]
        with open(compiled_dir / f"{contract_name}.ast.json", "w") as ast_file:
            json.dump(contract_data["ast"], ast_file, indent=4)


def list_directories(path):
    directories = []
    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)):
            directories.append(item)
    return directories


def extract_version(directory):
    return str(directory).split("-")[-1]


folder_path = Path("contracts")
directories = list_directories(folder_path)


for contract_dir in directories:
    compile_contract_directory(
        folder_path / contract_dir, extract_version(contract_dir)
    )

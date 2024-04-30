import re
import os


def replace_imports(file_path):
    # Read the content of the Solidity file
    with open(file_path, "r") as file:
        content = file.read()

    # Define the regex pattern to match import statements
    full_import = re.compile(r'import "((\.\.?)(\/\w*)*\/)*(\w+).sol";', re.MULTILINE)
    partial_import = re.compile(
        r'import {\s*(\w+(, \w+)*)\s*} from "((\.\.?)?(\/?\w*)*\/)*(\w+).sol";',
        re.MULTILINE,
    )
    # Replace import statements according to the pattern
    content = re.sub(full_import, r'import "./\4.sol";', content)
    content = re.sub(partial_import, r'import { \1 } from "./\6.sol";', content)

    # Write the modified content back to the file
    with open(file_path, "w") as file:
        file.write(content)


def get_contract_paths(root_folder):
    contract_paths = []
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith(".sol"):  # Filter for Solidity files
                contract_paths.append(os.path.join(root, file))
    return contract_paths


ROOT_FOLDER = "contracts"


all_contract_paths = get_contract_paths(ROOT_FOLDER)

for contract_path in all_contract_paths:
    replace_imports(contract_path)


print(f"Prepared {len(all_contract_paths)} contracts successfully!")

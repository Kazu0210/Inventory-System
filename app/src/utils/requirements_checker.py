import json
import importlib.util

import install_requirements

def is_library_installed(library_name):
    spec = importlib.util.find_spec(library_name)
    return spec is not None

requirements_dir = "app/resources/data/requirements.json"

with open(requirements_dir, 'r') as f:
    requirements = json.load(f)

for requirement in requirements:
    print(requirement)
    if is_library_installed(requirement):
        print(f"{requirement} is installed")
    else:
        print(f"{requirement} is not installed")
        install_requirements.install(requirement)
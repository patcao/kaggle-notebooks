from pathlib import Path
import shutil
import subprocess
import sys
import shutil

def create_vscode_project(project_name: str, requirements_path: str):
    # Get the current working directory
    base_dir = Path.cwd() / project_name

    # Create the project directory and bin directory
    bin_dir = base_dir / 'bin'
    bin_dir.mkdir(parents=True, exist_ok=True)

    # Create virtual environment
    venv_path = base_dir / f"{project_name}-venv"
    print(f"Creating virtual environment at {venv_path}...")
    subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)

    # Activate virtual environment and install packages
    pip_path = venv_path / 'bin' / 'pip'
    python_path = venv_path / 'bin' / 'python'

    requirements_file = Path(requirements_path)
    if requirements_file.exists():
        print(f"Installing packages from {requirements_file}...")
        subprocess.run([str(pip_path), "install", "-r", str(requirements_file)], check=True)
    else:
        print(f"Warning: {requirements_file} not found. Skipping package installation.")

    # Export installed packages to requirements.in
    # requirements_in_path = base_dir / f'{project_name}.in'
    # shutil.copy2(requirements_file, requirements_in_path)

    # Export installed packages to requirements.txt
    output_requirements_path = base_dir / 'requirements.txt'
    print(f"Exporting installed packages to {output_requirements_path}...")
    with open(output_requirements_path, 'w') as f:
        subprocess.run([str(pip_path), "freeze"], stdout=f)

    # Create .code-workspace file
    workspace_file = base_dir / f"{project_name}.code-workspace"
    workspace_content = f"""
{{
    "folders": [
        {{
            "path": "."
        }}
    ],
    "settings": {{
        "python.pythonPath": "{python_path}"
    }}
}}
    """

    workspace_file.write_text(workspace_content.strip())
    print(f"Created VSCode workspace file: {workspace_file}")

    # Create activate script in bin directory for easier activation
    activate_script_path = bin_dir / 'activate'
    activate_script_content = f"""#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"

# Activate the virtual environment
source "$SCRIPT_DIR/../{project_name}-venv/bin/activate"
    """
    
    activate_script_path.write_text(activate_script_content)
    
    # Make the activate script executable
    activate_script_path.chmod(0o755)
    print(f"Created activation script: {activate_script_path}")

    print(f"\n✅ Project '{project_name}' has been successfully created.")
    print(f"📁 Location: {base_dir}")
    print(f"📂 Virtual environment path: {venv_path}")
    print(f"📄 VSCode workspace file: {workspace_file}")
    print(f"📜 requirements.txt saved at: {output_requirements_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python create_vscode_project.py <project_name> <requirements.txt path>")
        sys.exit(1)

    project_name = sys.argv[1]
    requirements_path = sys.argv[2]

    create_vscode_project(project_name, requirements_path)

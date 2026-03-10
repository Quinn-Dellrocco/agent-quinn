import os
import subprocess
from google import genai
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        if args is None:
            args = []
        
        working_dir_abs = os.path.abspath(working_directory)
        absolute_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target = os.path.commonpath([working_dir_abs, absolute_file_path]) == working_dir_abs

        if not valid_target:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not absolute_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", absolute_file_path]
        if args:
            command.extend(args)

        completed = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )

        stdout = completed.stdout or ""
        stderr = completed.stderr or ""

        parts = []

        if completed.returncode != 0:
            parts.append(f"Process exited with code {completed.returncode}")

        if stdout == "" and stderr == "":
            parts.append("No output produced")
        else:
            if stdout != "":
                parts.append("STDOUT:")
                parts.append(stdout.rstrip("\n"))
            if stderr != "":
                parts.append("STDERR:")
                parts.append(stderr.rstrip("\n"))

        return "\n".join(parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python (.py) file relative to the working directory, optionally passing command-line arguments, and returns captured stdout/stderr.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Python file path to execute, relative to the working directory (must end with .py).",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of command-line arguments to pass to the Python file.",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="A single command-line argument string.",
                ),
            ),
        },
        required=["file_path"],
    ),
)
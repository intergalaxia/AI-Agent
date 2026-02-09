import os
import subprocess 
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=None):
    working_directory = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))
    command = ["python", target_path]

    try:
        if os.path.commonpath([working_directory, target_path]) != working_directory:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        if args:
            command.extend(args)

        result = subprocess.run(command, cwd=working_directory, capture_output=True, text=True, timeout=30)

        output = []

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")


        if not result.stdout and not result.stderr:
            output.append("No output produced")
        else:
            if result.stdout:
                output.append(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                output.append(f"STDERR:\n{result.stderr}")

        return "\n".join(output)
        
    
    except Exception as e:
        return f"Error: executing Python file: {e}"

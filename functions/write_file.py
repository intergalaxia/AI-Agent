import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write/overwrite",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text to write into the file",
            ),
        },
        required=["file_path", "content"],
    ),
)

def write_file(working_directory,file_path,content):
    working_directory = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))
    parent_dir = os.path.dirname(target_path)

    try:
        if os.path.commonpath([working_directory, target_path]) != working_directory:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        else: 
            os.makedirs(parent_dir, exist_ok=True)
            with open(target_path, "w") as f:
                f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        return f"Error: {e}"
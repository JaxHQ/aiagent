import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    full_abspath = os.path.abspath(full_path)
    if not full_abspath.startswith(os.path.abspath(working_directory)):
        return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if not os.path.isdir(full_abspath):
        return (f'Error: "{directory}" is not a directory')
    
    try:
        entries = os.listdir(full_abspath)
        result_lines = []
        for entry in entries:
            fullpath = os.path.join(full_abspath, entry)
            size = os.path.getsize(fullpath)
            isdir = os.path.isdir(fullpath)
            result_lines.append(f"- {entry}: file_size={size} bytes, is_dir={isdir}")
        return "\n".join(result_lines)
    except Exception as e:
        return f"Error: {e}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory.",
            ),
        },
    ),
)

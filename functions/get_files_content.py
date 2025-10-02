import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    full_abspath = os.path.abspath(full_path)

    if not full_abspath.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
   
    if not os.path.isfile(full_abspath):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(full_abspath, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):  # peek ahead
                file_content_string += f' [...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string
    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the file to read content from relative to the working Dir.",
            ),
        },
    ),
)
import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    full_abspath = os.path.abspath(full_path)

    if not full_abspath.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_abspath):
        return f'Error: File "{file_path}" not found.'
    if not full_abspath.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:

        cmd = ["python3", full_abspath] + args
        completed_process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=os.path.abspath(working_directory)
        )

        output_parts = []
        if completed_process.stdout.strip():
            output_parts.append(f"STDOUT:\n{completed_process.stdout.strip()}")
        if completed_process.stderr.strip():
            output_parts.append(f"STDERR:\n{completed_process.stderr.strip()}")
        if completed_process.returncode != 0:
            output_parts.append(f"Process exited with code {completed_process.returncode}")
        
        if not output_parts:
            return "No output produced."
        return "\n".join(output_parts)
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
            
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python files with optional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the python file to use for executing optional arguemnts relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of cammand-line arguments to pass to Python file.",
                items=types.Schema(type=types.Type.STRING)
            )
        },
    ),
)
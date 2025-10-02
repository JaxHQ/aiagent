from google.genai import types

from functions.get_files_info import get_files_info
from functions.get_files_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

WORKING_DIR = "./calculator"

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    fn_args = dict(function_call_part.args or {})

    if verbose:
        print(f"Calling function: {function_name}({fn_args})")
    else:
        print(f" - Calling function: {function_name}")

        
    registry = {
            "get_files_info": get_files_info,
            "get_file_content": get_file_content,
            "write_file": write_file,
            "run_python_file": run_python_file,
        }

    if function_name not in registry:
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
            )
        ],
    )

    fn_args["working_directory"] = WORKING_DIR

    try:
        result_str = registry[function_name](**fn_args)
    except Exception as e:
        result_str = f"Error: {e}"

    return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": result_str},
                )
            ],
        )
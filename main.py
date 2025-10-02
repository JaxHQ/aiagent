import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_files_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from call_function import call_function


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_run_python_file,
        schema_get_file_content,
        schema_write_file,
    ]
)

args = [a for a in sys.argv[1:] if not a.startswith("--")]
user_prompt = " ".join(args) if args else "I dont know what to talk about"
messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("error: missing GEMINI_API_KEY")
    sys.exit(1)


client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

verbose = ("--verbose" in sys.argv)

for _ in range(20):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt),
        )

    for candidate in response.candidates:
        messages.append(candidate.content)



    if response.function_calls:
        
        for fc in response.function_calls:
            function_call_result = call_function(fc, verbose=verbose)
            
            try:
                fr = function_call_result.parts[0].function_response.response
            except Exception:
                if verbose:
                    print(f"[warning] Tool call didn't return expected structure!!")
                fr = {"error": "Malformed tool response"}

            messages.append(
                types.Content(
                    role="user",
                    parts=[types.Part.from_function_response(name=fc.name, response=fr)],
                    )
                )



            if verbose:
                if isinstance(fr, dict):
                    if "result" in fr and fr["result"]:
                        print(fr["result"])
                    elif "error" in fr and fr["error"]:
                        print(fr["error"])
                    else:
                        print(fr)
                else:
                    print(fr)
        continue
        
    else:
        final_text = response.text or "(No final text returned)"
        print("==FINAL RESPONSE==")
        print(final_text)
        print()
        break
    

if "--verbose" in sys.argv and getattr(response, "usage_metadata", None):
    print("=== Token Usage ===")
    print("User prompt:", user_prompt)
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Total tokens:", response.usage_metadata.total_token_count)

def main():
    print("Hello from aiagent!")

    
if __name__ == "__main__":
    main()
from functions.get_files_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
import os

if __name__ == "__main__":
    base = os.path.abspath("calculator")

print(run_python_file(base, "main.py"))
print(run_python_file(base, "main.py", ["3 + 5"]))
print(run_python_file(base, "tests.py"))
print(run_python_file(base, "../main.py"))
print(run_python_file(base, "nonexistent.py"))
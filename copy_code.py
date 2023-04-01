import os
import sys
import pathlib
import pyperclip
import black
import subprocess
import argparse

def format_python_code(code: str) -> str:
    try:
        formatted_code = black.format_str(code, mode=black.FileMode())
        return formatted_code
    except Exception as e:
        print(f"Error formatting Python code: {e}")
        return code

def format_java_code(code: str) -> str:
    #formatter_path = "C:\\Users\\prucs\\Documents\\Scripts\\utils\\google-java-format-1.16.0-all-deps.jar"
    formatter_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "utils/google-java-format-1.16.0-all-deps.jar")
    try:
        result = subprocess.run(
            ["java", "-jar", os.path.abspath(formatter_path), "-"],
            input=code,
            text=True,
            capture_output=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error formatting Java code: {e.stderr}")
        return code
    except Exception as e:
        print(f"Error formatting Java code: {e}")
        return code

def copy_source_code_to_clipboard(folder_path, file_extensions, max_clipboard_size=None):
    source_code_content = ""
    for file_extension in file_extensions:
        for filepath in folder_path.glob(f'**/*.{file_extension}'):
            with open(filepath, 'r') as file:
                code = file.read()
                if file_extension == "java":
                    formatted_code = format_java_code(code)
                elif file_extension == "py":
                    formatted_code = format_python_code(code)
                else:
                    formatted_code = code

                if max_clipboard_size and len(source_code_content + formatted_code + '\n\n') > max_clipboard_size:
                    pyperclip.copy(source_code_content)
                    print("Source code content has been copied to clipboard.")
                    input("Press Enter to copy the next phase to the clipboard...")
                    source_code_content = ""

                source_code_content += formatted_code + '\n\n'

    if source_code_content:
        pyperclip.copy(source_code_content)
        print("Source code content has been copied to clipboard.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Copy source code to clipboard.")
    parser.add_argument("--path", type=str, help="Path to the directory containing source code. Defaults to the current directory.")
    parser.add_argument("--chunk", type=int, help="Maximum number of characters to copy to the clipboard at once. If not provided, copy everything at once.")

    args = parser.parse_args()

    folder_path = pathlib.Path.cwd() if args.path is None else pathlib.Path(args.path)

    if not folder_path.is_dir():
        print("The specified path is not a directory.")
        sys.exit(1)

    file_extensions = ['py', 'js', 'html', 'css', 'java']
    copy_source_code_to_clipboard(folder_path, file_extensions, args.chunk)


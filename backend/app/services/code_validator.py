import os
import re
import subprocess
import tempfile
import ast
from typing import Tuple


def validate_code(file_path: str, code: str) -> Tuple[bool, str]:
    ext = os.path.splitext(file_path)[1].lower()

    if ext in [".js", ".jsx", ".ts", ".tsx"]:
        return _validate_javascript(code, ext)
    elif ext == ".py":
        return _validate_python(code)
    elif ext in [".html", ".css", ".json", ".md", ".yml", ".yaml"]:
        return True, ""
    else:
        return True, ""


def _validate_python(code: str) -> Tuple[bool, str]:
    try:
        ast.parse(code)
        return True, ""
    except SyntaxError as e:
        return False, f"Python syntax error: {e.msg} at line {e.lineno}"


def _validate_javascript(code: str, ext: str) -> Tuple[bool, str]:
    open_braces = code.count("{") - code.count("}")
    open_parens = code.count("(") - code.count(")")
    open_brackets = code.count("[") - code.count("]")

    if open_braces != 0 or open_parens != 0 or open_brackets != 0:
        return False, f"Unbalanced braces/parens/brackets: {open_braces}/{open_parens}/{open_brackets}"

    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=ext, delete=False) as f:
            f.write(code)
            tmp_path = f.name

        result = subprocess.run(
            ["node", "--check", tmp_path],
            capture_output=True,
            text=True,
            timeout=10,
        )
        os.unlink(tmp_path)

        if result.returncode != 0:
            return False, f"Node check error: {result.stderr}"
        return True, ""
    except FileNotFoundError:
        return True, ""
    except Exception as e:
        return False, str(e)

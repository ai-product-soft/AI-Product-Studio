CODE_OUTLINE_PROMPT = """You are a senior full-stack engineer. Given this product idea: "{idea}" and tech stack: {tech_stack}, generate a complete file-by-file outline for a production-ready SaaS starter application.

Output as a markdown list where each line is:
- `path/to/file.ext`: Brief description of what the file contains

Include all necessary files for a working application: backend API, frontend components, database models, config, and documentation.
Do not include explanations outside the list."""

CODE_FILE_PROMPT = """You are a senior full-stack engineer. Given the product idea: "{idea}", generate the complete code for the file: `{file_path}`.

File description: {file_description}

Tech stack: {tech_stack}

Previously generated files summary:
{previous_summaries}

Write complete, production-ready code. Include all imports, types, error handling, and comments. Output only the code, wrapped in triple backticks."""

CODE_CRITIQUE_PROMPT = """You are a code reviewer. The following code for `{file_path}` has this error:

Error: {error_message}

Code:
```
{code}
```

Fix the code and output only the corrected version in triple backticks."""
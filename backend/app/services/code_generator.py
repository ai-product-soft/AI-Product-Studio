import os
import json
import re
from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.llm import llm_chat
from app.services.code_validator import validate_code
from app.prompts.generation import CODE_OUTLINE_PROMPT, CODE_FILE_PROMPT, CODE_CRITIQUE_PROMPT


async def generate_codebase(
    db: AsyncSession,
    project_id: int,
    idea: str,
    plan: Dict,
    output_dir: str,
) -> Dict[str, str]:
    os.makedirs(output_dir, exist_ok=True)

    outline_prompt = CODE_OUTLINE_PROMPT.format(
        idea=idea,
        tech_stack=json.dumps(plan.get("tech_stack", {})),
    )
    messages = [{"role": "user", "content": outline_prompt}]
    outline_response = await llm_chat(messages, temperature=0.5, max_tokens=2048)

    file_entries = _parse_outline(outline_response)
    generated_files: Dict[str, str] = {}

    previous_summaries: List[str] = []
    for entry in file_entries:
        file_path = entry["path"]
        file_desc = entry["description"]

        file_prompt = CODE_FILE_PROMPT.format(
            idea=idea,
            file_path=file_path,
            file_description=file_desc,
            previous_summaries="\n".join(previous_summaries),
            tech_stack=json.dumps(plan.get("tech_stack", {})),
        )

        messages = [{"role": "user", "content": file_prompt}]
        code = await llm_chat(messages, temperature=0.3, max_tokens=4096)

        validated_code = await _critique_and_fix(file_path, code)

        full_path = os.path.join(output_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(validated_code)

        generated_files[file_path] = validated_code
        previous_summaries.append(f"{file_path}: {file_desc}")

    return generated_files


def _parse_outline(outline_text: str) -> List[Dict[str, str]]:
    entries = []
    lines = outline_text.strip().split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        match = re.match(r"^[-*]\s*(?:\[(.*?)\])?\s*(?:`)?(.+?)(?:`)?\s*[-:]\s*(.*)$", line)
        if match:
            entries.append({
                "path": match.group(2).strip(),
                "description": match.group(3).strip() or "No description",
            })
        else:
            parts = line.lstrip("-* ").split(" ", 1)
            if len(parts) == 2 and "." in parts[0]:
                entries.append({"path": parts[0], "description": parts[1]})
    return entries


async def _critique_and_fix(file_path: str, code: str, max_attempts: int = 3) -> str:
    for attempt in range(max_attempts):
        is_valid, error_msg = validate_code(file_path, code)
        if is_valid:
            return code

        critique_prompt = CODE_CRITIQUE_PROMPT.format(
            file_path=file_path,
            code=code,
            error_message=error_msg,
        )
        messages = [{"role": "user", "content": critique_prompt}]
        fixed_code = await llm_chat(messages, temperature=0.2, max_tokens=4096)

        code = _extract_code(fixed_code)

    return code


def _extract_code(text: str) -> str:
    match = re.search(r"```(?:\w+)?\n(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

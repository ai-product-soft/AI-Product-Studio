PLAN_PROMPT = """You are a senior technical product manager and architect. Given the product idea: "{idea}" and this research summary: "{research_summary}", create a detailed project plan.

Output a JSON object with exactly these keys:
- phases (list of objects, each with: phase (string), tasks (list of strings), duration (string, e.g., "2 weeks"))
- tech_stack (object with: frontend (string), backend (string), database (string), ai_models (list of strings), hosting (string))
- monetization_strategy (string, describing pricing model and revenue streams)

Ensure the JSON is valid. No text outside the JSON."""
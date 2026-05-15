RESEARCH_PROMPT = """You are an expert business analyst and market researcher. Given the product idea: "{idea}" and the following search results:

{search_results}

Produce a JSON object with exactly these keys and no other text outside the JSON:
- summary (string, up to 3 sentences describing the market opportunity)
- competitors (list of objects, each with keys: name, url, strength, weakness)
- opportunity_score (integer 0-100)
- key_insights (list of strings, 3-5 actionable insights)

Ensure the JSON is valid and properly formatted."""
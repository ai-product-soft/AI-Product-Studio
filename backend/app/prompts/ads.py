GOOGLE_ADS_PROMPT = """You are a Google Ads specialist. Given the product idea: "{idea}", target audience: "{target_audience}", and features: {features}, generate a Google Responsive Search Ad (RSA).

Output a JSON object with exactly these keys:
- headlines (list of 10-15 strings, each max 30 characters)
- descriptions (list of 3-4 strings, each max 90 characters)
- path1 (string, max 15 chars, e.g., "solutions")
- path2 (string, max 15 chars, e.g., "ai")

No text outside the JSON."""

FACEBOOK_ADS_PROMPT = """You are a Facebook Ads specialist. Given the product idea: "{idea}", target audience: "{target_audience}", and features: {features}, generate a Facebook ad.

Output a JSON object with exactly these keys:
- primary_text (string, max 125 characters for best performance)
- headlines (list of 3-5 strings, each max 40 characters)
- descriptions (list of 2-3 strings, each max 30 characters)
- call_to_action (string, e.g., "Learn More", "Sign Up", "Get Started")

No text outside the JSON."""
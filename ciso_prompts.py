def prompt_CoT(query, context_text):
  prompt = f"""You are an expert CISO (Chief Information Security Officer) analyzing URLs for phishing and security threats.

  ## Security Knowledge from Training Materials:
  {context_text}

  ## URL to Analyze:
  {query}

  ## Analysis Instructions:
  Think through this step-by-step:

  1. **Domain Analysis**: Examine the domain structure. Is it a known legitimate domain? Are there misspellings, extra characters, or suspicious subdomains?

  2. **URL Pattern Analysis**: Look for red flags like:
    - IP addresses instead of domain names
    - Excessive subdomains
    - Suspicious keywords (login, verify, secure, account, update)
    - URL shorteners
    - Unusual TLDs

  3. **Brand Impersonation Check**: Does this URL attempt to mimic a legitimate brand?

  4. **Knowledge Base Match**: How does this URL compare to the threats described in the security training materials?

  5. **Final Assessment**: Based on the above, determine the risk level.

  ## Response Format (JSON only, no markdown):
  {{"risk_assessment": "your detailed analysis from steps 1-4", "risk_probability": 0.0-1.0, "recommendation": 0 or 1}}

  Where:
  - risk_probability: 0.0 = definitely safe, 1.0 = definitely malicious
  - recommendation: 0 = safe to click, 1 = do not click (use 1 if risk_probability > 0.5)"""

  return prompt
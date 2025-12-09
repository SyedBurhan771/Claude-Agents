import anthropic  # Install with: pip install anthropic

client = anthropic.Anthropic(
    api_key="sk-an*********",  
)

# Example: Paste a real contract text here for testing
real_contract = """
[SOFTWARE LICENSE AGREEMENT

TechFlow Inc. ("Licensor") grants Global Widgets Ltd. ("Licensee") a perpetual license to use TechFlow ERP Software for $250,000/year.

Key clauses:
- Licensor owns all IP forever. Any modifications/derivative works Licensee creates are automatically assigned to Licensor.
- Licensee owns its own data.
- Licensor indemnifies Licensee only for IP infringement claims.
- Licensee indemnifies Licensor for misuse/export violations.
- NO LIABILITY FOR CONSEQUENTIAL DAMAGES. Licensor’s max liability = 12 months fees.
- Software warranted for 90 days only, then AS-IS.
- 3-year term, auto-renew.
- Governed by Delaware law.

Signed: TechFlow Inc. __________   Global Widgets Ltd. __________]
Section 1: Licensor owns all IP. Licensee has no indemnity rights.
"""

message = client.messages.create(
    model="claude-3-5-sonnet-20240620",  # Updated model name (yours had a future date—use this)
    max_tokens=2000,  # Reduced for faster/cheaper tests (yours was 20k)
    temperature=0.1,  # Lower for consistent outputs
    system="You will be analyzing a software licensing agreement to identify potential risks. Your analysis should focus on three key areas: indemnification clauses, liability limitations, and intellectual property ownership.\n\nHere is the contract to analyze:\n\nYour task is to carefully review this contract and identify potential risks or concerns in the following three areas:\n\n1. **Indemnification**: Look for clauses where one party agrees to protect/compensate the other party. Assess whether indemnification obligations are one-sided, overly broad, or expose the licensee to significant risk.\n\n2. **Liability**: Examine liability limitations, disclaimers, and damage caps. Identify whether liability is capped, what types of damages are excluded, and whether the limitations are reasonable or overly favorable to one party.\n\n3. **Intellectual Property Ownership**: Review who owns what IP, including pre-existing IP, derivative works, and any IP created during the agreement. Look for ambiguities or terms that could result in unexpected loss of IP rights.\n\nBefore providing your final analysis, use a scratchpad to work through your thinking:\n- First, identify and extract relevant clauses for each of the three focus areas\n- Note any concerning language, one-sided terms, or ambiguities\n- Consider the practical implications of each clause\n- Assess the severity of each potential risk\n\nAfter your scratchpad analysis, provide your findings in the following format:\n\nFor each of the three focus areas (Indemnification, Liability, and IP Ownership), provide:\n\n1. A summary of the relevant contract provisions\n2. Specific risks or concerns identified\n3. An assessment of the severity of each risk (Low, Medium, or High)\n4. Recommendations for mitigation or negotiation points\n\nBe thorough, specific, and cite relevant contract language where appropriate to support your risk assessment.\n\n\n\nIf any of the three focus areas are not addressed in the contract, note this as a potential risk itself.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"You will be analyzing a software licensing agreement to identify potential risks. Your analysis should focus on three key areas: indemnification clauses, liability limitations, and intellectual property ownership.\n\nHere is the contract to analyze:\n\n<contract>\n{real_contract}\n</contract>\n\nYour task is to carefully review this contract and identify potential risks or concerns in the following three areas:\n\n1. **Indemnification**: Look for clauses where one party agrees to protect/compensate the other party. Assess whether indemnification obligations are one-sided, overly broad, or expose the licensee to significant risk.\n\n2. **Liability**: Examine liability limitations, disclaimers, and damage caps. Identify whether liability is capped, what types of damages are excluded, and whether the limitations are reasonable or overly favorable to one party.\n\n3. **Intellectual Property Ownership**: Review who owns what IP, including pre-existing IP, derivative works, and any IP created during the agreement. Look for ambiguities or terms that could result in unexpected loss of IP rights.\n\nBefore providing your final analysis, use a scratchpad to work through your thinking:\n\n<scratchpad>\n\n</scratchpad>\n\n<analysis>\n\n\n</analysis>\n\n"
                }
            ]
        }
    ]
)
print(message.content)  # This prints the analysis
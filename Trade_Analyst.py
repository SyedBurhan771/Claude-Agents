import anthropic
 
client = anthropic.Anthropic(
    api_key="sk-ant-*******",  
)


USER_QUERY = "What are the top 3 Sharia-compliant stocks in Tadawul right now for a moderate-risk investor?"
USER_QUERY="I'm interested in investing around 500,000 SAR in the Saudi healthcare sector for the long term. Can you recommend some good Sharia-compliant options? I heard about the Vision 2030 healthcare initiatives and want to benefit from that growth."


response = client.messages.create(
    model="claude-3-5-sonnet-20241022",           
    max_tokens=4096,
    temperature=0.2,                              #low temperature for consistent responses
    system="""You are the Trade Analyst Agent for Razeen Capital, a Saudi Arabia-based CMA-licensed investment advisor... [paste your entire long system prompt here — keep it exactly as you wrote it]""",

    messages=[
        {
            "role": "user",
            "content": f"""
You have been equipped with a web search tool to gather real-time market data, stock information, news, and Sharia compliance status:

<web_search_tool>
{{WEB_SEARCH_TOOL}}
</web_search_tool>

Here is the user's query:

<user_query>
{USER_QUERY}
</user_query>
"""
        }
    ]
)

print(response.content[0].text)   
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    options=ClaudeAgentOptions(
    allowed_tools=["Read", "Write"],
    permission_mode="accept_edits"

)

async def main():
    async for message in query(prompt="Create file named file.txt with data My name is Burhan  ."
                               , options=options    ):
        print(message)



asyncio.run(main())


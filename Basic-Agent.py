import asyncio
from claude_agent_sdk import query
async def main():
    async for message in query(prompt="hello how are u ."):
        print(message)

asyncio.run(main())


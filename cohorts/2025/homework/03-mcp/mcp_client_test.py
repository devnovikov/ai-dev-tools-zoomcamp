import asyncio
from fastmcp import Client

SERVER_PATH = "main_stdin.py"

async def main():
    async with Client(SERVER_PATH) as client:
        await client.ping()

        tools = await client.list_tools()
        print("Tools:", [t.name for t in tools])

        result = await client.call_tool("scrape", {"url": "https://github.com/alexeygrigorev/minsearch"})
        print("tool [scrape], raw text\n", result.content[0].text)
        print("tool [scrape], characters:", len(result.content[0].text))

        result = await client.call_tool("search", {"query": "demo"})
        print("tool [search], raw text\n", result.content[0].text)
        print("tool [search], characters:", len(result.content[0].text))

if __name__ == "__main__":
    asyncio.run(main())
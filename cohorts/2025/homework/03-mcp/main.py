
import requests
import search_tool
from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool
def scrape(url: str) -> str:
    """Scrape a website and return its content in markdown format using Jina reader."""
    response = requests.get(f"https://r.jina.ai/{url}")
    return response.text

@mcp.tool
def search(query: str) -> str:
    """Search the documentation using minsearch."""
    return search_tool.search(query)

@mcp.tool
def add_repository(repo_url: str) -> str:
    """Add a GitHub repository to the search index.
    Provide the URL to the repository, e.g. https://github.com/owner/repo
    """
    return search_tool.add_repository(repo_url)

if __name__ == "__main__":
    # Initialize with default repo to keep Q6 working
    search_tool.add_repository("https://github.com/jlowin/fastmcp")
    mcp.run(transport="http", host="127.0.0.1", port=8000, path="/mcp")
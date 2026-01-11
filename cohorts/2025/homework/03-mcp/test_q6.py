import search_tool

print("Testing search tool directly...")
try:
    search_tool.add_repository("https://github.com/jlowin/fastmcp")
    results = search_tool.search("demo")
    print("Direct call result:")
    print(results)
except Exception as e:
    print(f"Direct call failed: {e}")

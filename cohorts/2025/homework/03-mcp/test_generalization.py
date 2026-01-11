import search_tool

print("Testing search tool...")

# 1. Search default repo (should be empty initially because we are not running main.py but importing search_tool)
# But we can initialize it manually or just add a new one.
print("Adding default repo...")
search_tool.add_repository("https://github.com/jlowin/fastmcp")
results = search_tool.search("demo")
print(f"Default repo results count: {len(results.splitlines())}")

# 2. Add another repo
print("Adding minsearch repo...")
search_tool.add_repository("https://github.com/alexeygrigorev/minsearch")

# 3. Search for something in minsearch
print("Searching for 'vector'...")
results = search_tool.search("vector")
print("Results for 'vector':")
print(results)

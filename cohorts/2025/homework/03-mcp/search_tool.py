import os
import requests
import zipfile
import minsearch

_documents = []
_index = None

def get_index():
    global _index
    if _index:
        return _index
    # If no index, return empty one or build from empty
    _index = minsearch.Index(
        text_fields=["content"],
        keyword_fields=["filename"]
    )
    return _index

def add_repository(repo_url: str):
    global _documents, _index
    
    # Handle URL to get zip
    # Assumption: repo_url is like https://github.com/owner/repo
    # We want: https://github.com/owner/repo/archive/refs/heads/main.zip
    
    # Remove trailing slash if present
    repo_url = repo_url.rstrip("/")
    
    # Simple heuristic to check if it already points to a zip or archive
    if not repo_url.endswith(".zip"):
        zip_url = f"{repo_url}/archive/refs/heads/main.zip"
    else:
        zip_url = repo_url

    print(f"Downloading {zip_url}...")
    
    # Use a temporary filename or derived one
    # For homework simplicity, we can just use a fixed temp name or derive from repo name
    zip_path = "repo_download.zip"
    
    try:
        response = requests.get(zip_url)
        response.raise_for_status()
        
        with open(zip_path, "wb") as f:
            f.write(response.content)
            
        print("Indexing documents...")
        new_docs = []
        with zipfile.ZipFile(zip_path, 'r') as z:
            for file_info in z.infolist():
                if file_info.filename.endswith(".md") or file_info.filename.endswith(".mdx"):
                    # Remove first directory component (e.g. "repo-main/")
                    parts = file_info.filename.split("/", 1)
                    if len(parts) > 1:
                        filename = parts[1]
                        content = z.read(file_info).decode("utf-8")
                        new_docs.append({"filename": filename, "content": content})
        
        _documents.extend(new_docs)
        
        # Rebuild index
        _index = minsearch.Index(
            text_fields=["content"],
            keyword_fields=["filename"]
        )
        _index.fit(_documents)
        print(f"Added {len(new_docs)} documents. Total: {len(_documents)}")
        return f"Successfully added {len(new_docs)} documents from {repo_url}."
        
    except Exception as e:
        print(f"Error adding repository: {e}")
        return f"Error adding repository: {e}"
    finally:
        if os.path.exists(zip_path):
            os.remove(zip_path)

def search(query: str) -> str:
    """Search the documentation using minsearch."""
    idx = get_index()
    # Handle case where fit hasn't been called yet (if minsearch supports it, otherwise check docs)
    if not _documents:
        return "No documents indexed. Please add a repository first."
        
    results = idx.search(query, boost_dict={}, num_results=5)
    return "\n".join([f"- {res['filename']}" for res in results])

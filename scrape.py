import os
import re
import urllib.request
import urllib.parse

BASE_URL = "https://marceneiropro.site"
DOWNLOADED = set(["/assets/index-DtivU3Fh.js", "/assets/index-I35ezpeo.css"])
TO_DOWNLOAD = set(["/assets/index-DtivU3Fh.js", "/assets/index-I35ezpeo.css"])

def download_file(path):
    url = urllib.parse.urljoin(BASE_URL, path)
    if not path.startswith("/"):
        path = "/" + path
    local_path = "." + path
    local_dir = os.path.dirname(local_path)
    if not os.path.exists(local_dir):
        os.makedirs(local_dir, exist_ok=True)
    
    print(f"Downloading {url} to {local_path}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            content = response.read()
            with open(local_path, "wb") as f:
                f.write(content)
            return content
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

def extract_paths(content):
    # Search for patterns like "assets/something.ext" or "/assets/something.ext"
    paths = set()
    text = content.decode('utf-8', errors='ignore')
    
    # Matches strings that might be assets
    # Common Vite patterns: "assets/filename-[hash].ext"
    matches = re.findall(r'(?:/)?assets/[a-zA-Z0-9_.-]+', text)
    for match in matches:
        if not match.startswith("/"):
            match = "/" + match
        paths.add(match)
        
    # Also look for background-image: url("...") or src="..." in code
    return paths

def main():
    while TO_DOWNLOAD:
        path = TO_DOWNLOAD.pop()
        content = download_file(path)
        if content:
            # Only try to extract paths from text files (JS, CSS)
            if path.endswith('.js') or path.endswith('.css'):
                new_paths = extract_paths(content)
                for p in new_paths:
                    if p not in DOWNLOADED:
                        DOWNLOADED.add(p)
                        TO_DOWNLOAD.add(p)

if __name__ == "__main__":
    # Also parse index.html for possible paths
    try:
        with open("index.html", "rb") as f:
            content = f.read()
            new_paths = extract_paths(content)
            for p in new_paths:
                if p not in DOWNLOADED:
                    DOWNLOADED.add(p)
                    TO_DOWNLOAD.add(p)
    except:
        pass
    main()

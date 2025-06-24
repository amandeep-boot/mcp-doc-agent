import re
import subprocess
import shutil
import os

def extract_github_slug(url: str) -> str | None:
    """
    Extracts the GitHub slug (owner/repo) from a GitHub URL.
    Returns the slug as a string, or None if the URL is invalid.
    """
    pattern = r"github\.com[:/]+([\w.-]+)/([\w.-]+)(?:[/?#]|$)"
    match = re.search(pattern, url)
    if match:
        owner, repo = match.group(1), match.group(2)
        return f"{owner}/{repo}"
    return None

def download_github_markdown_docs(slug: str, output_dir: str = "./docs") -> str | bool:
    """
    Downloads markdown documentation files from a GitHub repository using the tfw.in deepwiki tool.
    The slug should be in the format 'owner/repo'.
    Returns the output_dir path as a string if successful, False otherwise.
    """
    NPX_PATH = shutil.which("npx") or shutil.which("npx.cmd")
    if not NPX_PATH:
        print("Error: 'npx' is not installed or not found in PATH.")
        return False
    if not slug or '/' not in slug:
        print("Invalid slug format. Expected 'owner/repo'.")
        return False
    cmd = [
        NPX_PATH, "@tfw.in/tools", "deepwiki", slug, "--output", output_dir
    ]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        return output_dir
    except subprocess.CalledProcessError as e:
        print(f"Error downloading docs: {e.stderr}")
        return "Deepwiki documentation does not exist." 

def generate_summary_md(docs_dir: str = "./docs") -> str:
    """
    Generates a SUMMARY.md file in the given directory, listing all markdown files (except SUMMARY.md itself).
    Handles the case where docs_dir contains a single subdirectory (the repo name) with the markdown files inside.
    Returns the path to the generated SUMMARY.md.
    """
    # Check if docs_dir contains a single subdirectory
    entries = [entry for entry in os.listdir(docs_dir) if not entry.startswith('.')]
    subdir_path = docs_dir
    if len(entries) == 1 and os.path.isdir(os.path.join(docs_dir, entries[0])):
        subdir_path = os.path.join(docs_dir, entries[0])
    md_files = [f for f in os.listdir(subdir_path) if f.endswith('.md') and f.lower() != 'summary.md']
    md_files.sort()
    summary_path = os.path.join(subdir_path, "SUMMARY.md")
    with open(summary_path, "w", encoding="utf-8") as summary:
        summary.write("# Summary\n\n")
        for f in md_files:
            title = f.replace("-", " ").replace("_", " ").replace(".md", "").title()
            summary.write(f"* [{title}]({f})\n")
    return summary_path

def build_gitbook(docs_dir: str) -> str | bool:
    """
    Runs 'npx gitbook-cli@2.3.2 build' on the given directory to generate the static site.
    Returns the path to the generated _book directory if successful, False otherwise.
    Adds detailed logging for debugging.
    """
    NPX_PATH = shutil.which("npx") or shutil.which("npx.cmd")
    if not NPX_PATH:
        print("Error: 'npx' is not installed or not found in PATH.")
        return False

    cmd = [NPX_PATH, "gitbook-cli@2.3.2", "build", docs_dir]
    print(f"Running command: {' '.join(cmd)}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Target docs_dir: {docs_dir}")

    try:
        result = subprocess.run(
            cmd,
            check=True, capture_output=True, text=True
        )
        print("STDOUT:")
        print(result.stdout)
        print("STDERR:")
        print(result.stderr)
        book_dir = os.path.join(docs_dir, "_book")
        if os.path.isdir(book_dir):
            return book_dir
        else:
            print("Build completed, but _book directory not found.")
            return False
    except subprocess.CalledProcessError as e:
        print("Error building GitBook:")
        print("STDOUT:")
        print(e.stdout)
        print("STDERR:")
        print(e.stderr)
        return False

# print(extract_github_slug("github.com/microsoft/vscode"))  

if __name__ == "__main__":
    # Test values
    test_url = "https://github.com/microsoft/vscode"
    slug = extract_github_slug(test_url)
    print(f"Extracted slug: {slug}")
    if slug:
        docs_dir = download_github_markdown_docs(slug, "./docs_test")
        print(f"Download result: {docs_dir}")
        if isinstance(docs_dir, str):
            summary_path = generate_summary_md(docs_dir)
            print(f"SUMMARY.md generated at: {summary_path}")
            # Determine the correct directory for gitbook build
            entries = [entry for entry in os.listdir(docs_dir) if not entry.startswith('.')]
            build_dir = docs_dir
            if len(entries) == 1 and os.path.isdir(os.path.join(docs_dir, entries[0])):
                build_dir = os.path.join(docs_dir, entries[0])
            book_dir = build_gitbook(build_dir)
            print(f"GitBook static site generated at: {book_dir}")
        else:
            print("Failed to download markdown docs.")
    else:
        print("Failed to extract slug.")

print(shutil.which("npx"))



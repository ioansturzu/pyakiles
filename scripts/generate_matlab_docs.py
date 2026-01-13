import os
from pathlib import Path

def generate_matlab_docs():
    matlab_root = Path("matlab_port/+akiles2d")
    docs_root = Path("docs/matlab_api")
    docs_root.mkdir(parents=True, exist_ok=True)
    
    # Create index
    index_content = ["# MATLAB API Reference\n\n"]
    
    for root, _, files in os.walk(matlab_root):
        rel_path = Path(root).relative_to(matlab_root)
        
        # Skip package generic files if preferred, but usually we want .m files
        m_files = sorted([f for f in files if f.endswith(".m")])
        if not m_files:
            continue
            
        group_name = str(rel_path).replace(os.sep, ".")
        if group_name == ".":
            group_name = "akiles2d (Root)"
        
        index_content.append(f"## {group_name}\n")
        
        for m_file in m_files:
            file_path = Path(root) / m_file
            # Create a dedicated markdown page for each file or section? 
            # Let's put them all in one big page per directory or just one page.
            # User wants "available in API reference". Let's create a page per file or use snippets.
            # Using snippets is cleaner.
            
            # The path must be relative to the document location (docs/)
            # snippet_path is currently absolute or relative to CWD.
            # We want something like ../matlab_port/...
            
            # file_path is absolute or relative to where script run.
            
            # rel_path is relative from matlab_root ("+akiles2d")
            # We want path from project root: matlab_port/+akiles2d/...
            project_rel_path = matlab_root / rel_path / m_file
            
            # Then relative to docs/: ../matlab_port/...
            snippet_path = Path("..") / project_rel_path
            
            # Use Sphinx directive for including file content
            # highlight-language: matlab
            
            index_content.append(f"### {m_file}\n\n")
            index_content.append("**Source Code**\n\n")
            index_content.append(f"```{{literalinclude}} {snippet_path}\n:language: matlab\n```\n\n")

    with open("docs/matlab_reference.md", "w") as f:
        f.write("\n".join(index_content))

if __name__ == "__main__":
    generate_matlab_docs()

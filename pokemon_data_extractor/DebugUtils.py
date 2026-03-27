def save_html_locally(html_content, filename="debug_file.html"):
    """Saves raw HTML string to a file for local testing."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"--- Cached local copy to {filename} ---")
    except Exception as e:
        print(f"Error saving HTML: {e}")
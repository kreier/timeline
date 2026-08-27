from pathlib import Path

# Always relative to this Python file, not the current working directory.
STATUS_DIR = Path(__file__).resolve().parent

INDEX_FILE = STATUS_DIR / "index.md"
README_FILE = STATUS_DIR / "README.md"


def generate_content():
    """
    Generate the actual status information.

    Return the Markdown body without YAML front matter.
    """

    # TODO: Replace this with your actual status-generation code.
    return """# Timeline status

This page is automatically generated.

Everything is currently up to date.
"""


def generate_index(content):
    """Generate the Jekyll page."""

    text = f"""---
layout: default
title: Timeline status
---

{content}
"""

    INDEX_FILE.write_text(text, encoding="utf-8")


def generate_readme(content):
    """Generate the GitHub README."""

    text = f"""{content}
"""

    README_FILE.write_text(text, encoding="utf-8")


def main():
    content = generate_content()

    generate_index(content)
    generate_readme(content)

    print(f"Generated {INDEX_FILE}")
    print(f"Generated {README_FILE}")


if __name__ == "__main__":
    main()

# Create status/index.md
# Create status/timeline24.md
# Create status/timeline25.md

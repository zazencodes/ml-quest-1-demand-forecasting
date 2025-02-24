import json
import shutil
from pathlib import Path

MARKDOWN_PREVIEW_LINES = 20


def load_lesson_hashes(filepath="lesson_hashes.json"):
    """Load and return the lesson hash mappings from JSON file"""
    with open(filepath, "r") as f:
        return json.load(f)


def setup_directories():
    """Create clean output directories"""
    if Path("site-content").exists():
        shutil.rmtree("site-content")
    Path("site-content/full").mkdir(parents=True, exist_ok=True)
    Path("site-content/preview").mkdir(parents=True, exist_ok=True)


def create_preview_content(content_lines):
    """
    Create preview version ensuring math blocks aren't split

    Args:
        content_lines (list): List of lines from the markdown file

    Returns:
        list: Preview lines that don't break math blocks
    """
    preview_lines = []
    in_math_block = False

    for i, line in enumerate(content_lines):
        # If we've hit our preview limit and we're not in a math block
        if i >= MARKDOWN_PREVIEW_LINES and not in_math_block:
            break

        # Check for math block markers
        if line.strip() == "$$":
            in_math_block = not in_math_block

        preview_lines.append(line)

    return preview_lines


def process_single_lesson(source_path, full_output, preview_output):
    """
    Process a single lesson file
    Args:
        source_path (Path): Path to source markdown file
        full_output (Path): Path for full content output
        preview_output (Path): Path for preview content output
    """
    # Copy full content
    shutil.copy2(source_path, full_output)

    # Create preview version
    with open(source_path, "r", encoding="utf-8") as source:
        content = source.readlines()
        preview_content = create_preview_content(content)

    # Write preview content
    with open(preview_output, "w", encoding="utf-8") as preview:
        preview.writelines(preview_content)


def create_content_bundle():
    """Bundle course content with full and preview versions"""
    lesson_hashes = load_lesson_hashes()
    setup_directories()

    # Process each lesson
    for filepath, hash_id in lesson_hashes.items():
        source_path = Path("content") / f"{filepath}.md"
        full_output = Path("site-content/full") / f"{hash_id}.md"
        preview_output = Path("site-content/preview") / f"{hash_id}.md"

        try:
            process_single_lesson(source_path, full_output, preview_output)
            print(f"Processed {filepath} -> {hash_id}.md")

        except FileNotFoundError:
            print(f"Warning: Could not find source file: {source_path}")
        except Exception as e:
            print(f"Error processing {filepath}: {str(e)}")


def main():
    print("Starting course content bundling...")
    create_content_bundle()
    print("Content bundling complete!")


if __name__ == "__main__":
    main()

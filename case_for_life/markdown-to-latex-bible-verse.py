#!/bin/python3 

import re

def read_markdown_file(file_path):
    """Read content from a markdown file."""
    with open(file_path, "r") as file:
        return file.read()

def parse_verses(markdown_text):
    # Pattern to capture verses with tags like [!bible] [Reference - NASB](link)
    verse_pattern = re.compile(
        r'> \[!bible\] \[(.*?) - NASB\]\((.*?)\)\n((?:> \d+\. .*\n)+)',
        re.MULTILINE
    )
    
    verses = []
    for match in verse_pattern.finditer(markdown_text):
        reference = match.group(1)
        content = match.group(3)
        
        # Process the verse content
        verses.append(format_verse(reference, content))
    
    return verses

def format_verse(reference, content):
    # Pattern to capture each verse line (e.g., > 18. verse text)
    line_pattern = re.compile(r'> (\d+)\. (.+)')
    
    formatted_lines = []
    for line_match in line_pattern.finditer(content):
        verse_number = line_match.group(1)
        verse_text = line_match.group(2)
        formatted_lines.append(f"\\vs{{{verse_number}}}{verse_text}")

    formatted_content = "\n    ".join(formatted_lines)
    
    # Structure the verse in LaTeX format
    latex_verse = f"\\begin{{scripture}}[{reference}]\n    {formatted_content}\n\\end{{scripture}}"
    
    return latex_verse

def save_to_latex(verses, output_file="output.tex"):
    with open(output_file, "w") as file:
        for verse in verses:
            file.write(verse + "\n\n")

def main(input_file, output_file="output.tex"):
    # Read the markdown content from the file
    markdown_content = read_markdown_file(input_file)
    # Parse verses from the markdown content
    parsed_verses = parse_verses(markdown_content)
    # Save the formatted verses to a LaTeX file
    save_to_latex(parsed_verses, output_file)
    print(f"Verses have been saved to {output_file}")

# Example usage:
# Replace 'input.md' with the path to your markdown file
main("input.md")

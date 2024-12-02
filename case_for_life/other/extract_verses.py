import json
import sys
import os

def generate_verse_text(book, chapter, verse_index, verse_text):
    """
    Generate LaTeX-formatted string for a single verse with a short label.
    """
    # Create a short label based on book abbreviation, chapter, and verse
    short_label = f"{book[`name`].split()[0][:3]}{chapter + 1}:{verse_index + 1}".replace(" ", "")
    
    # Output only the short label
    return f"\\textbf{{{book[`name`]} ({book[`abbrev`].upper()}) {chapter + 1}:{verse_index + 1} (NASB)}} {verse_text}\n\\label{{{short_label}}}\n\n"

def main(json_filename):
    # Load the NASB Bible JSON data
    with open(json_filename, "r") as file:
        bible_data = json.load(file)

    # Define the output .tex file name based on the JSON file name
    tex_filename = os.path.splitext(json_filename)[0] + ".tex"

    # Open the output .tex file for writing
    with open(tex_filename, "w") as tex_file:
        # Write the start document
        tex_file.write("\\documentclass{article}\n\\begin{document}\n\n")
        
        # Iterate through each book in the Bible
        for book in bible_data:
            # Iterate through each chapter in the book
            for chapter_index, chapter in enumerate(book["chapters"]):
                # Iterate through each verse in the chapter
                for verse_index, verse_text in enumerate(chapter):
                    # Generate LaTeX-formatted verse text with short label only
                    formatted_verse = generate_verse_text(book, chapter_index, verse_index, verse_text)
                    # Write to the output file
                    tex_file.write(formatted_verse)

        # Write the end document
        tex_file.write("\\end{document}\n")

    print(f"All verses have been written to {tex_filename} with short labels only")

# Run the script with the JSON file provided as a command-line argument
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_short_reference_nasb_verses.py <nasb_bible.json>")
    else:
        main(sys.argv[1])

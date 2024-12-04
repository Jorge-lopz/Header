import os
import re
import sys
import unidecode
from datetime import datetime

# TODO -> Make it work with virtual environments (.venv at least)
# TODO -> Make it add a different header depending on the file type (with config file)

HEADER_START_END = "# --------------------------------------------------------------------------- #"
HEADER_BASE = "#                                                                             #"
HEADER_PATTERN = re.compile(re.escape(HEADER_START_END) + r".*?" + re.escape(HEADER_START_END) + "\n", re.DOTALL)

# Define the header icons (https://patorjk.com/software/taag/#p=display&f=Alligator)

AD_ICON = [  # <Acceso a Datos>
    "         ::::     :::::::: ",
    "       ++: :+:   :+:   :++:",
    "     #:+   +:+  +:+    +:+ ",
    "   +#++:++#++: +#:    +:+  ",
    "  +#+     +#+ ##+    +#+   ",
    " ##+     #+# ###    ##+    ",
    "###     ### ########+      "
]

AC_ICON = [  # <Advent of Code>
    "         ::::      ::::::::",
    "       ++: :+:   :+:    :+:",
    "     #:+   +:+  +:+        ",
    "   +#++:++#++: +#+         ",
    "  +#+     +#+ +#+          ",
    " ##+     #+# #+#    #+#    ",
    "###     ###  ########      "
]
AUTHOR = "Jorge Lopez Puebla"
DATE = datetime.now().strftime('%d/%m/%Y')
MAX_LEN = 77

def generate_header(file, project):
    # Truncate filename, project, and other fields to fit within the width
    file = file[:30]
    project = project[:21]

    # Define the header icon
    HEADER_ICON = AC_ICON if project.upper().replace(" ", "") == "ADVENTOFCODE" else AD_ICON

    # Define the header structure
    header_lines = [
        HEADER_START_END,
        HEADER_BASE,
        f"#     {file + (' ' * (MAX_LEN - len(file) - 39)) + HEADER_ICON[0]}       #",
        f"#     {(' ' * (MAX_LEN - 39)) + HEADER_ICON[1]}       #",
        f"#     PROJECT: {project + (' ' * (MAX_LEN - len(project) - 48)) + HEADER_ICON[2]}       #",
        f"#     {(' ' * (MAX_LEN - 39)) + HEADER_ICON[3]}       #",
        f"#     {(' ' * (MAX_LEN - 39)) + HEADER_ICON[4]}       #",
        f"#     AUTHOR: {AUTHOR + (' ' * (MAX_LEN - len(AUTHOR) - 47)) + HEADER_ICON[5]}       #",
        f"#     LAST UPDATE: {DATE + (' ' * (MAX_LEN - len(DATE) - 52)) + HEADER_ICON[6]}       #",
        HEADER_BASE,
        HEADER_START_END
    ]

    header = ""
    for i, line in enumerate(header_lines):
        header += line + "\n"

    return header

def process_file(file_path, project):
    if project is None:
        project = os.path.basename(os.path.dirname(file_path))
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    header = generate_header(os.path.basename(file_path), project)

    # Replace the header if it exists, or add a new one
    if HEADER_PATTERN.search(content):
        content = HEADER_PATTERN.sub(header, content)
    else:
        content = header + "\n" + content

    # Write the updated content back to the file
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Processed {file_path}")
    except PermissionError:
        print(f"Permission denied ({file_path})")
        exit(-1)

def process_directory(directory, project=None):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                process_file(os.path.join(root, file), project)

def main():
    if len(sys.argv) > 2:
        # If filename and project name are passed as arguments (for external tool use)
        filename = sys.argv[1]
        project = unidecode.unidecode(sys.argv[2])
        process_file(filename, project)
    elif len(sys.argv) > 1:
        # If project name is passed as argument (for external tool use)
        current_dir = os.getcwd()
        project = sys.argv[1]
        process_directory(current_dir, project)
    else:
        # If no arguments are passed, process all .py files in the current directory and subdirectories
        current_dir = os.getcwd()
        process_directory(current_dir)

if __name__ == "__main__":
    main()

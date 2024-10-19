from pathlib import Path
import sys
import subprocess

TITLE = ""
SRC = Path("../src")
TGT = Path("../docs")
INDEX = Path('index_template.html')

def call_command(command):
    """Calls the specified command-line command.

    Args:
        command (str): The command to be executed.

    Returns:
        subprocess.CompletedProcess: A CompletedProcess object representing the
        execution of the command.
    """

    try:
        subprocess.run(command, shell=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None

homilies = []
for f in SRC.glob('*.md'):
    n = f.name.replace('.md', '.html')
    homilies.append(n)
    call_command(f"pandoc -f markdown -t html -o {TGT / Path(n)} {f} --template template.html --metadata title='{TITLE}'")

links = [f'<li><a href="./{x}">{x.replace(".html", "").replace("_", " ")}</a></li>' for x in homilies]
Path(TGT / Path('index.html')).write_text(INDEX.read_text().replace('$body$', '\n'.join(links)).replace('$title$', TITLE))

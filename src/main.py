from dotenv import load_dotenv
import sys

load_dotenv()

from cli.cli import main

# bugs out if no arguments are given
if len(sys.argv) < 2:
    sys.argv.append('-h')

main()
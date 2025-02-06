#!/usr/bin/env python
import sys
import subprocess

COMMANDS = ["run", "test"]

def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} [{'/'.join(COMMANDS)}]")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "run":
        # Run the FastAPI app with uvicorn
        subprocess.run(["uvicorn", "application.main:app", "--host", "0.0.0.0", "--port", "8000"])
    elif command == "test":
        # Run pytest
        subprocess.run(["pytest", "--maxfail=1", "--disable-warnings", "-q"])
    else:
        print(f"Unknown command: {command}. Available commands: {COMMANDS}")

if __name__ == "__main__":
    main()

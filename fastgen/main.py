import argparse
import sys
from rich.console import Console
from fastgen.core.cli_manager import display_help
from fastgen.core.project_manager import create_project_mode
from fastgen.core.template_manager import display_templates

console = Console()

def main():
    """Main CLI function for handling commands."""
    try:
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("command", nargs="?", help="Command to execute")
        args = parser.parse_args()

        commands = {
            "create": create_project_mode,
            "list": display_templates,
            "help": display_help,
        }

        if not args.command or args.command in ["--help", "-h"]:
            display_help()
            return

        if args.command in commands:
            commands[args.command]()
        else:
            console.print(f"[red]❌ Error: Unknown command '{args.command}'. Use 'poetry run fastgen help' to see available commands.[/red]")

    except KeyboardInterrupt:
        console.print("\n\n[bold red]👋 Goodbye! Exiting CLI.[/bold red]")
        sys.exit(0)

if __name__ == "__main__":
    main()

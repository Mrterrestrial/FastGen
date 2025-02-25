import argparse
import os
import re
import sys
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table

from fastgen.core import setup_project

console = Console()

# Default values for project creation (like Poetry)
DEFAULTS = {
    "project_name": "my_project",
    "use_git": True,
}

def fetch_available_templates():
    """Fetch available project templates dynamically from the 'templates/' directory."""
    template_dir = os.path.join(os.path.dirname(__file__), "../templates")
    templates = [f.replace(".yaml", "") for f in os.listdir(template_dir) if f.endswith(".yaml")]
    return templates if templates else ["(No templates found)"]

def display_templates():
    """Display available project templates in a table format."""
    console.print("\n[bold cyan]📜 Available Project Templates[/bold cyan]\n")
    templates = fetch_available_templates()
    
    if "(No templates found)" in templates:
        console.print("[red]❌ No templates found. Please add some in the 'templates/' directory.[/red]")
        return

    table = Table(title="Project Templates", show_header=True, header_style="bold green")
    table.add_column("Template Name", justify="left", style="yellow")
    
    for template in templates:
        table.add_row(template)

    console.print(table)

def validate_project_name(name):
    """Ensure project name is valid (no spaces or special characters)."""
    if not re.match("^[a-zA-Z0-9_-]+$", name):
        console.print("[red]❌ Invalid project name! Use only letters, numbers, '_' or '-'.[/red]")
        return False
    return True

def validate_project_type(project_type):
    """Ensure project type is valid."""
    available_templates = fetch_available_templates()
    if project_type not in available_templates:
        console.print("[red]❌ Invalid project type! Please select from available templates.[/red]")
        console.print("[yellow]Available templates:[/yellow]")
        for template in available_templates:
            console.print(f"    ● {template}")
        return False
    return True

def get_input_with_default(prompt_text, default_value=None, choices=None):
    """
    Prompt the user for input with an optional default value.
    If no default is provided, the user is required to enter a value.
    """
    while True:
        try:
            if default_value is not None:
                return Prompt.ask(f"[bold yellow]{prompt_text}[/bold yellow] [default: {default_value}]", 
                                  choices=choices, default=default_value)
            else:
                user_input = Prompt.ask(f"[bold yellow]{prompt_text} (Required)[/bold yellow]", choices=choices).strip()
                if user_input:
                    return user_input  # Accept only non-empty input
                console.print("[red]❌ This field is required! Please enter a valid value.[/red]")  # Show error and retry
        except KeyboardInterrupt:
            console.print("\n\n[bold red]👋 Goodbye!.[/bold red]")
            sys.exit(0)

def create_project_mode():
    try:
        console.print("[bold cyan]🔹 Starting Interactive Project Creation...[/bold cyan]")

        # Fetch and display available templates
        available_templates = fetch_available_templates()
        
        if "(No templates found)" in available_templates:
            console.print("[red]❌ No templates available! Please add some to the 'templates/' directory.[/red]")
            return

        display_templates()

        # Optional Features
        while True:
            # Select Project Type 
            project_type = get_input_with_default("Select a project type")
            if validate_project_type(project_type):
                break
        while True:
            #Enter Project Name
            project_name = get_input_with_default("Enter the project name", DEFAULTS["project_name"])
            if validate_project_name(project_name):
                break

        # Optional Features with Defaults
        use_git = Confirm.ask(f"[bold green]📌 Initialize a Git repository?[/bold green]", default=DEFAULTS["use_git"])

        console.print("\n[bold blue]🛠 Generating your project...[/bold blue]")
        console.print(f"📂 Project Name: [green]{project_name}[/green]")
        console.print(f"📦 Template: [yellow]{project_type}[/yellow]")
        console.print(f"🔗 Git Initialized: [cyan]{'Yes' if use_git else 'No'}[/cyan]")

        # Run project creation command
        setup_project.run(project_type, project_name, use_git)


    except KeyboardInterrupt:
        console.print("\n\n[bold red]👋 Goodbye! Project creation canceled.[/bold red]")
        sys.exit(0)


def display_help():
    """Display a well-formatted command list using Rich."""
    console.print("\n[bold cyan]🚀 Generator Your Project Fast[/bold cyan]\n")
    
    table = Table(title="Available Commands", show_header=True, header_style="bold green")
    table.add_column("Command", justify="left", style="yellow", no_wrap=True)
    table.add_column("Description", justify="left", style="white")

    commands = [
        ("create", "Create a new project interactively"),
        ("list", "List available project templates")
    ]

    for command, description in commands:
        table.add_row(command, description)

    console.print(table)
    console.print("[bold cyan]Usage Example:[/bold cyan] poetry run fastgen create\n")

def main():
    """Main function to handle command-line arguments with improved help menu and exit command."""
    try:
        parser = argparse.ArgumentParser(add_help=False)  # Disable default help to use custom
        parser.add_argument("command", nargs="?", help="Command to execute")
        args = parser.parse_args()

        commands = {
            "create": create_project_mode,
            "list": display_templates
        }

        if not args.command or args.command in ["help", "--help", "-h"]:
            display_help()
            return

        if args.command in commands:
            commands[args.command]()
        else:
            console.print(f"[red]❌ Error: Unknown command '{args.command}'. Use 'fastgen help' to see available commands.[/red]")

    except KeyboardInterrupt:
        console.print("\n\n[bold red]👋 Goodbye! Exiting CLI.[/bold red]")
        sys.exit(0)

if __name__ == "__main__":
    main()
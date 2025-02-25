import re
import sys
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from fastgen.core.template_manager import fetch_available_templates

console = Console()


def get_input_with_default(prompt_text, default_value=None):
    """
    Prompt the user for input with an optional default value.
    If no default is provided, the user is required to enter a value.
    """
    while True:
        try:
            # Format the prompt message
            prompt_message = f"[bold yellow]{prompt_text}[/bold yellow]"
            if default_value is None:
                prompt_message += f" [default: {default_value}]"

            user_input = Prompt.ask(prompt_message, default=str(default_value)).strip()

            # If user presses Enter without input, return the default
            if user_input == "" and default_value is not None:
                return default_value  

            # Return valid user input
            if user_input:
                return user_input  

            console.print("[red]❌ This field is required! Please enter a valid value.[/red]")

        except KeyboardInterrupt:
            console.print("\n\n[bold red]👋 Goodbye!.[/bold red]")
            sys.exit(0)


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

def display_help():
    """Display a well-formatted command list using Rich."""
    console.print("\n[bold cyan]🚀 Fastgen - Generate Your Project Quickly[/bold cyan]\n")
    
    table = Table(title="Available Commands", show_header=True, header_style="bold green")
    table.add_column("Command", justify="left", style="yellow", no_wrap=True)
    table.add_column("Description", justify="left", style="white")

    commands = [
        ("create", "Create a new project interactively"),
        ("list", "List available project templates"),
    ]

    for command, description in commands:
        table.add_row(command, description)

    console.print(table)
    console.print("[bold cyan]Usage Example:[/bold cyan] poetry run fastgen create\n")

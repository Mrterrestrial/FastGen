import os
import yaml
from rich.console import Console

console = Console()

TEMPLATE_DIR = "templates"

def list_templates():
    """
    Lists all available YAML templates in the templates directory.
    """
    console.print("[bold cyan]🔹 Available Templates:[/bold cyan]")
    templates = [f for f in os.listdir(TEMPLATE_DIR) if f.endswith(".yaml")]

    if not os.path.exists(TEMPLATE_DIR):
        console.print(f"[bold red]❌ No templates found in '{TEMPLATE_DIR}' directory.[/bold red]")
        return []

    for template in templates:
        console.print(f"[bold yellow] - {template.replace('.yaml', '')}[/bold yellow]")
    
    return templates

def load_template(template_name):
    """
    Loads a YAML template from the templates directory.

    :param template_name: Name of the template (without .yaml)
    :return: Template dictionary if successful, None if failed
    """
    template_file = os.path.join(TEMPLATE_DIR, f"{template_name}.yaml")

    if not os.path.exists(template_file):
        console.print(f"[bold red]❌ Error: Template '{template_name}.yaml' not found.[/bold red]")
        return None

    try:
        with open(template_file, "r", encoding="utf-8") as f:
            template = yaml.safe_load(f)
            console.print(f"[bold green]✅ Successfully loaded template: {template_name}[/bold green]")
            return template
    except yaml.YAMLError as e:
        console.print(f"[bold red]❌ Error loading YAML template: {e}[/bold red]")
        console.print("[bold yellow]💡 Tip: Check if your YAML file is formatted correctly.[/bold yellow]")
        return None

import os
import yaml
from rich.console import Console
from rich.table import Table

console = Console()

TEMPLATE_DIR = "templates"

def display_templates():
    """
    Displays available project templates in a well-formatted table.
    """    
    templates = fetch_available_templates()
    
    #check if templetes is empty list 
    if templates == []:
        return

    if "(No templates found)" in templates:
        console.print("[red]❌ No templates found. Please add some to the 'templates/' directory.[/red]")
        return

    table = Table(title="Project Templates", show_header=True, header_style="bold green")
    table.add_column("Template Name", justify="left", style="yellow")
    
    for template in templates:
        table.add_row(template)
        
    console.print("\n[bold cyan]📜 Available Project Templates[/bold cyan]\n")
    console.print(table)


def fetch_available_templates():
    """
    Fetches all available project templates dynamically from the 'templates/' directory.
    """
    if not os.path.exists(TEMPLATE_DIR):
        console.print(f"[bold red]❌ Error: Templates directory '{TEMPLATE_DIR}' does not exist.[/bold red]")
        return 

    templates = [f.replace(".yaml", "") for f in os.listdir(TEMPLATE_DIR) if f.endswith(".yaml")]
    return templates if templates else ["(No templates found)"]


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




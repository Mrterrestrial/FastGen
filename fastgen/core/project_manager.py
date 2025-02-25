import os
import shutil
import sys
from rich.console import Console
from rich.prompt import Confirm
from fastgen.core.template_manager import load_template, fetch_available_templates
from fastgen.core.cli_manager import get_input_with_default, validate_project_name, validate_project_type

console = Console()

GENERATED_PROJECTS_DIR = "generated_projects"
DEFAULTS = {
    "project_type": "basic_python",
    "project_name": "my_project",
    "use_git": True,
}



def delete_project_directory(project_path):
    """Deletes the entire project directory if project creation fails."""
    if os.path.exists(project_path):
        shutil.rmtree(project_path)
        console.print(f"[bold red]🗑️ Removed incomplete project: {project_path}[/bold red]")
    else:
        console.print(f"[bold yellow]⚠️ Warning: Project directory '{project_path}' does not exist, skipping deletion.[/bold yellow]")

def create_project(project_type, project_name, use_git):
    """
    Creates a project structure based on the selected template.

    :param project_type: Type of project (e.g., fastapi, django, react)
    :param project_name: Name of the project folder
    :param use_git: Boolean to initialize Git repository
    """
    try:
        console.print(f"[bold cyan]🔹 Creating project: {project_name}[/bold cyan]")

        # Load the template
        template = load_template(project_type)
        if not template:
            return

        # Define project path
        project_path = os.path.join(GENERATED_PROJECTS_DIR, project_name)
        os.makedirs(project_path, exist_ok=True)

        # Create necessary directories
        for directory in template.get("directories", []):
            dir_path = os.path.join(project_path, directory)
            os.makedirs(dir_path, exist_ok=True)
            console.print(f"[bold yellow]📁 Created directory: {dir_path}[/bold yellow]")

        # Create and write files
        for file_path, content in template.get("files", {}).items():
            file_full_path = os.path.join(project_path, file_path)
            file_dir = os.path.dirname(file_full_path)

            # Ensure the directory exists
            if not os.path.exists(file_dir):
                os.makedirs(file_dir, exist_ok=True)

            # Write file content
            with open(file_full_path, "w", encoding="utf-8") as file:
                file.write(content)

            console.print(f"[bold green]📝 Created file: {file_full_path}[/bold green]")

        # Initialize Git repository if selected
        if use_git:
            os.system(f"cd {project_path} && git init")
            console.print(f"[bold green]🔧 Initialized Git repository in '{project_name}'[/bold green]")

        console.print(f"[bold green]✅ Project '{project_name}' generated successfully! 🎉[/bold green]")

    except Exception as e:
        console.print(f"[bold red]❌ Unexpected Error: {e}[/bold red]")
        delete_project_directory(project_path)

def create_project_mode():
    """
    Handles user interaction for creating a project using the CLI.
    """
    try:
        console.print("[bold cyan]🔹 Starting Interactive Project Creation...[/bold cyan]")

        # Fetch and display available templates
        available_templates = fetch_available_templates()
        
        if "(No templates found)" in available_templates:
            console.print("[red]❌ No templates available! Please add some to the 'templates/' directory.[/red]")
            return

        # User selects project type
        while True:
            project_type = get_input_with_default("Select a project type", DEFAULTS["project_type"])
            if validate_project_type(project_type):
                break

        # User enters project name
        while True:
            project_name = get_input_with_default("Enter the project name", DEFAULTS["project_name"])
            if validate_project_name(project_name):
                break

        # Ask if Git should be initialized
        use_git = Confirm.ask("[bold green]📌 Initialize a Git repository?[/bold green]", default=True)

        # Create the project
        create_project(project_type, project_name, use_git)

    except KeyboardInterrupt:
        console.print("\n\n[bold red]👋 Goodbye! Project creation canceled.[/bold red]")
        sys.exit(0)

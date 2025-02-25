from fastgen.utils.template_loader import load_template
import os
import shutil
from rich.console import Console

# Initialize Rich Console
console = Console()

def delete_project_directory(project_path):
    """Deletes the entire project directory if creation fails."""
    if os.path.exists(project_path):
        shutil.rmtree(project_path)
        console.print(f"[bold red]🗑️ Removed incomplete project: {project_path}[/bold red]")
    else:
        console.print(f"[bold yellow]⚠️ Warning: Project directory '{project_path}' does not exist, skipping deletion.[/bold yellow]")

def run(project_type, project_name, use_git):
    """
    Creates a project structure based on the given template.

    :param project_type: Type of project template
    :param project_name: Name of the project folder
    :param use_git: Boolean to initialize Git repository
    """
    try:
        # Load the template
        template = load_template(project_type)
        base_dir = "generated_projects"
        project_path = os.path.join(base_dir, project_name)
        
        console.print(f"[bold cyan]🔹 Creating project: {project_path}[/bold cyan]")

        # Create the main project directory
        os.makedirs(project_path, exist_ok=True)

        # Track created directories for rollback
        created_dirs = set()
        created_dirs.add(project_path)

        # Create all necessary directories
        for directory in template.get("directories", []):
            dir_path = os.path.join(project_path, directory)
            os.makedirs(dir_path, exist_ok=True)
            created_dirs.add(dir_path)
            console.print(f"[bold yellow]📁 Created directory: {dir_path}[/bold yellow]")

        # Create and write files
        for file_path, content in template.get("files", {}).items():
            file_full_path = os.path.join(project_path, file_path)
            file_dir = os.path.dirname(file_full_path)

            # Check if directory exists before writing the file
            if not os.path.exists(file_dir):
                raise FileNotFoundError(f"Missing directory '{file_dir}' for file '{file_full_path}'. Please check your template YAML file and ensure all directories exist before adding files.")

            # Create and write the file
            with open(file_full_path, "w", encoding="utf-8") as file:
                file.write(content)
            
            console.print(f"[bold green]📝 Created file: {file_full_path}[/bold green]")

        # Initialize Git repository
        if use_git:
            os.system(f"cd {project_path} && git init")
            console.print(f"[bold green]🔧 Initialized Git repository[/bold green]")

        console.print(f"[bold green]✅ Project '{project_name}' generated successfully in '{base_dir}'! 🎉[/bold green]")

        console.print(f"\nTo get started:\n  [yellow]cd {project_path}[/yellow]\n")

        if use_git:
            console.print("[cyan]git init && git add . && git commit -m 'Initial commit'[/cyan]\n")

        console.print("[bold blue]🚀 Happy Coding![/bold blue] 🎉")

    except FileNotFoundError as e:
        console.print(f"[bold red]⚠️ Error: {e}[/bold red]")
        delete_project_directory(project_path)

    except Exception as e:
        console.print(f"[bold red]❌ Unexpected Error: {e}[/bold red]")
        delete_project_directory(project_path)

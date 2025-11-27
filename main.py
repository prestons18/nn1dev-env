from rich import print
from rich.panel import Panel
from rich.prompt import Prompt
from rich.console import Console
import shutil
import sys
import os
import subprocess

console = Console()

def check_requirements(requirements):
    return [r for r in requirements if shutil.which(r) is None]

def run(cmd, cwd=None):
    try:
        subprocess.run(cmd, cwd=cwd, check=True)
    except subprocess.CalledProcessError:
        console.print(f"[red]Command failed: {' '.join(cmd)}[/red]")
        sys.exit(1)

def setup_website():
    console.print(Panel.fit("[bold cyan]Website Setup[/bold cyan]", border_style="cyan"))
    
    missing = check_requirements(["git", "npm"])
    if missing:
        console.print(f"[red]Missing:[/red] {', '.join(missing)}")
        console.print("[yellow]Please install these tools first.[/yellow]")
        sys.exit(1)
    
    dest = Prompt.ask("Where should I put the website?", default="./website")
    
    if not os.path.exists(dest):
        console.print("[cyan]Cloning repo...[/cyan]")
        run(["git", "clone", "https://github.com/nn1-dev/website.git", dest])
    else:
        console.print("[yellow]Folder already exists, skipping clone.[/yellow]")
    
    console.print("[cyan]Installing dependencies...[/cyan]")
    if shutil.which("pnpm"):
        run(["pnpm", "install"], cwd=dest)
    else:
        console.print("[yellow]pnpm not installed but recommended, using npm instead[/yellow]")
        run(["npm", "install"], cwd=dest)
    
    env_path = os.path.join(dest, ".env")
    if not os.path.exists(env_path):
        console.print("[cyan]Creating .env file...[/cyan]")
        with open(env_path, "w") as f:
            f.write("API_URL_TICKETS=\nAPI_URL_NEWSLETTER=\nAPI_URL_FEEDBACK=\n")
            f.write("API_KEY_TICKETS=dev\nAPI_KEY_NEWSLETTER=dev\nAPI_KEY_FEEDBACK=dev\n")
    
    console.print("[bold green]✔ Done![/bold green]\n")
    console.print(Panel(
        f"[cyan]To start the development server:[/cyan]\n\n"
        f"  cd {dest}\n"
        f"  npm run dev\n\n"
        f"[cyan]Happy hacking! :)[/cyan]",
        title="[bold green]Next Steps[/bold green]",
        border_style="cyan"
    ))

def setup_api():
    console.print(Panel.fit("[bold cyan]API Setup[/bold cyan]", border_style="cyan"))
    
    dest = Prompt.ask("Where should I put the API?", default="./api")
    os.makedirs(dest, exist_ok=True)
    
    console.print("[bold green]✔ API folder created![/bold green]")

def main():
    console.print(Panel(
        "[bold cyan]NN1 Dev Setup[/bold cyan]\n"
        "Made by Preston Arnold - Arnold Development\n"
        "[link=https://prestonarnold.uk]prestonarnold.uk[/link]",
        expand=False,
        border_style="cyan"
    ))
    
    choice = Prompt.ask("What do you want to set up?", choices=["website", "apis"], default="website")
    
    if choice == "website":
        setup_website()
    elif choice == "apis":
        setup_api()

if __name__ == "__main__":
    main()

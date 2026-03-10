from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Log, Label
from textual.containers import Vertical, Horizontal
import asyncio
import random

class SimulationApp(App):
    CSS = """
    Screen {
        background: #0d1117;
    }
    #sidebar {
        width: 30;
        background: #161b22;
        border-right: solid #30363d;
        padding: 1 2;
    }
    #output {
        padding: 1 2;
    }
    .title {
        color: #58a6ff;
        text-style: bold;
        margin-bottom: 1;
    }
    Button {
        width: 100%;
        margin-bottom: 1;
    }
    #btn-simulation { background: #238636; }
    #btn-simulation:hover { background: #2ea043; }
    #btn-clear { background: #6e7681; }
    Log {
        height: 100%;
        background: #0d1117;
        border: solid #30363d;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Label("⚙ ACTIONS", classes="title")
                yield Button("▶ Lancer simulation", id="btn-simulation", variant="success")
                yield Button("📊 Générer rapport",  id="btn-rapport")
                yield Button("🔄 Reset données",    id="btn-reset")
                yield Button("🗑 Effacer logs",     id="btn-clear", variant="default")
            with Vertical(id="output"):
                yield Label("📋 OUTPUT", classes="title")
                yield Log(id="log", auto_scroll=True)
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        log = self.query_one(Log)

        if event.button.id == "btn-simulation":
            log.write_line("[bold green]>>> Simulation démarrée...[/]")
            for i in range(1, 6):
                await asyncio.sleep(0.5)
                val = random.uniform(0, 100)
                log.write_line(f"  Étape {i}/5 — valeur: {val:.2f}")
            log.write_line("[bold green]✓ Simulation terminée.[/]\n")

        elif event.button.id == "btn-rapport":
            log.write_line("[bold blue]>>> Génération du rapport...[/]")
            await asyncio.sleep(0.3)
            log.write_line("  Lignes traitées : 1024")
            log.write_line("  Erreurs         : 0")
            log.write_line("  Statut          : OK\n")

        elif event.button.id == "btn-reset":
            log.write_line("[bold yellow]>>> Données réinitialisées.[/]\n")

        elif event.button.id == "btn-clear":
            log.clear()

def main():
    app = SimulationApp()
    app.run()

if __name__ == "__main__":
    main()
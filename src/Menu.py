from textual.app import App, ComposeResult
from textual.widgets import Label, Button, Log
from textual.containers import Horizontal, Vertical
from src.Map import Map
from src.visualizer import animate


class Menu(App):
    CSS = """ 

    Screen{
        background: #0d1117;
    }

    #title{
        text-style: bold;
        text-align: center;
        width: 100%;
        padding: 1 0;
    }
    
    #sidebar{
        width: 30%;
        align: center top;
        padding: 1 2;
    }

    Button{
        width: 80%;
        margin: 1;
    }

    #log_consol{
        width: 70%;
        padding: 1 2;
    }
 """


    @classmethod
    def menu_init(cls, map: Map, path: str) -> None:
        cls.map = map
        cls.path = path

    def compose(self) -> ComposeResult:
        
        with Vertical():
            yield Label("Fly In", id="title")
            with Horizontal():
                with Vertical(id="sidebar"):
                    yield Button("Start Simulation", id="btn-sim")
                    yield Button("Start Visual", id="btn-pg")
                    yield Button("Exit", id="btn-quit", variant="error")
                with Vertical(id="log_consol"):
                    yield Log(id="log")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        log = self.query_one(Log)
        match event.button.id:
            case "btn-sim":
                log.write(self.map.print_path())
            case "btn-pg":
                animate(self.map)
            case "btn-quit":
                self.exit()

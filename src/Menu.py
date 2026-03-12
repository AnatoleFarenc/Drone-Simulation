from textual.app import App, ComposeResult
from textual.widgets import Label, Button, Log
from textual.containers import Horizontal, Vertical
from src.Map import Map
from src.visualizer import animate
from src.parser import get_data, check_data
from src.config import ROOT_NAME


class Menu(App):
    CSS = """
    Screen {
        background: #1e1e28;
        text-style: none;
    }

    #title {
        text-style: bold;
        text-align: center;
        width: 100%;
        padding: 1 0;
    }

    #sidebar {
        width: 30%;
        align: center top;
        padding: 1 2;
    }

    #console {
        width: 70%;
        padding: 1 2;
    }

    Log {
        scrollbar-size: 1 0;
    }

    .btn {
        width: 80%;
        margin: 1;
        text-style: none;

    }

    .selector {
        width: 80%;
        height: 3;
        margin: 1 1;
    }

    .selector-btn {
        width: 5;
        min-width: 5;
        margin: 0 1;
        text-style: none;
    }

    .selector-label {
        width: 1fr;
        text-align: center;
        margin: 1 1;
    }
"""

    @classmethod
    def menu_init(cls, map: Map, path: str, path_dict: str) -> None:
        cls.map = map
        cls.path_dict = path_dict
        cls.path = path
        cls.speed = cls.map.speed

        cls.dirs = [key for key, _ in path_dict.items()]
        dir_name = ["challenger", "hard", "medium", "easy"]
        for name in dir_name:
            if name in cls.dirs:
                cls.dirs.remove(name)
                cls.dirs.insert(0, name)

        for dir, _ in cls.path_dict.items():
            cls.path_dict[dir].sort()

        cls.idx_file = 0
        cls.idx_dir = 0
        cls.file_name = path.split('/')[-1]

    def get_path_map(self, dir: str, map_file: str) -> str:
        return ROOT_NAME + dir + '/' + map_file

    def change_map(self):
        log = self.query_one(Log)
        try:
            map_data = get_data(self.path)
            check_data(map_data)
            self.map = Map.map_init(map_data)
        except Exception as e:
            log.write("Invalid map file format")
            log.write(f"{e}")
            return
        self.map.speed = self.speed

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("Fly In", id="title")
            with Horizontal():
                with Vertical(id="sidebar"):
                    with Horizontal(classes="selector"):
                        yield Button("<", id="btn-prev-dir",
                                     classes="selector-btn")
                        yield Label(
                            f"{self.dirs[self.idx_dir]}",
                            id="dir-label",
                            classes="selector-label"
                        )
                        yield Button(">", id="btn-next-dir",
                                     classes="selector-btn")

                    with Horizontal(classes="selector"):
                        yield Button("<", id="btn-prev-file",
                                     classes="selector-btn")
                        yield Label(
                            f"{self.file_name}",
                            id="file-label",
                            classes="selector-label"
                        )
                        yield Button(">", id="btn-next-file",
                                     classes="selector-btn")

                    yield Button("Start Simulation", id="btn-sim",
                                 classes="btn")
                    yield Button("Clean Simulation", id="btn-clean-sim",
                                 classes="btn")
                    yield Button("Start Visual", id="btn-pg", classes="btn")

                    with Horizontal(classes="selector"):
                        yield Button("+", id="btn-plus",
                                     classes="selector-btn")
                        speed = round(self.map.speed, 1)
                        yield Label(
                            f"{speed} ms\n[b]speed[/b]",
                            id="speed_label",
                            classes="selector-label"
                        )
                        yield Button("-", id="btn-minus",
                                     classes="selector-btn")

                    yield Button("Exit", id="btn-quit", variant="error",
                                 classes="btn")

                with Vertical(id="console"):
                    yield Log(id="log")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        log = self.query_one(Log)
        match event.button.id:
            case "btn-sim":
                log.clear()
                log.write(self.map.print_path())

            case "btn-clean-sim":
                log.clear()

            case "btn-pg":
                animate(self.map, self.map.speed)

            case "btn-plus":
                self.map.speed += 0.1
                self.speed += 0.1
                speed = round(self.map.speed, 1)
                self.query_one("#speed_label", Label).update(
                    f"{speed} ms\n[b]speed[/b]"
                )
            case "btn-minus":
                self.map.speed -= 0.1
                self.speed -= 0.1
                speed = round(self.map.speed, 1)
                self.query_one("#speed_label", Label).update(
                    f"{speed} ms\n[b]speed[/b]"
                )

            case "btn-prev-dir":
                self.idx_dir = max(0, self.idx_dir - 1)
                self._update_dir()
            case "btn-next-dir":
                self.idx_dir = min(len(self.dirs) - 1, self.idx_dir + 1)
                self._update_dir()

            case "btn-prev-file":
                self.idx_file = max(0, self.idx_file - 1)
                self._update_file()
            case "btn-next-file":
                dirm = self.dirs[self.idx_dir]
                nb_file = len(self.path_dict[dirm])
                self.idx_file = min(nb_file - 1, self.idx_file + 1)
                self._update_file()

            case "btn-quit":
                self.exit()

    def _update_dir(self) -> None:
        dirm = self.dirs[self.idx_dir]
        self.query_one("#dir-label", Label).update(dirm)
        self.idx_file = 0
        self._update_file()

    def _update_file(self) -> None:
        dirm = self.dirs[self.idx_dir]
        filem = self.path_dict[dirm][self.idx_file]
        self.path = self.get_path_map(dirm, filem)
        self.file_name = self.path.split('/')[-1]
        self.query_one("#file-label", Label).update(self.file_name)
        self.change_map()

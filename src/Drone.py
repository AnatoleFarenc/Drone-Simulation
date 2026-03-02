from .Hub import Hub
from .Connection import Connection


class Drone():
    def __init__(self, name: str, c_hub: Hub):
        """ Set default setting """
        self.name = name
        self.c_hub = c_hub
        self.n_hub = c_hub
        self.len_path = 1
        self.nb_move = 0
        self.__stay = False
        self.__path = []
        self.con = None

    @property
    def name(self) -> str:
        """ Return name of drone """
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        """ Set name """
        self.__name = name

    @property
    def c_hub(self) -> Hub:
        """ Return the curent hub where the drone here """
        return self.__c_hub

    @c_hub.setter
    def c_hub(self, current_hub: Hub) -> None:
        """ Set the current hub """
        self.__c_hub = current_hub

    @property
    def n_hub(self) -> Hub | None:
        """ Return the next hub where the drone here """
        return self.__n_hub

    @n_hub.setter
    def n_hub(self, next_hub: Hub) -> None:
        """ Set the next hub """
        self.__n_hub = next_hub

    @property
    def len_path(self) -> int:
        """ Return len path [conection] """
        return self.__len_path

    @len_path.setter
    def len_path(self, len: int) -> None:
        """ Set len path """
        if len > 0:
            self.__len_path = len
        else:
            raise ValueError(f"Error: len({len} must be > 0)")

    @property
    def nb_move(self) -> int:
        """ Return nb_move remaining """
        return self.__nb_move

    @nb_move.setter
    def nb_move(self, move) -> None:
        """ Set move to nb_move """
        self.__nb_move = move

    @property
    def stay(self) -> bool:
        """ Return if the drone stay or not """
        return self.__stay

    @stay.setter
    def stay(self, stay) -> None:
        """ Set if the drone stay or not """
        self.__stay = stay

    @property
    def path(self) -> bool:
        """ Return path to goal """
        return self.__path

    @path.setter
    def path(self, path) -> None:
        """ Set paht to goal """
        self.__path = path

    @property
    def con(self) -> Connection:
        """ Return con"""
        return self.__con

    @con.setter
    def con(self, con) -> None:
        """ Set new """
        self.__con = con

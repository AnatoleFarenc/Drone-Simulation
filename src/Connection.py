from typing import Tuple, Dict
from .Hub import Hub


class Connection():
    def __init__(self, hubs: Tuple[Hub, Hub],
                 complementary_setting: Dict = {}) -> None:
        self.hubs = hubs
        self.c_setting = complementary_setting

    @property
    def hubs(self) -> Tuple[Hub, Hub]:
        """ Return tuple of hubs name connection """
        return self.__hubs

    @hubs.setter
    def hubs(self, hubs: Tuple[Hub, Hub]) -> None:
        """ Set hubs """
        self.__hubs = hubs

    @property
    def c_setting(self) -> Dict:
        """ Return complementary setting """
        return self.__c_setting

    @c_setting.setter
    def c_setting(self, complementary_setting: Dict) -> None:
        """ Set complementary setting """
        self.__c_setting = complementary_setting

    def __str__(self) -> str:
        return f"{self.hubs[0].name}-{self.hubs[1].name}"

from typing import Tuple, Dict
from .Hub import Hub


class Connection():
    def __init__(self, hubs: Tuple[Hub, Hub],
                 complementary_setting: Dict = {}) -> None:
        self.hubs = hubs
        self.c_setting = complementary_setting
        self.__is_visible = True
        self.capacity = 0
        self.m_capacity = 1

        if self.c_setting.get('max_link_capacity'):
            value = self.c_setting.get('max_link_capacity')
            try:
                value = int(value)
            except ValueError:
                raise ValueError(f"error: invalid value {value}")
            if value < 0:
                raise ValueError(f"error: invalid value {value}")
            self.m_capacity = value

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

    @property
    def is_visible(self) -> bool:
        """ Return if the connection is visble """
        return self.__is_visible

    @is_visible.setter
    def is_visible(self, is_visible: bool) -> None:
        """ Set connection visibility """
        self.__is_visible = is_visible

    @property
    def capacity(self) -> int:
        """ Return current number of drone in link """
        return self.__capacity

    @capacity.setter
    def capacity(self, nb_drone) -> None:
        """ Update the number of drone in link """
        self.__capacity = nb_drone

    @property
    def m_capacity(self) -> int:
        """ Return number of max drone in link """
        return self.__m_capacity

    @m_capacity.setter
    def m_capacity(self, nb_drone) -> None:
        """ Update the number of max drone in link """
        self.__m_capacity = nb_drone

    def __str__(self) -> str:
        return f"{self.hubs[0].name}-{self.hubs[1].name}"

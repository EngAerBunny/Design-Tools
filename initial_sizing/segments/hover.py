from segments.power.vertical_power import hover_power_loading as power_loading
from segments.power.vertical_power import vi_hover as vi_func
from segments.vertical import VerticalMode

class Hover(VerticalMode):
    def __init__(self, time: float, rho: float, ki: float, tip_speed: float, cd0: float,
                 solidity: float, disk_loading: float):
        super().__init__(rho, ki, tip_speed, cd0, solidity, disk_loading=disk_loading)
        self._time = time / 3600

    @property
    def time(self):
        return self._time
    
    @property
    def vi_hover(self):
        return vi_func(self._disk_loading, self._rho)
    
    def set_wing_load(self, wing_load):
        pass

    def set_power_loading(self):
        self._power_loading = power_loading(self._ki, self._disk_loading, self._rho, self._tip_speed, self._solidity,
                                    self._cd0, vi_func(self._disk_loading, self._rho))
    


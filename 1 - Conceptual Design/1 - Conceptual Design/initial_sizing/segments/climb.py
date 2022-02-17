import numpy as np
from segments.forward import ConventionalFlight

class Climb(ConventionalFlight):
    def __init__(self, climb_speed: float, climb_gradient: float, climb_height: float, prop_efficiency: float, fcell: object, rho: float, CD0: float, k: float):
        super().__init__(climb_speed, prop_efficiency, fcell, k, CD0, rho, climb_grad=climb_gradient)
        self._height = climb_height * 0.3048

    @property
    def time(self):
        return (self._height / self._climb_grad) / 3600

    @property
    def height(self):
        return self._height / 0.3048

    @property
    def climb_angle(self):
        return np.arcsin(self._climb_grad / self._speed)
    
    @property
    def range_climb(self):
        return np.sqrt(self._speed ** 2 - self._climb_grad ** 2) * self.time * 3.6







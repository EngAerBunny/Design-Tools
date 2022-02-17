import numpy as np
from segments.forward import ConventionalFlight

class Glide(ConventionalFlight):
    def __init__(self, prop_efficiency: float, fcell: object, k: float, CD0: float, rho: float, cl: float, wing_load: float, descent_height: float, power=0, speed = 0):
        super().__init__(speed, prop_efficiency, fcell, k, CD0, rho, wing_load=wing_load)
        self._cl = cl
        self._descent_height = descent_height * 0.3048
        self._cl_cd = 4 * CD0 * k
        self._power = power
        
    @property
    def descent_grad(self):
        return np.sqrt((2 * self._wing_load)/(self._rho * self._cl / self._cl_cd))
    
    @property
    def speed(self):
        return np.sqrt((2 * self._wing_load / self._rho) / self._cl)
    
    @property
    def time(self):
        return (self._descent_height / self.descent_grad) / 3600

    @property
    def range_glide(self):
        return np.sqrt(self.speed ** 2 - self.descent_grad ** 2) * self.time * 3.6
    
    def set_wing_load(self, wing_load):
        pass


    def set_power_loading(self):
        pass

    def set_power(self, weigth):
        pass

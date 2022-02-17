from segments.forward import ConventionalFlight

class Loiter(ConventionalFlight):
    def __init__(self, speed: float, prop_efficiency: float, fcell: object, k: float, CD0: float, rho: float,
                time = 0, reserve=0):
        super().__init__(speed, prop_efficiency, fcell, k, CD0, rho)
        self._time = time
        self._reserve = reserve
    
    @property
    def loiter_range(self):
        return self._speed * self._time * 3.6
    
    @property
    def time(self):
        return self._time + self._reserve

    @time.setter
    def time(self, time):
        self._time = time



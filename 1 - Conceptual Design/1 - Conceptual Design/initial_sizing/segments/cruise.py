from segments.forward import ConventionalFlight

class Cruise(ConventionalFlight):
    def __init__(self, speed: float, cruise_range: float, prop_efficiency: float, fcell: object, k: float, CD0: float, rho: float,
                 thrust=1, n=1, wing_load=0):
        super().__init__(speed, prop_efficiency, fcell, k, CD0, rho)
        self._range = cruise_range
    
    @property
    def time(self):
        return self._range / (self._speed * 3.6)

    def set_wing_load(self, wing_load):
        self._wing_load = wing_load

    def set_thrust(self, thrust):
        self._thrust = thrust


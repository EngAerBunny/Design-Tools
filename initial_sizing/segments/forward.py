import aircraft_data
from segments.power.forward_power import power_loading

avio_power = aircraft_data.AVIONICS.POWER
fcell_nominal_power = aircraft_data.FCELL.nominal_power
eta_es = aircraft_data.E_SYSTEM.EFFICIENCY

class ConventionalFlight():
    def __init__(self, speed: float, prop_efficiency: float, fcell: object, k: float, CD0: float, rho: float,
    wing_load=0, power_loading = 0, power = 0, climb_grad=0):
        self._speed = speed * 0.5144
        self._prop_efficiency = prop_efficiency
        self._fcell = fcell
        self._k = k
        self._CD0 = CD0
        self._rho = rho
        self._wing_load = wing_load
        self._power_loading = power_loading
        self._power = power
        self._climb_grad = climb_grad * 0.00508

    def set_power(self, weight):
        self._power = self._power_loading * weight

    @property
    def power(self):
        return self._power

    def set_power_loading(self):
        self._power_loading = power_loading(self._prop_efficiency, self._climb_grad, self._speed, self._rho, self._CD0, self._wing_load, self._k) 
    
    @property
    def fcell_efficiency(self):
        total_required_power = self._power/eta_es + avio_power
        return self._fcell.efficiency(total_required_power)
    
    def set_thrust(self, thrust):
        self._thrust = thrust
    
    def set_wing_load(self, wing_load):
        self._wing_load = wing_load




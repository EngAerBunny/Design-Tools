import numpy as np
import aircraft_data

# ----------------------------------------------------------------------------------------------------#
class LiftCoeffEstimator():
    def __init__(self, CD0: float, k: float, cl_max: float):
        self._CD0 = CD0
        self._k = k
        self._cl_max = cl_max

    @property
    def cl_max(self):
        return self._cl_max

    @property
    def cl_max_endurance(self):
        return np.sqrt(3 * self._CD0 / self._k)

    @property
    def cl_max_range(self):
        return np.sqrt(self._CD0 / self._k)


# ----------------------------------------------------------------------------------------------------#
def wing_load(rho: float, speed: float, CL: float) -> float:
    return 0.5 * rho * (speed * 0.5144)** 2 * CL


# ----------------------------------------------------------------------------------------------------#
def thrust_hover(MTOM: float, g: float):
    return MTOM * g


# ----------------------------------------------------------------------------------------------------#
def total_rotor_area(rotor_number: float, rotor_radius: float) -> float:
    return np.pi * rotor_radius**2 * rotor_number


# ----------------------------------------------------------------------------------------------------#
def wing_span(aspect_ratio: float, wing_area: float) -> float:
    return np.sqrt(aspect_ratio * wing_area)


# ----------------------------------------------------------------------------------------------------#

# Mass computations

def propulsion_mass(max_required_power: float, power_weight_ratio_engine: float, power_weight_ratio_esc: float,
                  int_factor=0) -> float:
    return ((max_required_power / 1000) / power_weight_ratio_engine +
            (max_required_power / 1000) / power_weight_ratio_esc) * (1 + int_factor)


def structural_mass(structural_weight_ratio: float, MTOM: float):
    '''
    structural_weight_ratio -> percentage of MTOM
    MTOM -> Maximum Take Off Mass, units [Kg]
    '''
    return structural_weight_ratio * MTOM


def wing_mass(wing_load: float, aspect_ratio: float, thrust: float) -> float:
    return (thrust / wing_load) * 1.495 + np.sqrt(aspect_ratio * thrust / wing_load) / 2 * 0.475


def fuel_mass(energy: float, e_fuel) -> float:
    '''
    energy is the value that must be produced by the fuel, units [W.h]
    e_fuel represents the specific energy density of the fuel to be used, units [Mj/Kg]
    '''
    return energy * (3.6 / 1000) / e_fuel


def battery_mass(energy: float, e_bat) -> float:
    '''
    energy -> energy quantity that must be provided by the batteries, units [W.h]
    e_bat -> specific energy density of the battery, units [W.h/Kg]
    '''
    return energy / e_bat


# ----------------------------------------------------------------------------------------------------#

# Receives efficiency and variable number of mission segments
# Note that each mission segment is an object of the type (climb, cruise, glide, loiter,
# vertical climb or vertical descent)

# Each object has a time and power associated with it

def energy_from_batteries(segments: list, efficiency: float):
    energy = 0

    for segment in segments:
        energy += (segment.power * segment.time)

    return (energy / efficiency)

# ----------------------------------------------------------------------------------------------------#
def energy_from_fuel(segments: list, efficiency: float, fcell_nominal_power: float, avio_power: float):
    energy_to_motors = 0
    energy_to_avionics = 0
    missing_energy = 0
    for segment in segments:

        # if segment.power/efficiency + avio_power > 1500:
        if segment.power/efficiency + avio_power > fcell_nominal_power:
            energy_to_motors += (fcell_nominal_power) * efficiency * segment.time / 0.5
            missing_energy += (segment.power/efficiency - (fcell_nominal_power - avio_power)) * segment.time
        
        else:
            energy_to_avionics += avio_power * segment.time / segment.fcell_efficiency
            energy_to_motors += (segment.power * segment.time) / segment.fcell_efficiency

    return energy_to_motors/efficiency + energy_to_avionics, missing_energy

# ----------------------------------------------------------------------------------------------------#
# def loiter_time(loiter: object, fcell_powered_segments_energy: float, descent_energy_from_fuel: float, 
#                 energy_to_recharge_battery: float) -> float:

#     # Constants to be used, imported from the inputs module
#     FUEL_MASS = aircraft_data.H2_MASS # [g]
#     FUEL_SPECIFIC_ENERGY = aircraft_data.FUEL_SPECIFIC_ENERGY
#     ETA_ES = aircraft_data.E_SYSTEM.EFFICIENCY
#     AVIO_POWER = aircraft_data.AVIONICS.POWER

#     total_energy_from_fuel = (FUEL_MASS*0.95)*FUEL_SPECIFIC_ENERGY*(1000/3.6)
#     # Energy that must be provided by the H2 (upstream of the fuel cell) to the loiter segment
#     # is given by the difference of the total energy with the sum of the energy given to fly all the other
#     # segments with the energy that must be provided to recharge the battery

#     loiter_energy_from_fuel = total_energy_from_fuel - fcell_powered_segments_energy - descent_energy_from_fuel - energy_to_recharge_battery

#     # required_power_loiter is the power that must be available at the fuel cell from the H2 in order for it
#     # to produce the necessary power to fly the segment
#     required_power_loiter = (loiter.power/ETA_ES + AVIO_POWER)/loiter.fcell_efficiency

#     return (loiter_energy_from_fuel/required_power_loiter)
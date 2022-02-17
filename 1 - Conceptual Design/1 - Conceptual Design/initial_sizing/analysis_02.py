# ---------------------------------------------------------------------------------------------------- #
# importing modules with classes and functions to be used throughout the script
from typing import Union

import numpy as np

import aircraft_data

import computations

from segments.climb import Climb
from segments.cruise import Cruise
from segments.glide import Glide
from segments.hover import Hover
from segments.loiter import Loiter
from segments.vertical_climb import VerticalClimb
from segments.vertical_descent import VerticalDescent
from mtow import mtow_estimation

# ---------------------------------------------------------------------------------------------------- #
def main(disk_loading: float, wing_loading: float, wing_aspect_ratio: float, stall_speed: float, 
    operational_speed: float, loiter_time: float) -> list:

    # ------------------------------------------------------------------------------------------------- #
    # Importing inputs

    GRAVITY = aircraft_data.GRAVITY # Gravitational Acceleration, units -> m/s^2
    SOUND_SPEED = aircraft_data.SOUND_SPEED # Speed of sound - SL, ISA + 20ºC Sea Level Conditions, units -> (m/s)

    FCELL = aircraft_data.FCELL

    ROTOR = aircraft_data.ROTOR

    # DISK_LOADING = disk_loading * 47.88

    PERFORMANCE = aircraft_data.PERFORMANCE

    PROP_EFFICIENCY = aircraft_data.PROPELLER_EFFICIENCY

    ELECTRIC_SYSTEM_EFFICIENCY = aircraft_data.E_SYSTEM.EFFICIENCY

    AVIO_POWER = aircraft_data.AVIONICS.POWER

    ki = ROTOR.IND_POW_COEFFICIENT

    tip_speed = ROTOR.TIP_MACH * SOUND_SPEED
    cd0 = ROTOR.BASE_DRAG
    solidity = ROTOR.SOLIDITY
    
    # vstall = PERFORMANCE.STALL_SPEED

    vstall = stall_speed

    cl_max = PERFORMANCE.CL_MAX
    CD0 = PERFORMANCE.AIRCRAFT_BASE_DRAG
    k = 1 / (np.pi * wing_aspect_ratio * 0.75)
    # l_d_ratio = inputs.PERFORMANCE.L_D_RATIO

    rho_SL = aircraft_data.SEA_LVL_DENSITY
    rho_climb_2 = aircraft_data.AIR_DENSITY_1500
    rho_mission = aircraft_data.MISSION_AIR_DENSITY
    rho_ceiling = aircraft_data.CEILING_AIR_DENSITY

    
    # ---------------------------------------------------------------------------------------------------- #

    # Mission segments instantiation:

    vertical_mode_battery_powered_segments = []
    fcell_powered_segments = []
    forward_mode_battery_powered_segments = []

    cruise_speed = operational_speed
    loiter_speed = operational_speed

    # Vertical Take off Segment
    v_take_off = VerticalClimb(vertical_speed=2, climb_height=25, prop_efficiency=PROP_EFFICIENCY, ki=ki, rho=rho_SL,
                               tip_speed=tip_speed, cd0=cd0, solidity=solidity, disk_loading=disk_loading)
    vertical_mode_battery_powered_segments.append(v_take_off)

    # Transition to forward flight
    transition_1 = Hover(time=30, rho=rho_SL, ki=ki, tip_speed=tip_speed, cd0=cd0, solidity=solidity, disk_loading=disk_loading)
    vertical_mode_battery_powered_segments.append(transition_1)

    # Climb Segments:
    climb1 = Climb(climb_speed=33, climb_gradient=500, climb_height=1500, prop_efficiency=PROP_EFFICIENCY, fcell=FCELL, rho=rho_SL,
                   CD0=CD0, k=k)
    climb2 = Climb(climb_speed=36, climb_gradient=300, climb_height=3500, prop_efficiency=PROP_EFFICIENCY, fcell=FCELL, rho=rho_climb_2,
                   CD0=CD0, k=k)

    fcell_powered_segments.append(climb1)
    fcell_powered_segments.append(climb2)

    # Cruise Segment to mission location
    cruise_1_range = 50 - (climb1.range_climb + climb2.range_climb)
    cruise1 = Cruise(speed=cruise_speed, cruise_range=cruise_1_range, prop_efficiency=PROP_EFFICIENCY, fcell=FCELL, k=k, CD0=CD0,
                     rho=rho_mission)
    fcell_powered_segments.append(cruise1)

    # Loiter main mission
    loiter = Loiter(speed=loiter_speed, prop_efficiency=PROP_EFFICIENCY, fcell=FCELL, k=k, CD0=CD0, rho=rho_mission, time=loiter_time)
    fcell_powered_segments.append(loiter)

    # ----------------------------------------------------------------------------------------------------#
    # Wing-Loading Constraint Computation
    cl_estimator = computations.LiftCoeffEstimator(CD0, k, cl_max)

    wing_load_stall = computations.wing_load(rho_SL, vstall, cl_estimator.cl_max)
    wing_load_range = computations.wing_load(rho_mission, cruise_speed, cl_estimator.cl_max_range)
    wing_load_endurance = computations.wing_load(rho_mission, loiter_speed, cl_estimator.cl_max_endurance)
    # wing_load_ceiling = computations.wing_load(rho_ceiling, cruise_speed, cl_estimator.cl_max_range)

    max_wing_load = min(wing_load_stall, wing_load_range, wing_load_endurance)
    # max_wing_load = min(wing_load_stall, wing_load_range, wing_load_endurance, wing_load_ceiling)

    # ----------------------------------------------------------------------------------------------------#
    # Descent mission, no power consumed. Glider mode
    cl_estimator = computations.LiftCoeffEstimator(CD0, k, cl_max)
    descent_height = climb1.height + climb2.height  # units -> [ft]
    descent = Glide(prop_efficiency=PROP_EFFICIENCY, fcell=FCELL, k=k, CD0=CD0, rho=rho_mission, cl=cl_estimator.cl_max_range, 
                    wing_load=wing_loading, descent_height=descent_height)
    forward_mode_battery_powered_segments.append(descent)

    # Cruise Segment from mission location to base
    cruise_range_2 = 50 - descent.range_glide
    cruise2 = Cruise(speed=cruise_speed, cruise_range=cruise_range_2, prop_efficiency=PROP_EFFICIENCY, fcell=FCELL, k=k, CD0=CD0, rho=rho_mission)
    fcell_powered_segments.append(cruise2)

    # Landing Circuit modeled as a loiter segment
    land_circuit = Loiter(speed=35, time=3/60, prop_efficiency=PROP_EFFICIENCY, fcell=FCELL, k=k, CD0=CD0, rho=rho_SL)
    forward_mode_battery_powered_segments.append(land_circuit)

    for segment in fcell_powered_segments:
        segment.set_wing_load(wing_loading)
        segment.set_power_loading()
    
    for segment in forward_mode_battery_powered_segments:
        segment.set_wing_load(wing_loading)
        segment.set_power_loading()

    # Transition to vertical mode
    transition_2 = Hover(time=45, rho=rho_SL, ki=ki, tip_speed=tip_speed, cd0=cd0, solidity=solidity, disk_loading=disk_loading)
    vertical_mode_battery_powered_segments.append(transition_2)

    # Vertical landing
    landing = VerticalDescent(speed=1, height=20, prop_efficiency=PROP_EFFICIENCY, vi_hover=transition_1.vi_hover, ki=ki,
                                rho=rho_SL, tip_speed=tip_speed, cd0=cd0, solidity=solidity, disk_loading=disk_loading)
    vertical_mode_battery_powered_segments.append(landing)

    for segment in vertical_mode_battery_powered_segments:
        segment.set_power_loading()

    # ----------------------------------------------------------------------------------------------------#
    # Iterative block that estimates the Maximum Take off Mass
    MTOM, fuel_mass = mtow_estimation(
        21.6, 
        0.001, 
        50,
        vertical_mode_battery_powered_segments, 
        fcell_powered_segments,
        forward_mode_battery_powered_segments, 
        wing_aspect_ratio)


    # ----------------------------------------------------------------------------------------------------#
    # After having the MTOW estimated w. all the required powers estimated
    # the loiter time is computed. Loiter time is a result of an energy balance w. the total available energy
    # provided by the H2 and the energy that was spent to fly the segments
    # the energy that is not spent to fly all the other segments is used for the loiter mission
    
    # fcell_powered_segments[3].time = computations.loiter_time(fcell_powered_segments[3], energy_fuel, 
                                                            # energy_bat_to_climb/0.5, energy_fuel_descent)


    # ----------------------------------------------------------------------------------------------------#
    endurance = sum([segment.time for segment in vertical_mode_battery_powered_segments]) + \
                sum(segment.time for segment in fcell_powered_segments) + sum(segment.time for segment in forward_mode_battery_powered_segments)

    wing_area = (1/wing_loading) * MTOM * GRAVITY

    wingspan = computations.wing_span(aspect_ratio=wing_aspect_ratio, wing_area=wing_area)

    power_lvl_flight = max([fcell_powered_segments[2].power, fcell_powered_segments[3].power])  / ELECTRIC_SYSTEM_EFFICIENCY + AVIO_POWER

    # rotor_diameter is calculated in inches
    rotor_diameter = np.sqrt(MTOM * GRAVITY/ (4 * np.pi * disk_loading)) * 2 / 0.0254

    return MTOM, endurance, fuel_mass, power_lvl_flight, wingspan, wing_loading, max_wing_load, vstall, operational_speed, rotor_diameter

# ----------------------------------------------------------------------------------------------------#

(mtow, flight_time, fuel_mass, lvl_flight_power, 
wingspan, wing_load_given, max_wing_load, stall_speed, cruise_speed, rotor_diameter) = main(218.5, 154.4, 12, 28, 38, 3)

print(f'Maximum Take-off mass is {mtow} [kg]')
print(f'The total time of the mission is {flight_time} [h]')
# print(f'the amount of hydrogen required is {H2_mass} [kg]')
print(f'The maximum power required in forward mode is {lvl_flight_power} [W]')
# print(f'The VTOL battery mass is {VTOL_Battery_Mass} [kg]')
# print(f'The Fuel Cell battery mass is {FCell_Battery_Mass} [kg]')
print(f'The wingspan is {wingspan} [m]')
# print(f'The wing area is {wing_area} [m2]')
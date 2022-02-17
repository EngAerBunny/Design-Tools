# Input classes constructors
import collections

Battery = collections.namedtuple('Battery', ['SPECIFIC_ENERGY', 'RESERVE', 'BACKUP_TIME']) # SPECIFIC_ENERGY units [W.h/kg], BACKUP_TIME unit [h]
ElectricSystem = collections.namedtuple('ElectricSystem', ['EFFICIENCY', 'ENG_POW_WEI_RATIO_VERTICAL', 'ENG_POW_WEI_RATIO_FORWARD', 'ESC_POW_WEI_RATIO', 'INTEGRATION_FACTOR']) # POW_WEI_RATIO units [kW/kg]
# FuelCellSystem = collections.namedtuple('FuelCell', ['EFFICIENCY', 'FUEL_SPECIFIC_ENERGY', 'SYS_MASS', 'TANK_WEIGHT_RATIO', 'NOMINAL_POWER']) # FUEL_SPECIFIC_ENERGY unit [MJ/kg]
Rotor = collections.namedtuple('Rotor', ['BASE_DRAG', 'TIP_MACH', 'SOLIDITY', 'DISK_LOADING', 'IND_POW_COEFFICIENT', 'NUMBER_OF_ROTORS']) # DISK_LOADING unit [N/m^2]
Performance = collections.namedtuple('Performance', ['AIRCRAFT_BASE_DRAG', 'L_D_RATIO', 'STALL_SPEED', 'CL_MAX']) # STALL_SPEED unit [m/s]
Avionics = collections.namedtuple('Avionics', ['POWER', 'MASS']) # POWER unit [W], MASS unit [kg]











import inputs_classes
from fuel_cell import FuelCell

GRAVITY = 9.80665 # Gravitational Acceleration, units -> m/s^2
SOUND_SPEED = 351.906 # Speed of sound - SL, ISA + 20ºC Sea Level Conditions, units -> (m/s)

PERFORMANCE = inputs_classes.Performance(0.04, 9, 30, 1.3)

ROTOR = inputs_classes.Rotor(0.012, 0.55, 0.1, 10 * 4.88242764 * GRAVITY, 1.2, 4)

PROPELLER_EFFICIENCY = 0.65

E_SYSTEM = inputs_classes.ElectricSystem(0.85, 4.5, 3.5, 20, 0.1)
# E_SYSTEM = inputs_classes.ElectricSystem(0.85, 6, 6, 20, 0.1)
AVIONICS = inputs_classes.Avionics(80, 2.5)

BATTERY = inputs_classes.Battery(160, 0.3, 0)
AVIONICS = inputs_classes.Avionics(80, 2.5)

FCELL = FuelCell(800, 0.25 + 0.93)
# FCELL = FuelCell(1300, 2.02)
FUEL_SPECIFIC_ENERGY = 120  # [MJ/Kg]
TANK_WEIGHT_RATIO = 0.035   # [kg/kg]
TANK_MASS = 4.3             # [kg]

STRUCTURAL_WEIGHT_RATIO = 0.35
PAYLOAD = 2 # units -> [kg]

# Relevant Air Densities
SEA_LVL_DENSITY = 1.14549       # Air Density (kg/m3) - SL, ISA + 20ºC conditions
AIR_DENSITY_1500 = 1.09531      # Air Density (kg/m3) - 1500 ft + 20ºC conditions
MISSION_AIR_DENSITY = 0.984762  # Air Density (kg/m3) - 5000 ft + 20ºC conditions
# CEILING_AIR_DENSITY = 0.84189   # Air Density (kg/m3) - 10000 ft + 20ºC conditions

# CEILING_AIR_DENSITY = 0.7767    # Air Density (kg/m3) - 12500 ft + 20ºC conditions
CEILING_AIR_DENSITY = 0.721321  # Air Density (kg/m3) - 15000 ft + 20ºC conditions



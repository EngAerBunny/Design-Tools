import computations
import aircraft_data

# importing some constants from the inputs file

g = aircraft_data.GRAVITY

bat_reserve = aircraft_data.BATTERY.RESERVE
backup_time = aircraft_data.BATTERY.BACKUP_TIME
e_bat = aircraft_data.BATTERY.SPECIFIC_ENERGY

Mavio = aircraft_data.AVIONICS.MASS
avio_power = aircraft_data.AVIONICS.POWER

e_fuel = aircraft_data.FUEL_SPECIFIC_ENERGY

fws = aircraft_data.STRUCTURAL_WEIGHT_RATIO

M_H2_system = aircraft_data.FCELL.mass
fcell_nominal_power = aircraft_data.FCELL.nominal_power

TANK_MASS = aircraft_data.TANK_MASS

payload = aircraft_data.PAYLOAD

eta_es = aircraft_data.E_SYSTEM.EFFICIENCY
p_w_e_forward = aircraft_data.E_SYSTEM.ENG_POW_WEI_RATIO_FORWARD
p_w_e_vertical = aircraft_data.E_SYSTEM.ENG_POW_WEI_RATIO_VERTICAL
p_w_esc = aircraft_data.E_SYSTEM.ESC_POW_WEI_RATIO
h2_to_tank_ratio = aircraft_data.TANK_WEIGHT_RATIO
mi = aircraft_data.E_SYSTEM.INTEGRATION_FACTOR


# MTOW estimation
def mtow_estimation(MTOM0, tol, max_iter, battery_powered_segments, fcell_powered_segments, forward_mode_battery_powered_segments,
                    aspect_ratio) -> float:
    error = 1
    i = 0

    MTOM = MTOM0

    while (error > tol and i < max_iter):

        th = computations.thrust_hover(MTOM, g)

        # Updating the segments power
        battery_time_vertical_mode = 0
        for segment in battery_powered_segments:
            segment.set_power(th)
            battery_time_vertical_mode += segment.time
        
        for segment in fcell_powered_segments:
            segment.set_power(th)
            
        battery_time_forward_mode = 0
        for segment in forward_mode_battery_powered_segments:
            segment.set_power(th)
            battery_time_forward_mode += segment.time

        # Power computations for each mission segment
        power_vertical = max([segment.power for segment in battery_powered_segments])
        power_forward = max([segment.power for segment in fcell_powered_segments])

        p_max_vertical = power_vertical / 0.85

        Mem = computations.propulsion_mass(p_max_vertical, p_w_e_vertical, p_w_esc)  # mass of the electric system (kg) - motor, ESC and integration

        # Forward Flight engine mass
        p_max_forward = power_forward / 0.9
        Mce = computations.propulsion_mass(p_max_forward, p_w_e_forward, p_w_esc)

        Mprop = Mem + Mce

        # Structural Mass computation
        Mstr = fws * MTOM

        # Other masses
        Mow = Mavio + M_H2_system

        empty_mass = Mstr + Mprop + Mow

        # Energy computations:

        energy_fuel, energy_missing = computations.energy_from_fuel(fcell_powered_segments, eta_es, fcell_nominal_power, avio_power)
        
        # Extra energy that might be required in order to climb in case power is > 800 W 
        # This energy will be provided by a battery connected to the fuel cell
        # note that the Avionics must be powered by the fuel cell battery during the vertical mode flight
        energy_bat_to_climb = (energy_missing + battery_time_vertical_mode * avio_power) / (1 - bat_reserve)
        
        # energy that the battery must hold in order to power the descent phase of the flight in forward mode
        # note that the Avionics must be powered by the fuel cell battery during the vertical mode flight
        energy_bat_to_descent_forward_mode = (computations.energy_from_batteries(forward_mode_battery_powered_segments, eta_es) +
            avio_power*(battery_time_forward_mode + battery_time_vertical_mode)) / (1 - bat_reserve)

        energy_fuel_descent, energy_missing_descent = computations.energy_from_fuel(forward_mode_battery_powered_segments, eta_es, fcell_nominal_power, avio_power)

        energy_missing_descent = (energy_missing_descent/eta_es)/(1 - bat_reserve)


        energy_bat_vertical_mode = computations.energy_from_batteries(battery_powered_segments, eta_es) / (1 - bat_reserve)
        energy_backup = (backup_time * fcell_powered_segments[4].time) / eta_es

        energy_bat_vertical_mode_total = energy_bat_vertical_mode + energy_backup

        # H2 mass calculation
        # Extra energy required to climb was given by battery
        # That amount of energy will be replenished in the battery, since the fuel cell will recharge the incorporated battery
        fuel_mass_forward_mode = computations.fuel_mass(energy_fuel, e_fuel)
        fuel_mass_recharge_batt = computations.fuel_mass(energy_bat_to_climb/0.5, e_fuel)
        fuel_mass_descent = computations.fuel_mass(energy_fuel_descent, e_fuel)
        
        fuel_mass = fuel_mass_forward_mode + fuel_mass_recharge_batt + fuel_mass_descent
        tank_mass = TANK_MASS

        battery_mass_vertical_mode = computations.battery_mass(energy_bat_vertical_mode_total, e_bat)
        max_energy_bat_forward_mode = max(energy_bat_to_climb, energy_bat_to_descent_forward_mode, energy_missing_descent)
        battery_mass_forward_mode = computations.battery_mass(max_energy_bat_forward_mode, e_bat)

        MTOM1 = empty_mass + battery_mass_vertical_mode + battery_mass_forward_mode + fuel_mass + tank_mass + payload

        error = abs((MTOM1 - MTOM) / MTOM)
        MTOM = MTOM1
        i += 1

    return MTOM, fuel_mass

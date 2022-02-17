def power_loading(eta_p: float, climb_grad: float, speed: float, rho: float, CD0: float,
                wing_load: float, k: float) -> float:
    return ( (1 / eta_p) * (climb_grad + (rho * speed ** 3 * CD0) / (2 * wing_load) +
                                   (2 * k * wing_load) / (rho * speed)) )

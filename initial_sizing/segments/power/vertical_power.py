import numpy as np

def vi_hover(disk_loading: float, rho: float) -> float:
    return np.sqrt(disk_loading / (2 * rho))


def hover_power_loading(ki: float, disk_loading: float, rho: float, tip_speed: float, sol: float, cd0: float,
                vi_hover: float) -> float:
    return ki * vi_hover + (rho * tip_speed ** 3 / disk_loading) * (sol * cd0 / 8)


def climb_power_loading(climb_speed: float, ki: float, disk_loading: float, rho: float, tip_speed: float,
                cd0: float, sol: float) -> float:
    return (climb_speed - ki * climb_speed / 2 + ki * 0.5 * np.sqrt(climb_speed ** 2 + 2 * disk_loading / rho)
            + ((rho * tip_speed ** 3) / disk_loading) * (sol * cd0 / 8))


def descent_power_loading(descent_speed: float, ki: float, disk_loading: float, rho: float, tip_speed: float,
                  cd0: float, sol: float, vi_hover: float) -> float:
    # use momentum-theory
    if descent_speed / vi_hover <= - 2:
        return (descent_speed - ki / 2 * (descent_speed + np.sqrt(descent_speed ** 2 - 2 * disk_loading / rho))
                + ((rho * tip_speed ** 3) / disk_loading) * (sol * cd0 / 8))
        
    # buckets thrown based on empirical formulation
    v_di = vi_hover * (ki - 1.125 * descent_speed / vi_hover - 1.372 * (descent_speed / vi_hover) ** 2 - 1.718 * (
                descent_speed / vi_hover) ** 3 - 0.655 * (descent_speed / vi_hover) ** 4)
    return (descent_speed + ki * v_di) + ((rho * tip_speed ** 3) / disk_loading) * (sol * cd0 / 8)

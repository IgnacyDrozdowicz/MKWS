import cantera as ct
import numpy as np
import matplotlib.pyplot as plt

def run_simulation(fuel, species_dict, temp, P, simulation_time, step_time):
    time_steps = int(simulation_time / step_time)
    Auto_ig_time = []  # Array for autoignition delay

    for T in temp:
        gas = ct.Solution('gri30.yaml')
        gas.TPX = T, P, species_dict
        r = ct.IdealGasReactor(gas)
        sim = ct.ReactorNet([r])
        time = 0  # Initial time
        
        states = ct.SolutionArray(gas, extra=['time_ms'])  # Preparing solution array for each state
        loop_counter = 0

        for n in range(time_steps):
            time += step_time
            sim.advance(time)
            states.append(r.thermo.state, time_ms=time / step_time)

            # Time for achieving (initial temperature + 400K)
            if (states.T[n] >= (T + 400)) and loop_counter == 0:
                Auto_ig_time.append(states.time_ms[n])
                loop_counter = 1

    print (Auto_ig_time)
    return Auto_ig_time

# Parameters
temp = np.linspace(950, 1400, 9)  # Initial temperature in K
P = 5 * 101325  # Initial pressure in Pa
simulation_time = 10  # seconds
step_time =  0.001  # seconds

# Fuels and their compositions
fuels = {
    'methane': {'CH4': 1, 'O2': 2},
    'hydrogen': {'H2': 1, 'O2': 2},
}

colors = {
    'methane': 'blue',
    'hydrogen': 'red',
}

plt.figure()

# Run simulations for each fuel
for fuel, species_dict in fuels.items():
    Auto_ig_time = run_simulation(fuel, species_dict, temp, P, simulation_time, step_time)
    plt.plot(temp, Auto_ig_time, '-o', color=colors[fuel], label=fuel)

# Plot settings
plt.grid(True)
plt.xlabel('Initial temperature [K]')
plt.ylabel('Autoignition delay [ms]')
plt.title('Autoignition delay for variable initial temperature')
plt.legend()
plt.show()

exit ()
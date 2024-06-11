import cantera as ct
import numpy as np
import matplotlib.pyplot as plt

def run_simulation(fuel, species_dict, pressure, T, simulation_time, step_time):
    time_steps = int(simulation_time / step_time)
    Auto_ig_time = []  # Array for autoignition delay

    for i in pressure:
        gas = ct.Solution('gri30.yaml')
        P = i * 101325  # Converting pressure from atm to Pa
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
pressure = np.linspace(0.5, 5, 9)  # Initial pressure in atm
T = 1000  # Initial temperature in Kelvin
simulation_time = 10  # seconds
step_time = 0.001 # seconds

# Fuels and their compositions
fuels = {
    'methane': {'CH4': 1, 'O2': 2},
    'hydrogen': {'H2': 2, 'O2': 1},

}

colors = {
    'methane': 'blue',
    'hydrogen': 'red',
}

plt.figure()

# Run simulations for each fuel
for fuel, species_dict in fuels.items():
    Auto_ig_time = run_simulation(fuel, species_dict, pressure, T, simulation_time, step_time)
    plt.plot(pressure, Auto_ig_time, '-o', color=colors[fuel], label=fuel)

# Plot settings
plt.grid(True)
plt.xlabel('Pressure [atm]')
plt.ylabel('Autoignition delay [ms]')
plt.title('Autoignition delay for variable initial pressure')
plt.legend()
plt.show()

exit()
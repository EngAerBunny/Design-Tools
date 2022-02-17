This code was originally written in MATLAB by prof. Frederico Afonso (IST) and later,
converted to python.

This version in python allows the use of multi-objective optimisation algorithms to quickly
explore the design space. To do so, pymoo framework is used.

The general workflow of the code is given in our AeroBest Conference paper, which can be found at:
https://aerobest2021.idmec.tecnico.ulisboa.pt/wp-content/uploads/2021/10/AeroBest2021_proceedings.pdf
pp 290
'Design of a Hydrogen Small Electric Fixed-Wing UAV With VTOL Capability'

main.py is an example of how the pymoo framework can be used to perform multi-objective optimisation with our numerical program
analysis_02.py is an example of how analysis can be executed (without optimisation)
aircraft_data.py contains some constants that must be provided and cannot be used as design variables in the optimisation problem
input_classes.py contains all the classes needed with the exception of the mission segments
segments folder contains all the typical mission segments that can be instantiated such as vertical climb, conventional climb, cruise, glide, etc.

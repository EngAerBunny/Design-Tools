Blade Element Theory Folders

Contain all the BET analyses from the 22x12 and 21x13 propellers in differents RPM.
The procedure is similar for the other propellers.
Base Literature: GENERAL AVIATION AIRCRAFT DESIGN:APPLIED METHODS AND PROCEDURES 
		 from SNORRI GUDMUNDSSON  

Introduce initial values:

Forward Speed, RPM, Propeller Diameter, Geometric Pitch, Number of blades
Air density, Air temperature, Air viscosity, Hub Geometry 

Divide the blade into X segments, knowing their position, cord and blade angle.

For each segment calculate Mach number, flow angle, relative velocity and Reynolds number

For each segment calculate Cl and Cd using XFLR5 or other software.

Calculate the induced angle of attack.

Final Procedure: Calculate Thrust, Torque and Power for each segment and 
		 add it all applying the Prandtl Correction . 
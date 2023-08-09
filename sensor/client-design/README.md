# Physical Design

Note: This design relies on an exteranl 12V power supply, either thruough the barrel or USB-PD
## File structures

`/Casing`     	The case of the new design. Open file located at `.../ver2/assembly2.prt`

`/KiCad`       	New Sensor Client's schematic and PCB design. Feel free to ignore .../ESP32Sensor-Archive
		All the schematic libs symboles are located in .../External Lib/KiCADv6
		All the footprints are located in .../External Lib/Library.pretty and .../External Lib/footprints.pretty

`/LTspice`     	Electrical simulation (Differ from real life situation for some reason)

## Design images

![flowchart drawio](https://github.com/LESA-RPI/hfs.main/assets/28797384/69c74000-fc72-4a3c-9aa4-87a0a1a7c524)
![assemblyver2](https://github.com/LESA-RPI/hfs.main/assets/28797384/67aaf320-4399-4c72-831c-aa4d6f5ddcf8)




The PCB was designed in KiCad. Needs to import all libs located in `\KiCad\External Lib` before opening and editing. For each components, if you want to see them in 3D viewer, you would needs to reassign 3D Models in Footprints Properties.

Delete the exisitng project specific libs and re-import them


- `KiCad\External Lib\KiCADv6` are where the symbols located. Delete the legacy one if multiple libs are sharing the same name

- `KiCad\External Lib\KiCADv6\footprints.pretty` & `KiCad\External Lib\Library.pretty` are where hte footprints located
  
- `KiCad\External Lib\3D` are where the 3D models located at

The new casing design is located in `Casing\Ver2\assembly2.prt`

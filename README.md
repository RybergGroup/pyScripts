# pyScripts
Some potentially useful Python scripts

## getSocken.py
The getSocken.py script was written by ChatGPT with minor changes.
It depend on geopandas (pip install geopandas) and the database sockenstad.gpkg (provided by Lantmäterriet under CC0).
Thi input file should be given as only argument to the script, e.g. ```python3 getSocken.py my_coordinates.csv```.
The CSV file should be comma separated with at least a longitude and latitude heading (see points.csv for an example).

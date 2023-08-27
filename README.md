# UBlox GPS project
Small project that retrieves gps information from a ublox 5 module, with a flask REST api to retrieve the coordinates in a json format and a simple webpage to display the data and show the position on a map. This project is developed to be run on a raspberry pi.

The code is split up into two parts, the flask REST api, in the `main.py` file and gps manager in the `gps.py` file. The information between the api calls from the webserver and gps information is shared through redis.

The code containing the flask code renders a simple page on the main route (the map shown is from leaflet) and the api GET call in the `api/coordinates` route to retrieve the coordinates, or null if the coordinates is unknown.
The map will be blank if the coordinates are unknown, and the latitude and longitude will be shown as "INVALID".

The gps code communicates with the ublox gps module through a serial connection and shows the status through an LED diode (blinking=waiting for signal, solid=signal found).

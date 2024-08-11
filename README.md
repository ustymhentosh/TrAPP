# TrAPP 

<img src="images/icon77.png" alt="image" width="100" height="auto">

Utility program for working with lviv transport data

#### 1. Installation
In the archive together with this manual is the main folder of the program. Unzip the folder and place it on your drive in any convenient location. After this ease of use, and for your device to recognize the new app, create a Shortcut in the location where you plan to have access to the app. The shortcut should refer to the <span style="color:#00b050">trapp.exe</span> file in the previously unzipped folder. Next, launch the program via the Shortcut.

#### 2. Data
The application works with monthly reports on visits to public transport stops in Lviv. You need to have a folder with `.xlsx` files for the routes you want to analyze. The files must be named according to the route number. Each file must follow the format:
lines 1,2,3,4 - header
line 5 - the name of the columns
lines 6 and on - date
- column 1 = stop name,
- column 2 = time of arrival in year/month/day h:min format
example:
<span style="color:#ff0000">the format of the data column is critical!</span>

#### 3. Launch and calculation
When the program is launched for the first time, a menu will appear with the option of the selected data folder. Select the required folder and click "Next". This step is necessary to clean and analyze the provided files, the calculation window contains a progress bar. This process may take several minutes. After completion, the functional program will be available.

During subsequent launches, the program has the ability to use already existing data, or to calculate new ones for another month.

#### 4. Use
The program contains two tabs Routes and Stops.
- On the "Routes" tab, you need to enter the route number, the starting and ending stops, and the days for displaying statistics. Click "get" to generate a graph of the time taken by a given vehicle to cover a given path at the current time based on the time of receipt. After highlighting the graph, there is an option to save it. There is also a map icon next to the number selection field, click on it to show all the stops of this route on the map and their names when hovering.
- On the "Stops" tab, you need to check the name of the stop, the desired route on it, as well as the day of the week and the collection period for statistics. The generated schedule shows the intervals between the arrival of the selected transport at the selected stop.

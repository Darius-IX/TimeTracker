# TimeTracker
Easily track the time for different projects. Add notes for every session to keep track of your progress.
## Usage
Run main.py or
## Create Windows Executable
In cmd:
- pip install pyinstaller
- pyinstaller --onefile --noconsole main.py\
\
Use the .exe file created in the dist directory and move it in the wished directory. A JSON file for storing the time will be created in the same directory.
## How does it work?
- Enter a project name below "Add or Remove Project", then press the Button
- Click "Start" or press enter to start time measurement
- Click "Stop" or press enter again to stop the measurement
- Add notes for every session, you may leave them empty and store that decision individually for each project
- The times are stored in the JSON. You can make modifications by hand

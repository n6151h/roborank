# roborank
A system I developed for my neice to help her choose allies in robotics competitions

Installation
------------

* Clone this repository and cd into the `roborank` directory.

* Create a virtual environment: `virtualenv -p python3 venv`

* Activate the virtual environment: `source venv/bin/activate`  (on windows: `venv\Scripts\activate.bat`)

* Run `pip install -r requirements.txt` to install the required packages.

* Set `export FLASK_APP=roborank.py` environment variable.

* Run `flask run` to start the application.

* Navigate to `http://localhost:8900/` to use *roborank*

***Remember to kill all the robots with fire when you're finished!!***

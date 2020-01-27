# roborank
My neice, now a high school student,  is *seriously* into robotics, and participates in robot competitions wherein teams compete, individually and in *alliances*
of 2 or more teams (each team having a robot that can perform one or more -- but not all -- of several tasks.)  

She needed a way to evaluate the scores of the teams to determine which of them would be optimal to pair with, taking into account which robots do well at
tasks her robot either isn't designed to do, or doesn't do well. The idea is that the alliance should be made up of robots that perform complementary tasks.

This isn't as easy as it sounds.

This app lets her set up entries for each team, and quickly record each team's performance in multiple rounds, across the several tasks.  The 
data are then aggregated across the rounds (mean and variance).  The aggregate scores are then passed to a scoring function which reduces these to
a scalar value for each grouping of potential alliances which is used to sort the teams from best to worst in future rounds.

It is possible that a team may have already allied with someone else, so, there must also be a way to quickly exclude that team (and any that roborank
paired it with in deriving the scores) from further consideration.


Installation
------------

* Clone this repository and cd into the `roborank` directory.

* Create a virtual environment: `virtualenv -p python3 venv`

* Activate the virtual environment: `source venv/bin/activate`  (on windows: `venv\Scripts\activate.bat`)

* Run `pip install -r requirements.txt` to install the required packages.

* Set `export FLASK_APP=main.py` environment variable.

* Run `flask run` to start the application.

* Navigate to `http://localhost:5000/` to use *roborank*

***Remember to kill all the robots with fire when you're finished!!***

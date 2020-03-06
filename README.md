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

## Pre-installation

* Install [python 3.6 or later](https://www.python.org/downloads/) on your computer, if it isn't there already. 
    If you're doing this on Windows, make sure to check the box that asks if you want to add this to your `PATH`.

* Make sure you have the latest version of pip:

~~~sh
pip install -U pip
~~~

* Install virtualenv on your computer.

~~~sh
pip install virtualenv
~~~

* Create a directory to contain roborank.  
    - linux: `mkdir ~/roborank`
    - windows: `mkdir C:\roborank`
    
* CD into that directory and create a virtualenv virtual environment:

~~~sh
virtualenv  venv
~~~
    
* Activate the virtual environment
    - linux: `. venv/bin/activate` 
    - windows (cmd.exe): `venv\Scripts\activate.bat`
    - windows (powershell): `venv\Scripts\activate.ps1` 
    
    You should now see a `(venv)` prefix on your prompt.  (Note: You might not. Try running `python` and make sure it's the version you think you installed.)

## Installation

* Clone this repository and cd into the `roborank` directory.

~~~sh
git clone git@github.com:n6151h/roborank.git
~~~

* Install the python modules required

~~~sh
pip install -r requirements.txt
~~~


### Web App 

This provides a web front-end to the scoring logic.  You don't have to (and probably shoulld **NOT**) run
this on some host somewhere.  It has ZERO authentication (i.e. no login accounts) of any sort.  It's meant to
have the server running on the same machine as the browser being used to access it.  

**Any other configuration is done at your own risk!**

To run it:

* Set the `FLASK_APP` environment variable:
   - linux:`export FLASK_APP=run.py` 
   - windows: `set FLASK_APP=run.py`

* Set the `FLASK_ENV` environment variable:
   (This will give you more debug output in the shell window.)
   - linux: `export FLASK_ENV=development`
   - windows: `set FLASK_ENV=development`
* 
* Start the application:
~~~sh
flask run
~~~

* In your browser, navigate to `http://localhost:5000/` to use *roborank*

### Command Line Utility (CLU) 

This was written mainly to test the scoring logic without having to deal with entering data into 
the website or database.  This has since been superceded by the web app
.
Run `clu.py` with the `-h` or `--help` switch to see the other
options available.

Very basic usage:  `clu.py some-scoring-sheet.xlsx` will score the contents and write it to a file named 
`some-scoring-sheet-output.xlsc`.  You can output a few other formats, too, like csv, json, and html.

The spreadsheet should have 10 columns: Rating, Team Id, Team Name, Balls High, Balls Low, Spinner Colour, Spinner Rotation,
Climb, Autonomous, and Round (number).  There may be multiple rounds in a single scoring file.



***Remember to kill all the robots with fire when you're finished!!***

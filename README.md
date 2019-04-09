# Chatbot API

## Installation steps:
> **Note:** Currently we support **Linux** and **Windows** platforms and **Python 3.6**.

> **Note:** Windows platform requires Git for Windows (for example, git), Visual Studio 2015/2017 with C++ build tools installed.

> **Warning:** **Python 3.5 is not supported!**.

 1. Clone this repo
 `git clone https://github.com/padfoot18/Chatbot.git`

 2. Create a virtual environment with Python 3.6: 
 `python3 -m virtualenv venv`
 
 3. Activate the environment:
 	- **Linux:** `source env/bin/activate`
	- **Windows:** `.\env\Scripts\activate.bat`
		 
 4. Install the required packages from `requirements.txt` inside this virtual environment:
	 `pip install -r requirments.txt`
	 
 5. Install Git Large File Storage from `https://git-lfs.github.com/`
 
 6. Download lstm and glove model:
    `git lfs pull`
    
## Usage Instructions:
 1. Activate the environment:
 	- **Linux:** `source env/bin/activate`
	- **Windows:** `.\env\Scripts\activate.bat`
	
 2. Run app2.py script:
    `python app2.py`
 
 3. For chat bot, open `popup.html` in any browser
 
 4. For admin site, open `http://localhost:5000/` in any browser
	 

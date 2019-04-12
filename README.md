# SAHEB
### (Somaiya Admission Help and Enquiry Bot)  

## Installation steps:
> **Note:** Currently we support **Linux** and **Windows** platforms and **Python 3.6**.

> **Note:** Windows platform requires Git for Windows (for example, git), Visual Studio 2015/2017 with C++ build tools installed.

> **Warning:** **Python 3.5 is not supported!**.

## Installation:

 1. Install Git Large File Storage from `https://git-lfs.github.com/` (this is required bcs the ML models are stored on Git-lfs cloud) 

 2. Clone this repo
 `git clone https://github.com/padfoot18/Chatbot.git`
 
 3. Change directory
 `cd SAHEB/`

 4. Create a virtual environment with Python 3.6: 
 `python3 -m virtualenv venv`
 
 5. Activate the environment:
 	- **Linux:** `source venv/bin/activate`
	- **Windows:** `.\venv\Scripts\activate.bat`
		 
 6. Install the required packages from `requirements.txt` inside this virtual environment:
	 `pip install -r requirements.txt`
 
    
## Usage Instructions:
 1. Activate the environment:
 	- **Linux:** `source venv/bin/activate`
	- **Windows:** `.\venv\Scripts\activate.bat`
	
 2. Run app.py script:
    `python app.py`
    > **Note:** For first run, this may take a while depending on your network connection as it downloads the required files(around 2GB).
 
 3. For chat bot, open `frontend/popup.html` in any browser
 
 4. For admin site, open `http://localhost:5000/` in any browser
	 

# How to run
1. Make sure you have a working Python 3 installation
2. Run `pip install -r requirements.txt`
3. Sign up for a Twitter developer account and create a Twitter app, as described in [this guide](https://python-twitter.readthedocs.io/en/latest/getting_started.html).
4. Copy `.env.example` to `.env` and fill in the listed values. 
5. Run `python New-Tweet-Collector.py` and wait while it gathers results. You can leave the program running for as long as you would like. Collected data will be placed into a new or existing `output.csv` file, with new data appended if the file already exists.  
6. When you would like to stop the program, press `Control+C` or close the terminal. 
7. View results in `outputfile.csv`

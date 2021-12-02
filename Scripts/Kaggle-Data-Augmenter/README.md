# How to run
1. Make sure you have a working Python 3 installation
2. Run `pip install -r requirements.txt`
3. Sign up for a Twitter developer account and create a Twitter app, as described in [this guide](https://python-twitter.readthedocs.io/en/latest/getting_started.html).
4. Copy `.env.example` to `.env` and fill in the listed values. 
5. Run `python Kaggle-Data-Augmenter.py inputfile.csv outputfile.csv`, where `inputfile.csv` is the CSV from the Kaggle dataset, and `outputfile.csv` is where you want the newly generated data to be stored. The output file will be overwritten. 
6. Wait for the program to finish running.
7. View results in `outputfile.csv`

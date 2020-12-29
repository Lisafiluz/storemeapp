from  dotenv import load_dotenv
load_dotenv()

# OR, the same with increased verbosity
# load_dotenv(verbose=True)

# OR, explicitly providing path to '.env'
# from pathlib import Path  # Python 3.6+ only
# env_path = Path('.') / '.env'
# load_dotenv(dotenv_path=env_path)


import os
SECRET_KEY = os.getenv("EMAIL")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

# import os

# os.environ['SECRET_KEY'] = '2a6352e066e2360e8169b91e4d3e8a5f'
# os.environ['DATABASE_URL'] = 'postgres://mxpgrlxlxcnfwg:dc13c53fa5d3742a094ecf2e607494270d87ebaadfc5f0c5a23d2c9977c8bb5f@ec2-54-237-155-151.compute-1.amazonaws.com:5432/d3nlt1fikgsico'
# os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 

#for development to use > command line > 
#export DATABASE_URL='sqlite:///site.db'
#export SECRET_KEY='2a6352e066e2360e8169b91e4d3e8a5f'

# SECRET_KEY, SQLALCHEMY_DATABASE_URI, FLASK_ENV, FLASK_APP
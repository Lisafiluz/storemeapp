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

#for development to use > command line > 
#export DATABASE_URL='sqlite:///site.db'
#export SECRET_KEY='2a6352e066e2360e8169b91e4d3e8a5f'

# SECRET_KEY, SQLALCHEMY_DATABASE_URI, FLASK_ENV, FLASK_APP
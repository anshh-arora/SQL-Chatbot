import pandas as pd
from sqlalchemy import create_engine

# Database connection details
db_user = 'root'
db_password = 'ansh1529'
db_host = 'localhost'
db_name = 'store_data'
table_name = 'store_data_sheet'

# Create the SQLAlchemy engine
engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}')

# Read the CSV file into a pandas DataFrame
csv_file = 'store_data.csv'
data = pd.read_csv(csv_file)

# Remove any leading/trailing whitespace from column names
data.columns = data.columns.str.strip()

# Transfer data to MySQL
data.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

print("Data transferred successfully!")

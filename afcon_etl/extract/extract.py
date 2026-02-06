import pandas as pd
from pathlib import Path

mod_path = Path(__file__).parent
csv_path = mod_path / "../../data/afcon-2025-MoroccoStandardTime.csv"
path = csv_path.resolve()

def extract_data():

	df = pd.read_csv(path)

	head = df.head()
	shape = df.shape
	columns = df.columns

	print("==================Printing the head:==================")
	print(head)
	print("==================Printing the shape:==================")
	print("Shape = ", shape)
	print("==================Printing the columns:===============")
	print("Columns = ", list(columns))

	print("Data extracted successfully!")

	return df

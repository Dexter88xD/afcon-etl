import pandas as pd

csv_path = "data/afcon-2025-MoroccoStandardTime.csv"

def extract_data():

	df = pd.read_csv(csv_path)

	head = df.head()
	shape = df.shape
	columns = df.columns

	print("==================Printing the head:==================")
	print(head)
	print("==================Printing the shape:==================")
	print("Shape = ", shape)
	print("==================Printing the columns:===============")
	print("Columns = ", list(columns))

	return df

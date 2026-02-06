import pandas as pd


def transform_data(df):

	clean_df = df.copy()

	clean_df["Date"] = pd.to_datetime(clean_df["Date"], format="%d/%m/%Y %H:%M", errors="coerce")

	clean_df["year"] = clean_df["Date"].dt.year
	clean_df["month"] = clean_df["Date"].dt.month 
	clean_df["day"] = clean_df["Date"].dt.day
	clean_df["time"] = clean_df["Date"].dt.time

	clean_df = clean_df.drop(columns=["Date"])

	clean_df = clean_df.fillna(value=None)

	clean_df = clean_df.drop_duplicates()

	print("Data transformed successfully!")

	return clean_df

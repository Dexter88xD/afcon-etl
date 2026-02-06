from extract.extract import extract_data
from transform.transform import transform_data
from load.load import load_data

def main():
	try:
		df = extract_data()
		clean_df = transform_data(df)
		load_data(clean_df)
	except Exception as e:
		print("Error:", e)

if __name__ == "__main__":
    main()
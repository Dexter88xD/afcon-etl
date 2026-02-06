import psycopg2

def load_data(clean_df):

	conn = psycopg2.connect(
		dbname = "afcon_db",
		user = "dexter",
		password = "123",
		host = "localhost",
		port = "5432"
	)
	cur = conn.cursor()
	insert_query = """
	INSERT INTO matches
	(match_number, round_number, match_year, match_month, match_day, match_time,
	location, home_team, away_team, group_name, result)
	VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
	ON CONFLICT (match_number) DO UPDATE
	SET round_number = EXCLUDED.round_number,
		match_year = EXCLUDED.match_year,
		match_month = EXCLUDED.match_month,
		match_day = EXCLUDED.match_day,
		match_time = EXCLUDED.match_time,
		location = EXCLUDED.location,
		home_team = EXCLUDED.home_team,
		away_team = EXCLUDED.away_team,
		group_name = EXCLUDED.group_name,
		result = EXCLUDED.result;
	"""


	for idx, row in clean_df.iterrows():
		cur.execute(insert_query, (
			row['Match Number'],
			row['Round Number'],
			row['year'],
			row['month'],
			row['day'],
			row['time'],
			row['Location'],
			row['Home Team'],
			row['Away Team'],
			row['Group'],
			row['Result']
	))

	
	conn.commit()
	print("Data loaded successfully!")

	cur.close()
	conn.close()
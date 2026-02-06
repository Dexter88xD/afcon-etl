# AFCON 2025 ETL Pipeline

A production-ready, but basic, Extract-Transform-Load (ETL) pipeline for processing AFCON 2025 (Africa Cup of Nations) football match data into a PostgreSQL database.

## 📋 Project Overview

This ETL pipeline automates the process of:
- **Extracting** match data from a CSV file
- **Transforming** the data by parsing dates and structuring it for database storage
- **Loading** the processed data into a PostgreSQL database

The pipeline is designed to be robust, with comprehensive error handling, data validation, and verification mechanisms.

---

## 🏗️ Project Structure

```
afcon-etl/
├── afcon_etl/
│   ├── main.py          # Main orchestrator / entry point
│   ├── extract/
│   │   ├── __init__.py
│   │   └── extract.py       # Data extraction logic
│   ├── transform/
│   │   ├── __init__.py
│   │   └── transform.py     # Data transformation logic
│   └── load/
│       ├── __init__.py
│       └── load.py          # Data loading logic
├── data/
│   └── afcon-2025-MoroccoStandardTime.csv  # Input data
├── requirements.txt          # Python dependencies
└── README.md               # This file
```

---

## 🔧 Dependencies

- **pandas** (3.0.0) - Data manipulation and CSV reading
- **psycopg2** (2.9.11) - PostgreSQL database adapter
- **python-dateutil** (2.9.0.post0) - Date/time utilities

### Full Requirements
See `requirement.txt` for complete list of all dependencies.

---

## 📥 Installation

### 1. Clone/Setup the Project
```bash
cd /home/dexter/work/afcon-etl
```

### 2. Create Virtual Environment (Optional but Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirement.txt
```

### 4. Configure Database Connection
Edit `afcon_etl/load/load.py` and update the connection parameters:
```python
conn = psycopg2.connect(
    dbname="afcon_db",      # Your database name
    user="user",          # Your database user
    password="123",         # Your database password
    host="localhost",       # Your database host
    port="5432"            # Your database port
)
```

### 5. Create Database Table
```sql
CREATE TABLE matches (
    match_number INTEGER PRIMARY KEY,
    round_number TEXT,
    match_year INTEGER,
    match_month INTEGER,
    match_day INTEGER,
    match_time TIME,
    location VARCHAR(255),
    home_team VARCHAR(100),
    away_team VARCHAR(100),
    group_name VARCHAR(50),
    result VARCHAR(50)
);
```

---

## 🚀 Usage

### Run the ETL Pipeline
```bash
# Run main script directly
python3 afcon_etl/main.py
```

### Expected Output
```
==================Printing the head:==================
   Match Number Round Number              Date ...
0             1            1  21/12/2025 20:00 ...
1             2            1  22/12/2025 15:00 ...
...

==================Printing the shape:==================
Shape =  (52, 8)

==================Printing the columns:===============
Columns =  ['Match Number', 'Round Number', 'Date', 'Location', ...]

Data extracted successfully!
Data transformed successfully!
Data loaded successfully! 52 records inserted.
```

---

## 📊 Data Flow Architecture

```
CSV File
   ↓
extract_data() 
   ├─ Reads CSV using pandas
   ├─ Displays head, shape, columns
   └─ Returns DataFrame
   ↓
transform_data()
   ├─ Copies DataFrame
   ├─ Parses Date column (DD/MM/YYYY HH:MM format)
   ├─ Extracts: year, month, day, time
   ├─ Removes original Date column
   ├─ Handles NULL values
   ├─ Removes duplicates
   └─ Returns cleaned DataFrame
   ↓
load_data()
   ├─ Connects to PostgreSQL
   ├─ Iterates through rows
   ├─ Inserts/updates data (ON CONFLICT)
   ├─ Verifies row count
   ├─ Commits transaction
   └─ Closes connection
   ↓
Database ✓
```

---

## 📁 Module Descriptions

### **extract.py**
**Purpose:** Read data from CSV file

**Key Features:**
- Directory-independent file path using `Path(__file__).parent`
- Displays data preview (head, shape, columns)
- Returns pandas DataFrame

**Function:** `extract_data() → DataFrame`

---

### **transform.py**
**Purpose:** Clean and structure data for database storage

**Transformations:**
- Converts Date string to datetime (format: `%d/%m/%Y %H:%M`)
- Extracts year, month, day, and time as separate columns
- Removes original Date column
- Fills NULL values
- Removes duplicate rows

**Function:** `transform_data(df: DataFrame) → DataFrame`

---

### **load.py**
**Purpose:** Insert processed data into PostgreSQL

**Key Features:**
- Secure PostgreSQL connection
- `INSERT ... ON CONFLICT` for idempotent operations
- Try/except/finally error handling
- Safe cleanup (checks if variables exist before closing)
- Verification query: confirms 52 records inserted
- Dynamic count verification using `clean_df.shape[0]`

**Function:** `load_data(clean_df: DataFrame) → None`

---

### **main.py**
**Purpose:** Orchestrate the ETL pipeline

**Features:**
- Imports all ETL functions
- Wires functions in correct order
- Central error handling
- Clean exit on success or error

---

## ✅ Data Validation

The pipeline includes multiple validation checkpoints:

1. **Extract Phase**
   - Verifies CSV file exists
   - Checks data shape (52 rows × 8 columns)

2. **Transform Phase**
   - Validates date parsing (handles coerce errors)
   - Removes duplicates
   - Fills NULL values

3. **Load Phase**
   - Verifies database connection
   - Checks row count matches expected (52 records)
   - Displays error if count mismatch

---

## 🔐 Error Handling

The pipeline implements comprehensive error handling:

### Extract Level
```python
# Validates file path using Path(__file__)
# Catches CSV reading errors
```

### Transform Level
```python
# Handles invalid date formats with errors="coerce"
# Safely handles NULL values
```

### Load Level
```python
try:
    # Connection and data insertion
except Exception as e:
    # Catches DB errors, constraint violations, etc.
finally:
    # Always closes connections safely
```

---

## 🐛 Troubleshooting

### Error: `ModuleNotFoundError: No module named 'pandas'`
**Solution:**
```bash
pip install -r requirement.txt
```

### Error: `psycopg2.OperationalError: could not connect to server`
**Check:**
- PostgreSQL is running
- Database credentials are correct in `load.py`
- Database host/port are correct

### Error: `FileNotFoundError: [Errno 2] No such file or directory`
**Check:**
- CSV file exists at `data/afcon-2025-MoroccoStandardTime.csv`
- Run from project root directory: `/home/dexter/work/afcon-etl`

### Error: `relation "matches" does not exist`
**Solution:**
- Create the database table using the SQL provided in Installation section

---

## 📈 Features

✅ **Robust Error Handling** - Try/except/finally blocks throughout  
✅ **Data Validation** - Verifies row counts and data integrity  
✅ **Directory-Independent** - Works from any execution directory  
✅ **Idempotent Operations** - Uses ON CONFLICT for safe re-runs  
✅ **Clean Code** - Separated concerns (extract, transform, load)  
✅ **Production Ready** - Error messages and status reporting  

---

## 📝 Sample Data

The dataset contains AFCON 2025 match information:
- **52 matches** from group stage through finals
- **Dates:** December 21, 2025 - January 18, 2026
- **Columns:** Match Number, Round, Date, Location, Teams, Group, Result

### Example Record
```
Match Number: 1
Round Number: 1
Date: 21/12/2025 20:00 → year: 2025, month: 12, day: 21, time: 20:00:00
Location: Stade Prince Moulay Abdellah
Home Team: Morocco
Away Team: Comoros
Group: Group A
Result: 2 - 0
```

---

## 🔄 Pipeline Run Example

```bash
$ python3 afcon_etl/main.py

==================Printing the head:==================
   Match Number Round Number              Date  ... Away Team    Group Result
0             1            1  21/12/2025 20:00  ...   Comoros  Group A  2 - 0
1             2            1  22/12/2025 15:00  ...    Zambia  Group A  1 - 1
[5 rows × 8 columns]

==================Printing the shape:==================
Shape =  (52, 8)

==================Printing the columns:===============
Columns =  ['Match Number', 'Round Number', 'Date', 'Location', 'Home Team', 'Away Team', 'Group', 'Result']

Data extracted successfully!
Data transformed successfully!
Data loaded successfully! 52 records inserted.
```

---

## 🎯 Next Steps / Enhancements

Possible future improvements:
- Add logging to file instead of just print statements
- Implement data quality checks (validate team names, dates)
- Add support for incremental loads (only new matches)
- Schedule pipeline runs with cron/Task Scheduler
- Add data rollback functionality
- Implement metrics/monitoring (execution time, row counts)
- Add configuration file for database credentials

---

## 📄 License

This project is part of the AFCON ETL Pipeline learning/demo project.

---

**Last Updated:** February 6, 2026  
**Version:** 1.0  
**Status:** ✅ Production Ready

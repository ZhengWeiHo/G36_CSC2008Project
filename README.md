# G36_CSC2008Project

This project contains a web application for managing and visualizing datasets. It supports both SQLite and MongoDB databases.

## Usage

Follow the steps below to set up and run the application. If you already have the necessary CSV files and database file, you can skip to step 3.

### 1. Generate datasets

To generate CSV files as datasets, run the following script:

python generateData.py

### 2. Insert data into the database

To insert data from the CSV files, run the `G36_DB.ipynb` Jupyter Notebook:

G36_DB.ipynb

### 3. Launch the web application

To start the web application, run the following script:

python main.py

### 4. Visualize performance data

To visualize the performance of queries, run the `Performance-Analysis.ipynb` Jupyter Notebook:

Performance-Analysis.ipynb

### 5. Migrate data to MongoDB

To migrate data from SQLite to MongoDB, run the `MongoDB-Migration.ipynb` Jupyter Notebook:

MongoDB-Migration.ipynb

## Team Members

| S/N | Name                        | Student ID | Email                            |
| --- | --------------------------- | ---------- | -------------------------------- |
| 1   | Ho Zheng Wei                | 2102580    | 2102580@sit.singaporetech.edu.sg |
| 2   | Quek Ser Wee, Darren        | 2102593    | 2102593@sit.singaporetech.edu.sg |
| 3   | Tan Wen Yang                | 2101119    | 2101119@sit.singaporetech.edu.sg |
| 4   | Perpetua Sorubha Raj        | 2101771    | 2101771@sit.singaporetech.edu.sg |
| 5   | Zamora Zchyrlene Mae Prades | 2101402    | 2101402@sit.singaporetech.edu.sg |
| 6   | Munigal Do Paramasivam      | 2102176    | 2102176@sit.singaporetech.edu.sg |

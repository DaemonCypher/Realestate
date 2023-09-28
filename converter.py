import sqlite3
import csv
from database_helper import *
from collections import Counter
from dateutil.relativedelta import relativedelta
from datetime import datetime

valid_conn = sqlite3.connect("validAddress.db")
results = fetch_from_db(valid_conn, 'validAddress')
length_frequencies = Counter(len(row[3]) for row in results)

# Find the most common length
most_common_length = length_frequencies.most_common(1)[0][0]

# Assume the data_date is in the format 'YYYY-MM-DD HH:MM:SS.ssssss'
# Convert the data_date string to a datetime object
data_date_dt = datetime.strptime(results[0][6], '%Y-%m-%d %H:%M:%S.%f')

# Create header by counting backwards by 1 month starting from the last element in history
header = ['Address']+[(data_date_dt - relativedelta(months=i)).strftime('%Y-%m') for i in range(most_common_length - 1, -1, -1)] + ['Status', 'Data Date']

# Modify results to spread the history values across multiple columns for each row,
# but only for rows with the most common history length
modified_results = []
for id, address, city, history, status, status_date, data_date in results:
    if len(history) == most_common_length:
        modified_row = (address,*history, status, data_date)
        modified_results.append(modified_row)

with open('output.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)  # write the header
    writer.writerows(modified_results)  # write the data rows

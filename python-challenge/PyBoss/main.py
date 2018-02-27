#Import libraries
import csv
import os
import datetime
import re

#Get file path
file_valid = 0
while file_valid == 0:
    emp_data_path = input("Please enter path to employee data file: ")
    if os.path.isfile(emp_data_path):
        file_valid = 1
    else:
        print("Invalid path or file does not exist.")

#Declare variables
employee_list = []

#Define dictionary for State abbreviations
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

#Read from csv file
with open(emp_data_path, "r") as emp_data_file:
    emp_data_reader = csv.reader(emp_data_file, delimiter = ",")
    next(emp_data_reader) #Skip header
    for emp_data_row in emp_data_reader:
        name = emp_data_row[1].split()
        dob = datetime.datetime.strptime(emp_data_row[2], '%Y-%m-%d').strftime('%m/%d/%y') 
        ssn = re.sub(r'\d{3}-\d{2}', r'***-**', emp_data_row[3])
        employee_list.append([emp_data_row[0], name[0], name[1], dob, ssn, us_state_abbrev[emp_data_row[4]]])

#Print results and write to file
#Set output file path
emp_results_path = os.path.join('output', 'employee_results.csv')
#Open the file using "write" mode. Specify the variable to hold the contents
with open(emp_results_path, 'w', newline = '') as emp_results_file:
    #Initialize csv.writer
    csvwriter = csv.writer(emp_results_file, delimiter=',')
    #Write the first row (column headers)
    csvwriter.writerow(['Emp ID', 'First Name', 'Last Name', 'DOB', 'SSN', 'State'])
    
    for emp_results_row in employee_list:
        csvwriter.writerow(emp_results_row)
        
print("\n\nDone! You may view results in the output/employee_results.csv file.")

    

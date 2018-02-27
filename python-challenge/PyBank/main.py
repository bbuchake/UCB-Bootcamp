#Import modules
import csv
import os

#Get file path from user
budget_data_path = input("Please enter the file path: ")

#Declare variables
total_months = 0
total_revenue = 0
greatest_rev_increase = 0
rev_increase_month = ""
greatest_rev_decrease = 0
rev_decrease_month = ""

#Read from csv file
with open(budget_data_path, "r") as budget_data_file:
    budget_data_reader = csv.reader(budget_data_file, delimiter = ",")
    next(budget_data_reader) #Skip header
    #Calculate total months which is same as total number of rows in the file
    #total_months = len(list(budget_data_reader)) - *** When I ran this line, it worked but then the reader finished 
    #reading to the end of the line and the 'for' loop did not work
    for budget_data_row in budget_data_reader:
        #Calculate total revenue
        total_months = total_months + 1
        total_revenue = total_revenue + int(budget_data_row[1])
        if int(budget_data_row[1]) > greatest_rev_increase:
            greatest_rev_increase = int(budget_data_row[1])
            rev_increase_month = budget_data_row[0]
        else:
            greatest_rev_decrease = int(budget_data_row[1])
            rev_decrease_month = budget_data_row[0]
            
    avg_rev_change = int(total_revenue / total_months)
    
    
    print("Total months: " + str(total_months))
    print("Total revenue: " + str(total_revenue))
    print("Average revenue change " + str(avg_rev_change))
    print("Greatest revenue increase " + rev_increase_month + " " + str(greatest_rev_increase))
    print("Greatest revenue decrease " + rev_decrease_month + " " + str(greatest_rev_decrease))
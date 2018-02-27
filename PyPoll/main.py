#Import libraries
import csv
import os

#Get file path
file_valid = 0
while file_valid == 0:
    poll_data_path = input("Please enter path to poll data file: ")
    if os.path.isfile(poll_data_path):
        file_valid = 1
    else:
        print("Invalid path or file does not exist.")

#Declare variables
total_votes = 0
candidates = {}
winner = 0
winner_name = ""

#Read from csv file
with open(poll_data_path, "r") as poll_data_file:
    poll_data_reader = csv.reader(poll_data_file, delimiter = ",")
    next(poll_data_reader)
    for poll_data_row in poll_data_reader:
        total_votes = total_votes + 1 #Count total votes
        if not poll_data_row[2] in candidates.keys():
            candidates[poll_data_row[2]] = 1
        else:
            candidates[poll_data_row[2]] = candidates[poll_data_row[2]] + 1

#Print results and write to file
results_file = open("election_results.txt", "w")

print("\nElection Results\n----------------------------------------\nTotal votes: " + str(total_votes) + 
      "\n----------------------------------------\n")
results_file.write("\nElection Results\n----------------------------------------\nTotal votes: " + str(total_votes) + 
      "\n----------------------------------------\n")
#Now we have the dictionary, let's loop through it
for name, count in candidates.items():
    print(name + ": " + str(int(count/total_votes * 100)) + "% (" + str(count) + ")")
    results_file.write(name + ": " + str(int(count/total_votes * 100)) + "% (" + str(count) + ")\n")
    if count > winner:
        winner = count
        winner_name = name

print("\n----------------------------------------\nWinner: " + winner_name)
results_file.write("\n----------------------------------------\nWinner: " + winner_name)        
    
results_file.close()
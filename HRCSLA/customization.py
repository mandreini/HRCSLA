"""
Created on July, 2014
@author: ma56nin9 / Matt
Contact: ma56nin@hotmail.com
"""

import sys

version = "V 0.9"
    
def create_ban_file():
    b = open("ban_keywords.txt", 'w')
    b.write("#ban list. Add key words that you're chat uses to determine a banned verdict, case insensitive\n#can be used with other languages, e.g. bandido (banned in Portuguese)\n#notice: does not support non-alphanumeric characters\n#DO NOT change the name of this document. Doing so removes the capability\n#to categorize reports!!! Only alter text below this line.\nbanned\nb&\nb4nned")
    return b

def create_clean_file():
    c = open("clean_keywords.txt", 'w')
    c.write("#clean list. Add key words that your chat uses to determine a clean verdict, case insensitive\n#can be used with other languages, e.g. limpo (clean in Portuguese)\n#notice: doesnot support non-alpha numeric characters\n#DO NOT change the title of this document. Doing so will remove the ability\n#to categorize the reports!! Only alter text below this line.\nclean")
    return c
    
def open_files(): 
    try:
        b = open("ban_keywords.txt", 'r')
    except:
        print("ban_keywords.txt file not found, creating a new one...")
        b = create_ban_file()
        print("File successfully created with default ban verdicts.")
        b = open("ban_keywords.txt", 'r')
    
    try:
        c = open("clean_keywords.txt",'r')
    except:
        print("clean_keywords.txt file not found, creating a new one...")
        c = create_clean_file()
        print("File successfully created with default clean verdicts.")
        c = open("clean_keywords.txt",'r')
        
    ban_verdicts = []
    clean_verdicts = []
    
    for bline in b:
        if bline[0] != "#":
            ban_verdicts.append(bline.rstrip('\n'))
    for cline in c:
        if cline[0] != "#":
            clean_verdicts.append(cline.rstrip('\n'))
    
    b.close()
    c.close()
    
    return ban_verdicts, clean_verdicts
    
def add_to_database():
    try:
        f = open("reports_record.txt","r")
    except:
        print("File 'reports_record.txt' not found. \nAdd the reports from the HRCLM exported to notepad, then run again.")
        f = open("reports_record.txt","w")
        f.close()
        sys.exit()
    
    report_list = f.readlines()
    
    for i in range(len(report_list)):
        report_list[i] = report_list[i].strip("\n")
        report_list[i] = report_list[i].split("\t")
    

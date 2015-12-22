from astropy.io import ascii
import numpy as np
import datetime
import time
from time import strftime
import sys
import os
import glob
import calendar


def convert_epoch(x):
    t = (datetime.datetime( int((x.split(" ")[0]).split("-")[0]),  int(x.split(" ")[0].split("-")[1]),  int(x.split(" ")[0].split("-")[2]), int(x.split(" ")[1].split(":")[0]) ,   int(x.spl$
    return calendar.timegm(t.timetuple())

def convert_time(arr):
    return np.array([convert_epoch(x) for x in np.array(arr)])

def cat_string(list_of_files):
    if len(list_of_files)==0:
        iterator = np.array([])
    elif len(list_of_files)==1:
        iterator=list_of_files
    elif len(list_of_files)>=2:
        iterator = list_of_files

    output=""
    for x in range(0, len(iterator)):
        output = output+iterator[x]+" "
    return output[:-1]



while True:
    raw1_file_list = glob.glob("../BA/*.csv")
    raw2_file_list= np.array([x.split("/")[2] if "kismet" not in x else "-99" for x in raw1_file_list])
    raw3_file_list = raw2_file_list[raw2_file_list!="-99"]
    index_file_list = np.array([int(((x.split("-")[1]).split("."))[0]) for x in raw3_file_list])
    file_list= np.array([y[1] for y in sorted(zip(index_file_list, raw3_file_list),key=lambda x:x[0])])
    os.chdir("../BA")
    os.system("cat %s > ../hello_again/onelevel/real_time_combined_S.csv"%(cat_string(file_list)))
    os.chdir("../hello_again/")

    with open('./onelevel/real_time_combined_S.csv','r') as in_file, open('./onelevel/full_day_S.csv','w') as out_file:
        switch = 0
        out_file.write("Station MAC, First time seen, Last time seen, Power, # packets, BSSID \r")
        for line in in_file:
            if (line[0:5]=="Stati"):
                switch = 1
            if (line[0]=="\r"):
                switch = 0
            if switch==1:
                if line[0]!="\r":
                    if (line.split(",")[0]!="Station MAC"):
                        processed_line = line.split(",")[0]+","+ line.split(",")[1]+","+line.split(",")[2]+","+line.split(",")[3]+","+line.split(",")[4]+","+line.split(",")[5]+"\r"
                        out_file.write(processed_line)


    raffles = ascii.read("./onelevel/full_day_S.csv")

    raffles_data = np.array(zip(raffles['Station MAC'], convert_time(raffles['First time seen']), convert_time(raffles['Last time seen'])))

    sorted_raffles= sorted(raffles_data,key=lambda x: x[0])

    sorted_mac_r = np.array([x[0] for x in sorted_raffles])
    sorted_first_r = (np.array([x[1] for x in sorted_raffles], dtype=int))
    sorted_last_r = (np.array([x[2] for x in sorted_raffles], dtype=int))

    final_mac_r= np.array([sorted_mac_r[0]])
    final_first_r = np.array([sorted_first_r[0]])
    final_last_r = np.array([sorted_last_r[0]])

    for x in range(1, len(sorted_raffles)): #this does the sessioning
        if sorted_mac_r[x-1]!=sorted_mac_r[x]:
            final_first_r = np.append(final_first_r, sorted_first_r[x])
            final_mac_r = np.append(final_mac_r, sorted_mac_r[x])
            final_last_r = np.append(final_last_r, sorted_last_r[x])

        if (sorted_mac_r[x-1]==sorted_mac_r[x]) & (np.absolute(int(sorted_last_r[x-1])-int(sorted_first_r[x]))>300):
            final_first_r = np.append(final_first_r, sorted_first_r[x])
            final_mac_r = np.append(final_mac_r, sorted_mac_r[x])
            final_last_r = np.append(final_last_r, sorted_last_r[x])

        if (sorted_mac_r[x-1]==sorted_mac_r[x]) & (np.absolute(int(sorted_last_r[x-1])-int(sorted_first_r[x]))<=300):
            final_last_r[-1] = int(sorted_last_r[x])

    ascii.write([final_mac_r, final_first_r, final_last_r], names=['mac_by_session', 'first_seen', 'last_seen'], output='./local_database.dat')
    time.sleep(12*60*60) #this is how long we sleep before coming up with a new file for the sake of database writing

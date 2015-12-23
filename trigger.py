from __future__ import division
import smtplib
import os
import calendar
import time
import numpy as np
from astropy.io import ascii
import glob
from twilio.rest import TwilioRestClient

account_sid = ""
auth_token = ""
client = TwilioRestClient(account_sid, auth_token)

def writeFile():
if os.path.isfile("./sent_list.dat"):
    print "There is a SENT file that exists..."
else:
    ascii.write([ np.array([]), np.array([])], names=['mac','sent_time'], output='./sent_list.dat')

restricted_list = np.array(["00:26:75:BB:E9:40","BC:6C:21:02:FC:49","A8:8E:24:68:98:80","68:94:23:A4:6F:23","8C:3A:E3:45:88:C7","88:53:2E:B3:CC:98", "48:E9:F1:2A:C1:E3", "A0:18:28:2A:0F:5C"])

def mainCommand()
    while True:
        check_sent = glob.glob("./sent_list.*")
        if check_sent!=[]:
            sent_already = ascii.read("./sent_list.dat")
        else:
            sent_already = np.array([])

        if (os.path.isfile("./trigger.dat")):
            trigger_input = ascii.read("./trigger.dat")
            if len(trigger_input['mac'])>0:
                if len(sent_already["mac"])!=0:
                    trig_unique_1 = np.array([x if ((x not in sent_already['mac'])|( (x in sent_already['mac'])and(  np.max(sent_already['sent_time'][sent_already['mac']==x]) < calendar.timer.timegm(time.gmtime()) - 5*60))) else "-99" for x in trigger_input['mac']])
                    trig_unique_2 = ((trig_unique_1[trig_unique_1!="-99"]))
                else:
                    trig_unique_1 = trigger_input['mac']
                    trig_unique_2 = trig_unique_1

                if len(trig_unique_2)>0:
                    outbound_macs = np.array([])
                    outbound_time = np.array([])

                    for x in trig_unique_2:
                        if x not in restricted_list:
                            outbound_macs = np.append(outbound_macs, x)
                            outbound_time = np.append(outbound_time, (calendar.timegm(time.gmtime())) )
                            print_message = "Mac:%s, Last Visited:%s, Time Spent:%s minutes \n"%(x, time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(trigger_input['last_seen'][trigger_input['mac']==x]+ 8*60*60 )) , (trigger_input['time_spent'][trigger_input['mac']==x]))
                            print print_message
                        #   message = client.messages.create(
                #               body=print_message,
                #               to="",
                #               from_="")
                #           print message.sid

                    if len(sent_already)==0:
                        ascii.write([outbound_macs, outbound_time], names=['mac','sent_time'], output='sent_list.dat')
                    else:
                        ascii.write([np.append(sent_already['mac'], outbound_macs), np.append(sent_already['sent_time'],outbound_time)], names=['mac','sent_time'], output='sent_list.dat')

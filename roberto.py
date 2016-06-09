#!/usr/bin/python

print "\r\nWhat the... you're not made of Tuesday!\r\n"

import requests
import json
import socket,struct
import warnings
import os

warnings.filterwarnings("ignore", category=DeprecationWarning)
requests.packages.urllib3.disable_warnings()

auth_header={'X-AUTH-TOKEN':'carbonblackapitoken'}
for hashfile in os.listdir("./hashes"):
        with open("./hashes/"+hashfile) as f:
                hashlist=f.read().splitlines()
        for hash in hashlist:
                r=requests.get("https://ccarbonblackserver/api/v1/process?q=process_md5:"+hash,headers=auth_header,verify=False)
                myjson=json.loads(r.text)

                for hit in myjson["results"]:
                        if hit["netconn_count"] > 0:
                                print hit["path"]+" started on "+hit["start"]+" by "+hit["username"]+" on host "+hit["hostname"]
                                print "Connections made by "+hit["path"]+":"
                                r=requests.get("https://carbonblackserver/api/v1/process/"+str(hit["id"])+"/"+str(hit["segment_id"])+"/event",headers=auth_header,verify=False)
                                netconn=json.loads(r.text)
                                for conn in netconn["process"]["netconn_complete"]:
                                        thisconn=conn.split("|")
                                        conn_time=thisconn[0]
                                        remote_addr=socket.inet_ntoa(struct.pack('>L', long(thisconn[1])))
                                        remote_port=thisconn[2]
                                        protocol=thisconn[3]
                                        remote_host_name=thisconn[4]
                                        direction=thisconn[5]
                                        if direction=="true":
                                                direction="Outbound"
                                        else:
                                                direction="Inbound"

                                        if protocol=="6":
                                                protocol="TCP"
                                        elif protocol=="17":
                                                protocol="UDP"

                                        print conn_time+" "+remote_addr+" "+remote_port+" "+protocol+" "+remote_host_name+" "+direction
                                        r=requests.get("https://carbonblackserver/api/v1/process?q="+remote_addr,headers=auth_header,verify=False)
                                        conn_count=json.loads(r.text)
                                        print "\tThere have been "+str(conn_count["total_results"])+" connections to "+remote_addr
                                print "\r\n"
                        else:
                                print hit["path"]+" started on "+hit["start"]+" by "+hit["username"]+" on host "+hit["hostname"]

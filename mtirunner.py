#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import os

def createDataDir(datadir):
    """Creates directory with tor instance data"""
    try:
        os.mkdir(datadir.split("/")[1])
    except OSError:
        print("Data directory exists")

def formCommand(bsp, bcp, datadir, i):
    """Forms a command to run tor according to user input"""
    r = "tor --RunAsDaemon 1 --CookieAuthentication 0 --HashedControlPassword"
    r += " \"\" " + "--SocksPort " + str(bsp) + " --ControlPort " + str(bcp)
    r += " --DataDirectory " + datadir + str(i) + " --PidFile " 
    r += "tor" + str(i) + ".pid"
    return(r)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-bsp", "--base-socks-port",
        dest="bsp",
        action="store", 
        help="set base SOCKS port", 
        default="9050"
        )
    parser.add_argument(
        "-bcp", "--base-control-port", 
        action="store",
        dest="bcp",
        help="set base control port",
        default="8000"
    )
    parser.add_argument(
        "-d", "--data", 
        action="store",
        dest="data",
        help="set data storage directory, default - ./tordata/instance",
        default="./tordata/instance"
    )
    parser.add_argument(
        "-n", "--number", 
        action="store",
        dest="number",
        help="set number of tor instances to run, default - 10",
        default="10"
    )
    parser.add_argument(
        "-k", "-killall",
        action="store_true",
        dest="killall",
        help="kill all tor instances",
        default=False
    )
    args = parser.parse_args()
    if not args.killall:    
        bsp = int(args.bsp)
        bcp = int(args.bcp)
        datadir = args.data
        number = int(args.number)
        i = 0
        print("Multiple Tor Instance Runner")
        createDataDir(datadir)
        while i != number:
            command = formCommand(bsp+i, bcp+i, datadir, i)
            print(str(i)+" "+command)
            os.system(command)
            i += 1
    else:
        os.system("killall -w tor")

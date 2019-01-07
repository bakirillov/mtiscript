#!/usr/bin/python3
# -*- coding: utf-8 -*-

import mticlass
import threading
import queue
import argparse

#Just a simple test of mticlass module
#Script visits a list of webpages through tor, counts their length,
#then changes exit node and prints out link to page, tor port 
#number, control port number, ip address before and after exit node 
#change. 
#Number of threads must be less than or equal to number of tor 
#instances ran on your computer. Use -h to print out help.

class WorkerThread(threading.Thread):
    
    def __init__(self, q, number=0,
        initialport=9051, controlport=8001
    ):
        threading.Thread.__init__(self)
        self.threadNumber = number
        self.q = q
        self.initialport = initialport
        self.controlport = controlport
        
    def run(self):
        c = mticlass.TorInterface(
        self.initialport+self.threadNumber, self.controlport+self.threadNumber
        )
        while not self.q.empty():
            link = self.q.get()
            print(link)
            print("Tor port: "+str(c.port))
            print("Tor control port: "+str(c.controlPort))
            s = c.getSoup(link)
            print("Length of html text: "+str(len(s.get_text())))
            ip = c.checkMyIP()
            print("IP address before changing exit node: "+ip)
            c.changeExitNode()
            ip = c.checkMyIP()
            print("IP address after changing exit node: "+ip)
            c.finish()
            self.q.task_done()


def performTest(n):
    q = queue.Queue()
    q.put("http://www.google.com/")
    q.put("https://ru.wikipedia.org/")
    q.put("http://pythonworld.ru/")
    q.put("http://stackoverflow.com/")
    q.put("https://ru.wikibooks.org/")
    q.put("https://toster.ru/")
    q.put("http://www.unixmen.com/")
    q.put("http://habrahabr.ru/")
    q.put("http://help.ubuntu.ru/")
    q.put("https://vk.com/")
    i = 0
    threads = []
    while i != n:
        worker = WorkerThread(q, i, 9050+i, 8000+i)
        worker.setDaemon("True")
        threads.append(worker)
        i += 1
    for a in threads:
        a.start()
    q.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n", "--number-of-threads",
        dest="number",
        action="store", 
        help="set number of threads", 
        default="1"
        )
    args = parser.parse_args()
    performTest(int(args.number))

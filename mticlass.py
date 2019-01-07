#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pycurl
import io
import bs4
import re
import getpass
import stem
import stem.connection
from stem import Signal
from stem.control import Controller

#Regular expression for IP address mining
IPREGEX = "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\.?"

class TorInterface():
    
    def __init__(self, port=9050, controlport=8000):
        try:
            self.controller = Controller.from_port(port=controlport)
        except:
            print("Error: something went wrong")
        self.controlPort = controlport
        self.port = port

    def getSoup(self, url, t='GET', enc="utf-8"):
        """Visits an url and returns its content in form of bs4 soup"""
        output = io.BytesIO()
        query = pycurl.Curl()
        query.setopt(query.URL, url)
        query.setopt(query.PROXY, 'localhost')
        query.setopt(query.PROXYPORT, self.port)
        query.setopt(query.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)
        query.setopt(query.WRITEFUNCTION, output.write)
        try:
            query.perform()
            response = output.getvalue().decode(enc)
            soup = bs4.BeautifulSoup(response)
            return(soup)
        except pycurl.error as exc:
            return "Unable to reach %s (%s)" % (url, exc)

    def checkMyIP(self, link="http://www.get-myip.com/", n=0):
        """Visits a getmyip webpage and returns string with an adress"""
        lsoup = self.getSoup(link)
        ips = re.findall(IPREGEX, lsoup.get_text())
        r = ""        
        if len(ips) >= 1:
            r = ips[n]
        else:
            print("Error: no IP")
        return(r)

    def authenticate(self):
        """Authenticates a controller"""
        try:
            self.controller.authenticate()
        except self.connection.MissingPassword:
            p = getpass.getpass("Tor password: ")
            try:
                self.controller.authenticate(password = p)
            except stem.connection.PasswordAuthFailed:
                print("Error: Incorrect password.")
        except stem.connection.AuthenticationFailure as exc:
            print("Authentification error: %s" % exc)

    def changeExitNode(self):
        """Changes an exit node"""
        self.authenticate()
        try:
            self.controller.signal(Signal.NEWNYM)
        except e:
            print("Error: %s" % e)

    def finish(self):
        """Shuts controller down"""
        self.controller.close()

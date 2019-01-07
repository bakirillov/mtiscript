# README #

### MTIScript ###

* Script and class for using multiple TOR instances  
* Version 0.2

### How do I get set up? ###

* Usage  
  1. Add to your program some code controlling the TOR instance.  
  2. Run mtirunner.py with your preferred setup.  
  3. Run your program.  
  4. Enjoy!  

* mtirunner.py  
Runs a number of TOR instances.  
  1. -h, --help ==> show this help message and exit  
  2. -bsp BSP, --base-socks-port BSP ==> set base SOCKS port  
  3. -bcp BCP, --base-control-port BCP ==> set base control port  
  4. -d DATA, --data DATA ==> set data storage directory, default - ./tordata/instance  
  5. -n NUMBER, --number NUMBER ==> set number of tor instances to run, default - 10  
  6. -k, -killall ==> kill all tor instances  
  
* mticlass.py  
There is a TorInterface class. It wraps stem.control.Controller to control an instance and adds some additional functionality. You can work with stem.control.Controller as usual, it can be accessed as c.controller.    
Additional functions:  
  1. changeExitNode ==> changes TOR exit node.  
  2. checkMyIP ==> visits an ip checker webpage (default http://www.get-myip.com/) and returns IP as a string.  
  3. getSoup ==> visits an url through TOR and returns its content as bs4 soup.  
  4. authenticate ==> shortcut for TOR Controller authentication.  
  5. finish ==> finishes TOR Controller.  
```
#!python
 #EXAMPLE
 c = mticlass.TorInterface(controlport=8000, port=9050)   
 #Put your code here   
 c.finish() # stops controller. TorInterface should be finished after the job is done. 
```  

* test.py  
Simple test of mticlass module functioning. Visits a list of webpages through tor, counts their length, then changes exit node and prints out link to page, tor port 
number, control port number, ip address before and after exit node 
change.  Number of threads must be less than or equal to number of tor 
instances ran on your computer.  
  1. -n NUMBER, --number-of-threads NUMBER ==> set number of threads.  
  2. -h, --help ==> show this help message and exit.  

* Dependencies  
  1. stem(http://stem.torproject.org)   
  2. pycurl(http://pycurl.sourceforge.net)   
  3. argparse(docs.python.org/3/library/argparse.html)  
  4. BeautifulSoup4(pypi.python.org/pypi/beautifulsoup4)  

### Who do I talk to? ###

* Bogdan Kirillov k1r1llov@bk.ru
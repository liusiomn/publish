'''
Created on Jan 9, 2017
-*- coding: utf-8 -*-
@author: tcl
'''

from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler
import time
import os
import platform
from subprocess import call

class FileEventHandler(RegexMatchingEventHandler):
    def __init__(self, recievers, root='', patterns=[r'.*']):
        super(FileEventHandler, self).__init__(patterns)
        self.recievers = recievers
        self.root = root
        self.platform = platform.platform()

    def on_moved(self, event):
        if event.is_directory:
            print("directory moved from {0} to {1}".format(event.src_path,event.dest_path))
        else:
            print("file moved from {0} to {1}".format(event.src_path,event.dest_path))

    def on_created(self, event):
        if event.is_directory:
            for reciever in self.recievers:
                dst = self.parse_dir(reciever, event.src_path)
                if not os.path.exists(dst):
                    os.mkdir(dst)
                print("directory created:{0}".format(event.src_path))
            
        else:
            for reciever in self.recievers:
                dst = self.parse_dir(reciever, event.src_path)
                if not os.path.exists(dst):
                    self.createlink(self.parse_dir(reciever, event.src_path), 
                                event.src_path)
                print("file created:{0}".format(event.src_path))
                

    def on_deleted(self, event):
        if event.is_directory:
            print("directory deleted:{0}".format(event.src_path))
        else:
            print("file deleted:{0}".format(event.src_path))

    def on_modified(self, event):
        if event.is_directory:
            print("directory modified:{0}".format(event.src_path))
        else:
            print("file modified:{0}".format(event.src_path))
               
    def createlink(self, link, target):
        call([r'mklink' r'/H', link, target], shell=True)
        
    def parse_dir(self, reciever, src):
        if os.path.isdir(src):
            dst = os.path.join(src.split(self.root)[0],
                               self.root,
                               reciever,
                               'download',
                               src.split(os.sep)[-1])
        else:
            dst = os.path.join(src.split(self.root)[0],
                               self.root,
                               reciever,
                               'download',
                               src.split(os.sep)[-2],
                               src.split(os.sep)[-1])
        return dst    
        

if __name__ == "__main__":
    observer = Observer()
    event_handler = FileEventHandler([r'scen'], 'watchdog',[r'.*upload.+'])
    observer.schedule(event_handler,r"C:\Users\tcl\workspace\test\watchdog",True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

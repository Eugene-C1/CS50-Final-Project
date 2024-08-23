from bs4 import BeautifulSoup
from googleapiclient.discovery import build

import re
import json
import sys
import requests
import csv
import os
import os.path

TO_RETURN = dict()

import project

class YoutubeBot:
    def __init__(self):
        self._link = ""
        self._homepage = ""
        self._is_online = bool
        self._channel_name = ""
    
    def new_link(self, link):
        self._link = link
    
    @property
    def get_link(self):
        return self._link
    
    @property
    def get_name(self):
        return self._channel_name

    @property
    def check(self):
        return self._is_online
    
    def save_data(self):
        
        with open("youtube_notif.csv", "a") as file:
            writer = csv.DictWriter(file, fieldnames=["username", "homepage", "stream"])
            writer.writerow({"username": self._channel_name, "homepage" : self._homepage, "stream" : self._link})
            
        file.close()
        
    def notif_save(self, channel_url):
        
        response = requests.get(channel_url)
        
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            live = soup.find("link", {"rel": "canonical"})

            # Get Channel Name
            self._channel_name = re.search(r"https://www.youtube.com/@?(.+)/live", channel_url).group(1)
                            
            # Search for indicators that the channel is live streaming
            live_indicator = "isLiveBroadcast"
            offline_indicator = "Live in"
            

            self._homepage = channel_url
            #matches = re.search(r'<link href=\"(.+)\" rel=\"canonical\"/>', str(live))
            #self.new_link(matches.group(1))  # Set the link
            self.save_data()
            
            return self._is_online

    def is_online(self):
        youtubers = []
        new_list = []
        with open("youtube_notif.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                youtubers.append({"username" : row["username"], "homepage" : row["homepage"], "stream" : row["stream"]})      
        
        with open("temp.csv", "a") as file:
            writer = csv.DictWriter(file, fieldnames=["username", "homepage", "stream"])
            writer.writeheader()
               
            file.close()
        
        
        for youtuber in youtubers:
            response = requests.get(youtuber["homepage"])
            
            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                live = soup.find("link", {"rel": "canonical"})

                # Search for indicators that the channel is live streaming
                live_indicator = "isLiveBroadcast"
                offline_indicator = "Live in"
                
                matches = re.search(r'<link href=\"(.+)\" rel=\"canonical\"/>', str(live)).group(1)
                    
                if matches != youtuber["stream"] or youtuber["stream"] == None:
                    if live_indicator in html:
                        if offline_indicator not in html:
                            youtuber["stream"] = matches
                            TO_RETURN.update({youtuber["username"] : youtuber["stream"]})
                            new_list.append(youtuber)

                else:
                    new_list.append(youtuber)
        
            
            with open("temp.csv", "a") as file:
                writer = csv.DictWriter(file, fieldnames=["username", "homepage", "stream"])
                writer.writerow({"username": youtuber["username"], "homepage" : youtuber["homepage"], "stream" :youtuber["stream"]})    
            
            
            file.close()
        
        if file_exists := os.path.exists('temp.csv'):
            os.remove("youtube_notif.csv")
            os.rename("temp.csv", "youtube_notif.csv")            
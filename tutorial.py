#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PySimpleGUI27 as sg
import json
from pprint import pprint


with open('tweets_spain.json') as f:
    data = json.load(f)

    total = str(len(data[u'tweets']))
    outf = writeOpening()
    for i in range(0,len(data[u'tweets'])):
        index = str(i+1)
        name = data[u'tweets'][i][u'username'].decode('utf8')
        profile_geolocation = data[u'tweets'][i][u'profile_geolocation']
        text = data[u'tweets'][i][u'text']
        tweet_geolocation = data[u'tweets'][i][u'twit_geolocation']

        layout = [
                  [sg.Text("User ID: "+name)],
                  [sg.Text("Profile Geolocation: "+profile_geolocation)],
                  [sg.Text("Tweet Geolocation: "+tweet_geolocation)],
                  [sg.Text("Tweet: "+text)], [sg.Text('Geolocation', size=(15, 1)), sg.InputCombo(['1', '0'])],
                  [sg.Text('Relevance', size=(15, 1)), sg.InputCombo(['1', '0'])],
                  [sg.Text('Time', size=(15, 1)), sg.InputCombo(['f', 'p','none'])],
                  [sg.Text('Tweet '+ index +' of '+ total)],
                  [sg.Submit(), sg.Cancel()]
                 ]
        window = sg.Window('Process a tweet')

        button, values = window.LayoutAndRead(layout)
        # outf.write("\n\t\"Username\": "+str(name) + ",\n")
        print(profile_geolocation + "\n")
        print(text + "\n")
        print(tweet_geolocation + "\n")
        print('g' + str(values[0]) + 'r' + str(values[1]) + str(values[2]) + "\n")
        outf = writeMiddle(name,profile_geolocation,text,tweet_geolocation)
        if i+1 == len(data[u'tweets']):
            outf = writeFinalGroup()
        else:
            outf = writeEndGroup()
        sg.Popup(button,values)


    outf = writeEnding()

f.close()
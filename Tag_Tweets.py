#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PySimpleGUI as sg
import json


def writeOpening():
    with open('tagged_spain.json', 'w') as fd:
        fd.write("{\n")
        fd.write("\t\"tweets\": [\n")
def writeEnding():
    with open('tagged_spain.json','a') as fd:
        fd.write("\t]\n")
        fd.write("}\n")
    fd.close()

def writeMiddle(username,place_profile,text, place_tweet,RT,fd):
    fd.write("\t\t{\n\n")
    fd.write("\t\t\t\"username\" : \" %s \",\n" %username)
    fd.write("\t\t\t\"profile_geolocation\" : \"%s\", \n" %place_profile)
    fd.write("\t\t\t\"text\" : \" %s \",\n" %text)
    fd.write("\t\t\t\"tweet_geolocation\" : \" %s \",\n" % place_tweet)
    fd.write("\t\t\t\"RT\" : \" %s \",\n" % RT)



with open('retrieved_tweets_spain.json','r') as f:
    #decoded_json = f.read().decode('string_escape').decode('latin1')
    data = json.load(f)
    #data = json.loads(HTMLParser().unescape(data.body.decode('unicode-escape')))
    total = str(len(data[u'tweets']))
    # for i in range(0,len(data[u'tweets'])):
    writeOpening()
    for i in range(0,3):
        index = str(i+1)
        name = data[u'tweets'][i][u'username'].encode('utf8')
        profile_geolocation = data[u'tweets'][i][u'profile_geolocation'].encode('utf8')
        text = data[u'tweets'][i][u'text'].encode('utf8')
        tweet_geolocation = data[u'tweets'][i][u'tweet_geolocation'].encode('utf8')
        RT = data[u'tweets'][i][u'RT'].encode('utf8')

        layout = [
                  [sg.Text("User ID: "+str(name.decode('utf8')))],
                  [sg.Text("Profile Geolocation: "+str(profile_geolocation.decode('utf8')))],
                  [sg.Text("Tweet Geolocation: "+str(tweet_geolocation.decode('utf8')))],
                  [sg.Text("Tweet: "+str(text.decode('utf8')))], [sg.Text('Geolocation', size=(15, 1)), sg.InputCombo(['1', '0'])],
                  [sg.Text('Relevance', size=(15, 1)), sg.InputCombo(['1', '0'])],
                  [sg.Text('Time', size=(15, 1)), sg.InputCombo(['f', 'p','none'])],
                  [sg.Text('Spain', size=(15, 1)), sg.InputCombo(['yes', 'no', 'undefined'])],
                  [sg.Text('Tweet '+ index +' of '+ total)],
                  [sg.Submit(), sg.Cancel()]
                 ]
        window = sg.Window('Processing tweets')

        button, values = window.LayoutAndRead(layout)

        if button == 'Cancel':
            break


        with open('tagged_spain.json','a') as fout:
            writeMiddle(name,profile_geolocation,text,tweet_geolocation,RT,fout)
            fout.write('\t\t\t\"Tag \": \"g' + str(values[0]) + 'r' + str(values[1]) + str(values[2]) + "\"\n")
            fout.write('\t\t\t\"Spain \": \"%s \"\n"' % str(values[3]))
        sg.Popup(button,values)
writeEnding()

f.close()
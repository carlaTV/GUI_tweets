#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PySimpleGUI27 as sg
import json
from googletrans import Translator
import emoji
import pyperclip


translator = Translator()


def remove_emoji(text):
    return emoji.get_emoji_regexp().sub(u'', text)

def writeOpening():
    with open('tagged_spain.json', 'w') as fd:
        fd.write("{\n")
        fd.write("\t\"tweets\": [\n")
def writeEnding():
    with open('tagged_spain.json','a') as fd:
        fd.write("\n\t]\n")
        fd.write("}\n")
    fd.close()

def writeMiddle(username,place_profile,text, place_tweet,RT,fd):
    fd.write("\n\t\t{\n")
    fd.write("\t\t\t\"username\" : \" %s \",\n" %username)
    fd.write("\t\t\t\"profile_geolocation\" : \"%s\", \n" %place_profile)
    fd.write("\t\t\t\"text\" : \" %s \",\n" %text)
    fd.write("\t\t\t\"tweet_geolocation\" : \" %s \",\n" % place_tweet)
    fd.write("\t\t\t\"RT\" : \" %s \",\n" % RT)



with open('retrieved_tweets_spain.json','r') as f:
    data = json.load(f)
    total = str(len(data[u'tweets']))
    writeOpening()
    i = 0
    button = ''
    while i < total:
        index = str(i+1)
        name = data[u'tweets'][i][u'username'].encode('utf8')
        profile_geolocation = data[u'tweets'][i][u'profile_geolocation'].encode('utf8')
        text = data[u'tweets'][i][u'text'].encode('utf8')
        tweet_geolocation = data[u'tweets'][i][u'tweet_geolocation'].encode('utf8')
        RT = data[u'tweets'][i][u'RT'].encode('utf8')

        text = unicode(text, "UTF-8")
        text = text.replace(u"\u00A0", " ")
        noemoji = remove_emoji(text)

        russian_trans = translator.translate(noemoji, dest='ru').text
        english_trans = translator.translate(noemoji, dest='en').text


        layout = [
                  [sg.Text("User ID: "+name,font=("Calibri",11))],
                  [sg.Text("User Geolocation: "+profile_geolocation,font=("Calibri",11))],
                  [sg.Text("Tweet Geolocation: "+tweet_geolocation,font=("Calibri",11))],
                  [sg.Text("Tweet:\n"+noemoji,font=("Calibri",11))],
                  [sg.Text(russian_trans,font=("Calibri",11))],
                  [sg.Text(english_trans,font=("Calibri",11))],
                  [sg.ReadButton('Copy Original Tweet')],[sg.ReadButton('Copy Russian translation')],
                  [sg.ReadButton('Copy English translation')],
                  [sg.Text('Geolocation', size=(15, 1),font=("Calibri",11)), sg.InputCombo(['0', '1'])],
                  [sg.Text('Relevance', size=(15, 1),font=("Calibri",11)), sg.InputCombo(['0', '1'])],
                  [sg.Text('Time', size=(15, 1),font=("Calibri",11)), sg.InputCombo(['none','f', 'p'])],
                  [sg.Text('Spain', size=(15, 1),font=("Calibri",11)), sg.InputCombo(['yes', 'no', 'undefined'])],
                  [sg.Text('Narrow Geolocation', size=(15, 1),font=("Calibri",11)), sg.InputCombo(['yes', 'no'])],
                  [sg.Text('Tweet '+ index +' of '+ total,font=("Calibri",11))],
                  [sg.Text('Start from tweet number: ',font=("Calibri",11))],[sg.Input()],
                  [sg.Submit(), sg.Cancel()]
                 ]


        window = sg.Window('Processing tweets')
        button, values = window.LayoutAndRead(layout)

        if button != 'Submit':

            if button == 'Copy Original Tweet':
                pyperclip.copy(text)
            if button == 'Copy Russian translation':
                pyperclip.copy(russian_trans)
            if button == 'Copy English translation':
                pyperclip.copy(english_trans)

            if button == 'Cancel':
                break

        else:
            i += 1
            if values[5] != '':
                i = int(values[5]) - 1

            with open('tagged_spain.json', 'a') as fout:
                writeMiddle(name, profile_geolocation, text.encode('utf8'), tweet_geolocation, RT, fout)
                fout.write('\t\t\t\"Tag \": \"g' + str(values[0]) + 'r' + str(values[1]) + str(values[2]) + "\",\n")
                fout.write('\t\t\t\"Spain \": \"%s \"\n' % str(values[3]))
                if i < total:
                    fout.write("\t\t},")
                else:
                    fout.write("\t\t}")
            sg.Popup(button, values)

writeEnding()
f.close()
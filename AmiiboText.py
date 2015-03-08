#!/usr/bin/env python

# Modified by: Paul Schow
# Date Modified: March 6 2015
#
# This modified version scans Amazon for a particular amiibo and
# sends a text when that amiibo comes in stock. Unlike the original
# code, this is meant to be run as a cron job. See the readme for
# more details.

# Original copyright notice included:

# Author: Omar A. Ansari
# Date Modified: 1/17/15
# Version: 1.5
#
# This program queries Amazon.com for changes in Amiibo Selection and
# tweets about these changes.
#
# This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################


#########################################################################
# Modules
#########################################################################

from amazonproduct import API, AWSError
#from tweepy.streaming import StreamListener
#from tweepy import OAuthHandler
#from tweepy import Stream
#from apscheduler.schedulers.background import BackgroundScheduler
#import tweepy
import time
import datetime
from lxml import html
import requests
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import smtplib

#########################################################################
# Class
#########################################################################


class AmiiboLookup():

#########################################################################
# Static Method: lookup(id_num, auth)
#
# This method searches for a product on Amazon.com by id_num
#
# Param:
#
# id_num -- Amazon.com Prouct ID Number used to search
# auth -- Encryption key used for Amazon API.
#
#########################################################################
    @staticmethod
    def lookup(id_num, auth):

        node = auth.item_lookup(id_num, ResponseGroup='Offers',
             Condition='All', MerchantId='All')

        for a in node.Items.Item.Offers.Offer:
            try:
                return a.OfferListing.Price.FormattedPrice
                break
            except:
                return "NA"

#########################################################################
# Static Method: searchAmiibo(auth)
#
# This method searches for any product on Amazon.com with the word
# "Amiibo" in the title and returns a list of found items.
#
# Param:
#
# auth -- Encryption key used for Amazon API.
#
#########################################################################

    @staticmethod
    def searchAmiibo(auth):

        amiibosOnAmazon = []

        for item in auth.item_search('VideoGames', Title='Amiibo',
             MerchantId="Amazon", Availability="Available"):
            name = (item.ItemAttributes.Title)
            identification = item.ASIN
            identificationString = str(identification)
            #print identificationString
            try:
                value = AmiiboLookup.lookup(identificationString, auth)
            except:
                value = "NA"
            #print value
            spaces = str(name).encode("utf-8").count(' ')
            if spaces < 4 and (value != "NA"):
                amiibosOnAmazon.append(str(name).encode('ascii',
                errors='ignore'))

        time.sleep(1)

        return amiibosOnAmazon

#########################################################################
# Main
#########################################################################

if  __name__ == '__main__':

    log = open('log1.txt', 'a')  # open a text file for logging
    #f = open("amiibos.txt", "w")
    #print f
    print log  # print what the log file is
    #log.write('Time,IP,Ping\n')  # write to log

    amazon = API("Short key",
         "long key", "us", "Amazon associate tag")
    # Short key first, then long key, then locale, then Amazon associate tag

    oldAmiibosListAmazon = []
    newAmiibosListAmazon = []
    oldAmiiboPrice = ""
    newAmiiboPrice = ""
    information = AmiiboLookup()

    oldAmiibosListAmazon = information.searchAmiibo(amazon)
    strami = str(oldAmiibosListAmazon)
    print strami
    #print strami[3]
    #f.write(strami)

    # Look for Ness
    nessdetect = 'Ness' in strami
    #print nessdetect
    if nessdetect is True:
        logging = str(time.strftime("%B %d %H:%M:%S"))
        log.write(logging)  # write to log
        log.write(strami)
        log.write("\n")  # you know what, it works okay
        print "He has risen"

        # Send email
        # This should probably be in a function or class or something
        fromaddr = "example@gmail.com"  # from address
        toaddr = "5551230987@vmobl.com"  # to email
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "NESS DETECTED"

        body = str(strami)
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login("example@gmail.com",  # from address
             "password")  # from password
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
    else:
        print "No"

    print "done"

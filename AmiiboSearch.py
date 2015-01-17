##########################################################################
# Author: Omar A. Ansari
# Date Modified: 1/16/15
# Version: 1.4
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
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from apscheduler.schedulers.background import BackgroundScheduler
import tweepy
import time
import datetime

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

		node = auth.item_lookup(id_num, ResponseGroup='Offers', Condition='All', MerchantId='All')
		try:
			for a in node.Items.Item.Offers.Offer:
		    		return a.OfferListing.Price.FormattedPrice
		    		break
		except AttributeError:
			return "NA"

#########################################################################
# Method: printOut(e, items, auth)
#
# This method prints out items in the Amiibo list with the prices.
#
# Param:
#
# e -- exception
# items -- List of Amiibo.
# auth -- Encryption key used for Amazon API.
#
#########################################################################


	def printOut(e, items, auth):
		
		count = 0
		statement = ""
		amiiboString =""
		while count < len(items):
			tempElem = items[count]
			amiiboString = str(AmiiboLookup.lookup(tempElem[1], auth))
			
			if amiiboString == "Too low to display":
					statement += tempElem[0]+":"+"TLtD"+"| "

			else:
					statement += tempElem[0]+":"+amiiboString+"| "
			
			count = count + 1
			time.sleep(1)
		
		return statement

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


		for item in auth.item_search('VideoGames', Title='Amiibo', MerchantId="Amazon"):
			name = (item.ItemAttributes.Title)
			try:
					spaces = str(name).encode("utf-8").count(' ')
					if spaces < 4:
						amiibosOnAmazon.append(str(name).encode('ascii',errors='ignore'))
			except:
					continue
			time.sleep(1)
		return amiibosOnAmazon

#########################################################################
# Static Method: tweetAlert(e, CKEY, CSECRET, AKEY, ASECRET, listChange)
#
# This method tweets a message notifiying users that a change has been
# detected. Either an Amiibo was added or deleted.
#
# Param:
#
# e -- exception
# CKEY -- Consumer Key used by Tweepy.
# CSECRET -- Consumber Secret Key used by Tweepy
# AKEY -- Application Key used by Tweepy
# ASECRET -- Application Secret Key used by Tweepy
# listChange = list to tweet out.
#
#########################################################################
	
	def tweetAlert(e, CKEY, CSECRET, AKEY, ASECRET, listChange, i):

		auth = tweepy.OAuthHandler(CKEY, CSECRET)
		auth.set_access_token(AKEY, ASECRET)
		api = tweepy.API(auth)

		if i == 1:
			api.update_status("Amiibo addition: " + str(listChange) + " has been detected." + " " + str(datetime.datetime.now().time().microsecond)[:3])
			print "Amiibo addition: " + str(listChange) + " has been detected." + " " + str(datetime.datetime.now().time().microsecond)[:3]
		else:
			api.update_status("Amiibo removal: " + str(listChange) + " has been detected." + " " + str(datetime.datetime.now().time().microsecond)[:3])
			print "Amiibo removal: " + str(listChange) + " has been detected." + " " + str(datetime.datetime.now().time().microsecond)[:3]
	
#########################################################################
# Static Method: tweetAlert(e, CKEY, CSECRET, AKEY, ASECRET, listChange)
#
# This method searches for a product on Amazon.com by id_num
#
# Param:
#
# e -- exception
# CKEY -- Consumer Key used by Tweepy.
# CSECRET -- Consumber Secret Key used by Tweepy
# AKEY -- Application Key used by Tweepy
# ASECRET -- Application Secret Key used by Tweepy
# authentication -- Encryption key used for Amazon API.
# items -- Items to be tweeted.
#
#########################################################################

	def tweetStatus(e, CKEY, CSECRET, AKEY, ASECRET, authentication, items):

		auth = tweepy.OAuthHandler(CKEY, CSECRET)
		auth.set_access_token(AKEY, ASECRET)
		api = tweepy.API(auth)
		s = AmiiboLookup.printOut(e, items, authentication)
		n = 10
		splitUp = s.split(" ")
		group1 = " ".join(splitUp[:n]) 
		group2 =" ".join(splitUp[n:])

		api.update_status(group1 + str(datetime.datetime.now().time().second))
		time.sleep(.5)
		api.update_status(group2 + str(datetime.datetime.now().time().second))
		print group1 + " " +str(datetime.datetime.now().time().second)
		time.sleep(.5)
		print group2 + " " +str(datetime.datetime.now().time().second)

#########################################################################
# Main
#########################################################################

if  __name__ =='__main__':
	
	amazon = API("XXXXXXXX", "XXXXXXXXXXXXXXXXXXXXXXXX", "us", "XXXXX")
	
	CONSUMER_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXX'#keep the quotes, replace this with your consumer key
	CONSUMER_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXX'#keep the quotes, replace this with your consumer secret key
	ACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXX'#keep the quotes, replace this with your access token
	ACCESS_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXX'#keep the quotes, replace this with your access token secret
	

	oldAmiibosList = []
	newAmiibosList = []
	oldAmiiboPrice = ""
	newAmiiboPrice = ""
	information = AmiiboLookup()
	
	amiibo = [
		["MR", "B00N4ABMG4"], ["PE", "B00N4ABT1W"], ["Y", "B00N4ABT1C"],
		["LU", "B00N4ABVOM"], ["PK", "B00N4ABSLS"], ["K", "B00N4ABV10"],
		["DO", "B00N4ABP7A"], ["F", "B00N4ABODK"], ["S", "B00N49EEO2"],
		["W", "B00N49EERY"], ["V", "B00N4ABMUA"], ["MT", "B00N4ABOXU"],
		["Z", "B00O92ONBM"], ["DI", "B00O982JSU"], ["LU", "B00O97ZWVC"], 
		["LM","B00O97ZVJA"], ["PI","B00O97ZYP6"], ["C","B00O97ZVJ0"],
		["TL","B00PG6Z9VI"], ["SH","B00PG6ZAZ8"], ["IK","B00PG7M95G"],
		["SO","B00PG6ZBTS"], ["MM","B00PG6ZCT2"], ["KD","B00PG6ZDPK"],
	]

	#information.tweetStatus(CONSUMER_KEY,CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET, amazon, amiibo)

	#scheduler = BackgroundScheduler()
	#scheduler.add_job(lambda: information.tweetStatus(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET, amazon, amiibo), 'interval', seconds=7200)
	#scheduler.start()


	oldAmiibosList = information.searchAmiibo(amazon)
	oldAmiibosPrice = information.printOut(amiibo, amazon)
	time.sleep(1)
	newAmiiboPrice = oldAmiiboPrice

	while(True):
		newAmiibosList = information.searchAmiibo(amazon)
		newAmiiboPrice = information.printOut(amiibo, amazon)
		time.sleep(1)
		if oldAmiibosList != newAmiibosList:
			print "NEW AMIIBOS DETECTED"
			my_list = []
			value = 0
			if len(newAmiibosList) > len(oldAmiibosList):
				my_list = list(set(newAmiibosList) - set(oldAmiibosList))
				value = 1
			else: 
				my_list = list(set(oldAmiibosList) - set(newAmiibosList))
				value = 2

			print my_list
			information.tweetAlert(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET, my_list, value)
			print oldAmiibosList
			print oldAmiiboPrice
			print newAmiibosList
			print newAmiiboPrice
			oldAmiibosList = newAmiibosList
			time.sleep(60)
		else:
			oldAmiibosList = newAmiibosList
			print ("I'm sorry, there has been no change in the Amiibos available on Amazon.com. Trying again now.")

		#if oldAmiiboPrice != newAmiiboPrice:
		#	information.tweetStatus(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET, amazon, amiibo)
		#	print "New Price Detected"
		#	oldAmiiboPrice = newAmiiboPrice
		#	time.sleep(60)
		#else:
		#	print "NO NEW PRICE DETECTED"
		#	oldAmiiboPrice = newAmiiboPrice
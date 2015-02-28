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
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from apscheduler.schedulers.background import BackgroundScheduler
import tweepy
import time
import datetime
from lxml import html
import requests
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
			
		for a in node.Items.Item.Offers.Offer:
			try:	  
	  			return a.OfferListing.Price.FormattedPrice
		    		break
			except:
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

		
		for item in auth.item_search('VideoGames', Title='Amiibo', MerchantId="Amazon", Availability = "Available"):
			name = (item.ItemAttributes.Title)
			identification = item.ASIN
			identificationString =str(identification)
			print identificationString
			try:
				value = AmiiboLookup.lookup(identificationString, auth)
			except: 
				value = "NA"
			print value
			spaces = str(name).encode("utf-8").count(' ')
			if spaces < 4 and (value != "NA"):
				amiibosOnAmazon.append(str(name).encode('ascii',errors='ignore'))

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
			try:	
				api.update_status(" AZ Amiibo addition: " + str(listChange) + " has been detected." + " " + str(datetime.datetime.now().time().microsecond)[:3])
				print "Amiibo addition: " + str(listChange) + " has been detected." + " " + str(datetime.datetime.now().time().microsecond)[:3]
			except:
				api.update_status("SEVERAL CHALLENGERS APPROACH! " + str(datetime.datetime.now().time().microsecond)[:3])
				print "n"
		if i == 2:
			try:
				api.update_status("AZ Amiibo removal: " + str(listChange) + " has been detected." + " " + str(datetime.datetime.now().time().microsecond)[:3])
				print "Amiibo removal: " + str(listChange) + " has been detected." + " " + str(datetime.datetime.now().time().microsecond)[:3]
	
			except:
				api.update_status("SEVERAL CHALLENGERS APPROACH! " + str(datetime.datetime.now().time().microsecond)[:3])
				print "n"
		if i == 3:
			try:
				api.update_status("GS New Amiibo detected." + " " + str(datetime.datetime.now().time().microsecond)[:3])
				print "Stock availability has changed on Gamestop.com has been detected." + " " + str(datetime.datetime.now().time().microsecond)[:3]
	
			except:
				api.update_status("SEVERAL CHALLENGERS APPROACH! " + str(datetime.datetime.now().time().microsecond)[:3])
				print "n"
		if i == 4:
			try:
				api.update_status("GS new Amiibo stock change has been detected." + " " + str(datetime.datetime.now().time().microsecond)[:3])
				print "Stock availability has changed on Gamestop.com has been detected." + " " + str(datetime.datetime.now().time().microsecond)[:3]
	
			except:
				api.update_status("SEVERAL CHALLENGERS APPROACH! " + str(datetime.datetime.now().time().microsecond)[:3])
				print "n"
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

##########################################################################

	def loopThroughPosted(e):
		
		page = requests.get('http://www.gamestop.com/browse?nav=16k-3-amiibo,28zu0')
		tree = html.fromstring(page.text)

		amiiboList = []
		firstText = "//a[@id="
		secondText = "mainContentPlaceHolder_dynamicContent_ctl00_RepeaterResultFoundTemplate_ResultFoundPlaceHolder_1_ctl00_1_ctl00_1_StandardPlaceHolderTop_3_ctl00_3_rptResults_3_res_"
		thirdText = "_hypTitle_"
		fourthText = "]/text()"
		counter = 0
					
		while(True):
			#print counter
			itemToSearch = ""
			try:
				itemToSearch = firstText + "'"  + secondText + str(counter) + thirdText + str(counter) + "'" + fourthText
				#print itemToSearch
				item = tree.xpath(itemToSearch)
				if item:

					amiiboList.append(item)
					
				else:
					break
			except:
				break
				print ("Done with items in search.")

			counter = counter + 1 
		
		return amiiboList

##########################################################################

	def loopThroughAvailable(e):
		
		page = requests.get('http://www.gamestop.com/browse?nav=16k-3-amiibo,28zu0')
		tree = html.fromstring(page.text)

		amiiboList = []
		firstTextAvailable = "//li[@id="
		secondTextAvailable = "mainContentPlaceHolder_dynamicContent_ctl00_RepeaterResultFoundTemplate_ResultFoundPlaceHolder_1_ctl00_1_ctl00_1_StandardPlaceHolderTop_3_ctl00_3_rptResults_3_res_"
		thirdTextAvailable = "_Li1_"
		fourthText = "]/text()"
		counter = 0

		while(True):
			itemToSearch = ""

			availableToSearch = firstTextAvailable + "'"  + secondTextAvailable + str(counter) + thirdTextAvailable + str(counter) + "'" + fourthText
			
			item = tree.xpath(availableToSearch)
			
		
			amiiboList.append(item)
			counter = counter + 1
			
			if counter > len(AmiiboLookup.loopThroughPosted(e)):
				break

		return amiiboList

#########################################################################
# Main
#########################################################################

if  __name__ =='__main__':
	
	amazon = API("", "", "us", "")
	
	CONSUMER_KEY = ''#keep the quotes, replace this with your consumer key
	CONSUMER_SECRET = ''#keep the quotes, replace this with your consumer secret key
	ACCESS_KEY = ''#keep the quotes, replace this with your access token
	ACCESS_SECRET = ''#keep the quotes, replace this with your access token secret
	

	oldAmiibosListAmazon = []
	newAmiibosListAmazon = []
	oldAmiibosListGameStop = []
	newAmiibosListGameStop = []
	oldAmiibosPriceGameStop = []
	newAmiibosPriceGameStop = []
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
	
	
	oldAmiibosListAmazon = information.searchAmiibo(amazon)
	time.sleep(110)
	oldAmiibosPrice = information.printOut(amiibo, amazon)
	time.sleep(10)
	oldAmiibosListGameStop = information.loopThroughPosted()
	time.sleep(10)
	
	oldAmiibosPriceGameStop = information.loopThroughAvailable()
	time.sleep(10)


	

	newAmiibosPriceGameStop = oldAmiibosPriceGameStop
	newAmiibosListGameStop = oldAmiibosListGameStop
	

	
	while(True):
		newAmiibosListGameStop = information.loopThroughPosted()
		time.sleep(10)
		newAmiibosPriceGameStop = information.loopThroughAvailable()
		time.sleep(10)
		newAmiibosListAmazon = information.searchAmiibo(amazon)
		time.sleep(10)
###########AMAZON###################################AMAZON##################################AMAZON###############################################		
		if (oldAmiibosListAmazon != newAmiibosListAmazon) and (len(newAmiibosListAmazon) != 0) and (len(oldAmiibosListAmazon) != 0):
			print oldAmiibosListAmazon
			print newAmiibosListAmazon
			print "NEW AMIIBOS DETECTED AZ"
			my_list = []
			value = 0
			if len(newAmiibosListAmazon) > len(oldAmiibosListAmazon):
				my_list = list(set(newAmiibosListAmazon) ^  set(oldAmiibosListAmazon))
				value = 1
			elif len(newAmiibosListAmazon) < len(oldAmiibosListAmazon): 
				my_list = list(set(oldAmiibosListAmazon) ^ set(newAmiibosListAmazon))
				value = 2
			print value
			print my_list
			try:
				information.tweetAlert(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET, my_list, value)
			except:
				print "TWEET TOO LONG"

			oldAmiibosListAmazon = newAmiibosListAmazon
			time.sleep(1)
		else:
			oldAmiibosListAmazon = newAmiibosListAmazon
			print ("I'm sorry, there has been no change in the Amiibos available on Amazon.com. Trying again now.")
			print oldAmiibosListAmazon
			print newAmiibosListAmazon
	
###########AMAZON###################################AMAZON##################################AMAZON###############################################

###########GAMESTOP###################################GAMESTOP##################################GAMESTOP#########################################
		print "GET HERE"
		print oldAmiibosListGameStop
		print oldAmiibosPriceGameStop
		print newAmiibosListGameStop
		print newAmiibosPriceGameStop

		if (oldAmiibosListGameStop != newAmiibosListGameStop) and (len(newAmiibosListGameStop) != 0) and (len(oldAmiibosListGameStop) != 0):
			
			print "NEW AMIIBOS DETECTED GS"
			gameStop_list = []
			gameStopValue = 0
			if len(newAmiibosListGameStop) > len(oldAmiibosListGameStop):
				gameStop_list = list(set(newAmiibosListGameStop) ^ set(oldAmiibosListGameStop))
				gameStopValue = 1
			elif len(newAmiibosListGameStop) < len(oldAmiibosListGameStop):
				gameStop_list = list(set(oldAmiibosListGameStop) ^ set(newAmiibosListGameStop))
				gameStopValue = 3

			try:
				information.tweetAlert(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET, gameStop_list, gameStopValue)
			except:
				print "TWEET TOO LONG"
		
		if (oldAmiibosPriceGameStop != newAmiibosPriceGameStop) and (len(newAmiibosPriceGameStop) != 0) and (len(oldAmiibosPriceGameStop) !=0):
			print oldAmiibosPriceGameStop
			print newAmiibosPriceGameStop
			gameStop_list = []
			gameStopValue = 4
			try:
				information.tweetAlert(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET, gameStop_list, gameStopValue)
			except:
				print "TWEET TOO LONG"

###########GAMESTOP###################################GAMESTOP##################################GAMESTOP#########################################

		#if oldAmiiboPrice != newAmiiboPrice:
		#	information.tweetStatus(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET, amazon, amiibo)
		#	print "New Price Detected"
		#	oldAmiiboPrice = newAmiiboPrice
		#	time.sleep(60)
		#else:
		#	print "NO NEW PRICE DETECTED"
		#	oldAmiiboPrice = newAmiiboPrice

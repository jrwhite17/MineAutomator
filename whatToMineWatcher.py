import json
import re
import time
import os
import subprocess
from urllib.request import Request, urlopen
from pprint import pprint

configJson = 'C:\\Users\\JWhite\\Documents\\Github\\MineAutomator\\config.json'



class AutoMiner:
	#Final Variables
	COINS_ENDPOINT = "http://whattomine.com/calculators"
	COIN_CALCULATION_ENDPOINT = "http://whattomine.com/coins"
	
	#Create algorithm list
	algorithmsList = []
	#Create all coins list
	allCoinsList = []
	#Create mineable coins endpoint list
	mineableCoinsEndpointList = []
	#Create mineable coins data list
	mineableCoinsList = []
	
	def setup(self):
		self.currentAbsPath = os.path.dirname(os.path.abspath(__file__))
		self.jsonConfig = self.currentAbsPath + "\\config.json"
		
		#Check to see if config file exists
		if os.path.isfile(self.jsonConfig) == False:
			pprint("ERROR: Could not find config.json")
			pprint("Create file in the following directory..")
			pprint(self.currentAbsPath)
			quit()
			
		#Check to see if mining directory exists
		if os.path.isdir(self.currentAbsPath + "\\mining") == False:
			pprint("ERROR: Could not find mining directory")
			pprint("Create mining directory in the following directory..")
			pprint(self.currentAbsPath)
			quit()
	#End of setup Function

	def openConfig(self):
		with open(self.jsonConfig) as configFile:
			#Load Json data into python
			configData = json.load(configFile)
			#Load checkRateMinutes and store as variable
			self.checkRateMinutes = configData["AutoMiner"]["config"]["checkRateMinutes"]
			#Load profitDifferenceDollars and store as variable
			self.profitDifferenceDollars = configData["AutoMiner"]["config"]["profitDifferenceDollars"] 
			
			#Load algorithms data and create class
			for algorithm in configData["AutoMiner"]["algorithms"]:
				algorithmName = algorithm
				minerDir = configData["AutoMiner"]["algorithms"][algorithm]["minerDir"]
				p = configData["AutoMiner"]["algorithms"][algorithm]["p"]
				hr = configData["AutoMiner"]["algorithms"][algorithm]["hr"]
				fee = configData["AutoMiner"]["algorithms"][algorithm]["fee"]
				cost = configData["AutoMiner"]["algorithms"][algorithm]["cost"]
				hcost = configData["AutoMiner"]["algorithms"][algorithm]["hcost"]
				
				#Create AlgorithmData class and add to algorithmsList
				self.algorithmsList.append(AlgorithmData(algorithmName, minerDir, p, hr, fee, cost, hcost))
	#End of openConfig Function			

	def pullAllCoins(self):
		allCoinsRequest = Request(self.COINS_ENDPOINT, headers={'User-Agent': 'Mozilla/5.0'})
		allCoinsHTMLData = urlopen(allCoinsRequest).read().decode("utf-8")
		
		#Return all coins IDs
		self.allCoinsList = re.findall("<h3><a href=\"/coins/*(.+)\">", allCoinsHTMLData)
	#End of pullAllCoins Function
	
	def generateMineableCoinEndpoints(self):
		for coin in self.allCoinsList:
			for algorithm in self.algorithmsList:
				if algorithm.name in coin:
					coinEndpointLink = self.COIN_CALCULATION_ENDPOINT + "/" + coin + ".json?utf8=%E2%9C%93&" + \
					"hr=" + str(algorithm.hr) + \
					"&p=" + str(algorithm.p) + \
					"&fee=" + str(algorithm.fee) + \
					"&cost=" + str(algorithm.cost) + \
					"&hcost=" + str(algorithm.hcost) + \
					"&commit=Calculate"
					
					self.mineableCoinsEndpointList.append(coinEndpointLink)
	#End of generateMineableCoinEndpoints Function
	
	def parseMineableCoins(self):
		for coinEndpoint in self.mineableCoinsEndpointList:
			coinRequest = Request(coinEndpoint, headers={'User-Agent': 'Mozilla/5.0'})
			coinJSONData = urlopen(coinRequest).read().decode("utf-8")
			coinData = json.loads(coinJSONData)
			
			#Store algorithm name from config file in CoinData class
			for algorithm in self.algorithmsList:
				if algorithm.name in coinEndpoint:
					self.mineableCoinsList.append(CoinData(str(coinData["name"]),str(coinData["tag"]),str(algorithm.name),float(coinData["profit"].replace('$',''))))
					#DEBUG
					#pprint(str(coinData["name"]) +  " - " + str(coinData["tag"]) + " - " + str(coinData["algorithm"]) + " - " + str(algorithm.name) + " - " + str(coinData["profit"]))
					#pprint(coinEndpoint)
	#End of parseMineableCoins Function

	def sortCoinsByProfit(self):
		#Debug
		#pprint("Before: " + self.mineableCoinsList[0].name + " " + str(self.mineableCoinsList[0].profit))
		self.mineableCoinsList.sort(key=lambda x: x.profit, reverse=True)
		#DEBUG
		#pprint("After: " + self.mineableCoinsList[0].name + " " + str(self.mineableCoinsList[0].profit))
	#End of sortCoinsByProfit Function
	
	def executeMiner(self):
		for mineableCoin in self.mineableCoinsList:
			for algorithm in self.algorithmsList:
				if mineableCoin.algorithm == algorithm.name:
					#pprint(algorithm.name + " -- " + algorithm.minerDir)
					pprint(self.currentAbsPath + "\\mining\\" + algorithm.minerDir + "\\" +  mineableCoin.abbreviation + ".bat")
					if os.path.isfile(self.currentAbsPath + "\\mining\\" + algorithm.minerDir + "\\" +  mineableCoin.abbreviation + ".bat"):
						minerProc = subprocess.Popen("C:\\Windows\\System32\\cmd.exe /c "+ self.currentAbsPath + "\\mining\\" + algorithm.minerDir + "\\" +  mineableCoin.abbreviation + ".bat", shell=True)
						return
	
	#End of executeMiner Function
	
	def timer(self):
		mins = 0
		#Loop until mins equals checkRateMinutes
		while mins < float(self.checkRateMinutes):
			#DEBUG
			pprint("Timer: " + mins + " Minutes")
			# Sleep for a minute
			time.sleep(60)
			# Increment the minute total
			mins += 1
	#End of timer Function


#This class contains the algorithm data loaded from the config file	

class AlgorithmData:
	def __init__(self, name, minerDir, p, hr, fee, cost, hcost):
		#Load the algorithm name
		self.name = name
		#Load the miner name into this class variable
		self.minerDir = minerDir
		#Load the power integer into this class variable
		self.p = p
		#Load the hash rate integer into this class variable
		self.hr = hr
		#Load the fee integer into this class variable
		self.fee = fee
		#Load the cost integer into this class variable
		self.cost = cost
		#Load the hcost integer into this class variable
		self.hcost = hcost
#End of AlgorithmData Class

class CoinData:
	def __init__(self, name, abbreviation, algorithm, profit):
		#Set the coin name
		self.name = name
		#Set the coin abbreviation
		self.abbreviation = abbreviation
		#Set the algorithm name
		self.algorithm = algorithm
		#Set the profit
		self.profit = profit
#End of CoinData Class


#MAIN			
AutoMiner = AutoMiner()
AutoMiner.setup()
AutoMiner.openConfig()
AutoMiner.pullAllCoins()
AutoMiner.generateMineableCoinEndpoints()
AutoMiner.parseMineableCoins()
AutoMiner.sortCoinsByProfit()
AutoMiner.executeMiner()

#pprint(AutoMiner.mineableCoinsEndpointList)

#https://whattomine.com/coins/172-pasc-pascal.json?utf8=%E2%9C%93&hr=4041.0&p=900.0&fee=0.0&cost=0.06&hcost=0.0&commit=Calculate


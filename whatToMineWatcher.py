import json
import re
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
	#Create mineable coins list
	mineableCoinsEndpointList = []

	def openConfig(self, jsonConfig):
		with open(jsonConfig) as configFile:
			#Load Json data into python
			configData = json.load(configFile)
			#Load checkRateMinutes and store as variable
			self.checkRateMinutes = configData["AutoMiner"]["config"]["checkRateMinutes"]
			#Load profitDifferenceDollars and store as variable
			self.profitDifferenceDollars = configData["AutoMiner"]["config"]["profitDifferenceDollars"] 
			
			#Load algorithms data and create class
			for algorithm in configData["AutoMiner"]["algorithms"]:
				algorithmName = algorithm
				minerName = configData["AutoMiner"]["algorithms"][algorithm]["minerName"]
				p = configData["AutoMiner"]["algorithms"][algorithm]["p"]
				hr = configData["AutoMiner"]["algorithms"][algorithm]["hr"]
				fee = configData["AutoMiner"]["algorithms"][algorithm]["fee"]
				cost = configData["AutoMiner"]["algorithms"][algorithm]["cost"]
				hcost = configData["AutoMiner"]["algorithms"][algorithm]["hcost"]
				
				#Create AlgorithmData class and add to algorithmsList
				self.algorithmsList.append(AlgorithmData(algorithmName, minerName, p, hr, fee, cost, hcost))
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
	#End of parseMineableCoins Function
	
	
#This class contains the algorithm data loaded from the config file			
class AlgorithmData:
	def __init__(self, name, minerName, p, hr, fee, cost, hcost):
		#Load the algorithm name
		self.name = name
		#Load the miner name into this class variable
		self.minerName = minerName
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
			
			
			
			

#MAIN			
AutoMiner = AutoMiner()
AutoMiner.openConfig(configJson)
AutoMiner.pullAllCoins()
AutoMiner.generateMineableCoinEndpoints()

pprint(AutoMiner.mineableCoinsEndpointList)

#https://whattomine.com/coins/172-pasc-pascal.json?utf8=%E2%9C%93&hr=4041.0&p=900.0&fee=0.0&cost=0.06&hcost=0.0&commit=Calculate


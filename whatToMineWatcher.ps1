#Variables

$COIN_LIST_URL = "http://whattomine.com/calculators"






function Get-Coin-IDs
{
	#Get HTML
	$COIN_LIST_HTML = Invoke-WebRequest -URI $COIN_LIST_URL

	
	foreach($COIN_ID in $COIN_LIST_HTML.Links.outerHTML){
		#write-output $COIN_ID
		$TEST1 = $COIN_ID|%{$_.split('"')[1]}
		
		if(Invoke-WebRequest -URI $COIN_LIST_URL){
			
			if ($TEST1 -like '*coins*') { 
			
				write-output $TEST1
				$pos = $TEST1.IndexOf("-")
				write-output $TEST1.Substring($pos)
			}
			
		}
	}
	
}


Get-Coin-IDs



# Variables
#$DEBUG = $true
#$URL = "http://whattomine.com/coins.json"
#Need to determine where BTC Price is pulled from
#$BTC_PRICE = "950"


#$CoinNameArray = New-Object System.Collections.ArrayList
#$CoinTagArray = New-Object System.Collections.ArrayList
#$CoinAlgorithmArray = New-Object System.Collections.ArrayList
#revenue = btc_revenue x btc_price
#$CoinRevenueArray = New-Object System.Collections.ArrayList
#profit = revenue - power cost
#$CoinProfitArray = New-Object System.Collections.ArrayList


#$JSON = Invoke-WebRequest $URL | ConvertFrom-JSON
#foreach($COIN in $JSON.Coins.psobject.properties.name){

	#$CoinNameArray.Add($COIN)
	#$CoinTagArray.Add($JSON.Coins.$COIN.tag)
	#$CoinAlgorithmArray.Add($JSON.Coins.$COIN.algorithm)
	
	#$PROFIT = [Double]$BTC_PRICE * [Double]$JSON.Coins.$COIN.btc_revenue
	#$REVENUE = [Double]$PROFIT - [Double]"1.58"
	#$REVENUE = [math]::round($REVENUE,2)
	#write-output $COIN" -- Revenue:$"$PROFIT" -- Profit:$"$REVENUE
	
	#Index
	#write-output $$JSON.Coins.psobject.properties.name.IndexOf($COIN)	
#}

#write-output $CoinNameArray
#write-output $CoinTagArray
#write-output $CoinAlgorithmArray
#write-output $CoinProfitabilityArray
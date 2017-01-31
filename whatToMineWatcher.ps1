#Variables
$DEBUG = $true
$URL = "http://whattomine.com/coins.json"

$RUNNING = $true

$CoinNameArray = New-Object System.Collections.ArrayList
$CoinTagArray = New-Object System.Collections.ArrayList
$CoinAlgorithmArray = New-Object System.Collections.ArrayList
$CoinProfitabilityArray = New-Object System.Collections.ArrayList



#Invoke-WebRequest $URL |
#ConvertFrom-JSON |
#select -expand coins |
#select -expand . |
#Select tag, algorithm, profitability

$JSON = Invoke-WebRequest $URL | ConvertFrom-JSON
foreach($COIN in $JSON.Coins.psobject.properties.name){
$CoinNameArray.Add($COIN)
$CoinTagArray.Add($JSON.Coins.$COIN.tag)
$CoinAlgorithmArray.Add($JSON.Coins.$COIN.algorithm)
$CoinProfitabilityArray.Add($JSON.Coins.$COIN.profitability)
}

write-output $CoinNameArray
write-output $CoinTagArray
write-output $CoinAlgorithmArray
write-output $CoinProfitabilityArray




$TemplateParameterFileLocal = 'C:\Users\JWhite\Documents\Github\MineAutomator\config.json'

$JsonContent = (Get-Content $TemplateParameterFileLocal -Raw) | ConvertFrom-Json 

write-output $JsonContent
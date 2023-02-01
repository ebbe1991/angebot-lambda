# Angebot-Lambda

Diese AWS-Lambda-Function dient zur Pflege  von Angeboten einer Applikation. Die Angebote (Betreff + Nachricht) werden in einer DynamoDB mit einer optionalen Gültigkeit hinterlegt. 

Sofern das 'GültigBis' gepflegt ist, werden die Angebote mit einer TTL in der DynamoDB hinterlegt und nach einem Versatz von 7 Tagen zum 'GültigBis' gelöscht (Feature ist über die Umgebungsvariable 'TTL_FEATURE_ACTIVE' deaktivierbar).

## Voraussetzungen
- Python (3.9)
    - boto3
    - moto
    - pytest
    - aws_lambda_powertools

## Umgebungsvariablen
```sh
TTL_FEATURE_ACTIVE=0|1:int
ANGEBOT_TABLE_NAME=*:str
```

## Tests ausführen
```sh
pytest
```


# Api-Dokumentation (wip)

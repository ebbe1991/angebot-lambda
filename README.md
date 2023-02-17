# Angebot-Lambda

## Routen

### Angebot 

- POST api/angebot
- GET api/angebot/<id>
- GET api/angebot[?stichtag=YYYY-MM-DD]
- PUT api/angebot/<id>
- DELETE api/angebot/<id>


## Umgebungsvariablen
| Name                   | Beschreibung                                          |
|------------------------|-------------------------------------------------------|
| ANGEBOT_TABLE_NAME     | Name der Angebot DynamoDB-Table                       |
| TTL_FEATURE_ACTIVE     | Flag, ob TTL für die Angebot DynamoDB-Table aktiv ist |

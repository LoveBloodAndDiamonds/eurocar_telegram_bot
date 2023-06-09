# eurocar_telegram_bot
A bot for company "Europcar", that helps users create and send car rental requests.


## How to deploy:
- fill .sheets_google_credentions.json
- fill .env

### deploy with poetry:
- create poetry env
- poetry update
- install redis
- run redis server
- poetry run python3 -m bot

### deploy with docker:
- docker-compose up -d

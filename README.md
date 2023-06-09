# eurocar_telegram_bot
A bot for company "Europcar", that helps users create and send car rental requests.


## How to deploy:
- fill .sheets_google_credentions.json
- fill .env

<h4>deploy with poetry:</h4>
- create poetry env
- poetry update
- install redis
- run redis server
- poetry run python3 -m bot

<h4>deploy with docker:</h4>
- docker-compose up -d

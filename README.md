# Foto bot
A telegram bot (@FotoparadiesBot) hosted on fly.io that checks the website of fotoparadies for an update on photo orders.

## Setting the TOKEN
- Use `fly secrets set TOKEN=my-telegram-bot-token` to set the telegram token
- Use `fly secrets set API_KEY='my-api-key'` to set the API Key for JSON_BIN
    - use single quotes for keys containing special characters
    
## Running the bot
- Use `/set_shop XXXX` to set the 4 digit shop number.
- Use `/set_order XXXXXX` to set the 6 digit order number.
- Use `/status` to get the current settings.
- Use `/update` to get an update on your order.

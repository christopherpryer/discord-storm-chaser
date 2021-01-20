# discord-stormchaser
Discord bot to assist with storm-chasing for skiers and snowboarders.



# how-to

Fork this repo. Clone it. Open up the terminal. Navigate to the cloned repo.

## weatherbit api

Go to [weatherbit](https://www.weatherbit.io/account/dashboard) and set yourself up.

## discord dev

Go to [discord dev](https://discord.com/developers/applications/) prepare your bot application.

## create .env

Make a file called `.env` and place it in the root of the repo with the following configured:

```.env
DISCORD_GUILD=123456789
DISCORD_CHANNEL=123456789
DISCORD_TOKEN=123456789
API_KEY=123456789 # weatherbit
```
## set up venv

Run `python -m venv venv` and activate the `venv` using `source venv/scripts/actiave` or `venv\Scripts\activate` on windows. Run `pip install -r requirements.txt`.


## run the bot :rocket:

`python main.py`

## commands ⌨️

To get the 10d forecast for Windham Mountain in NY type `!weather windham ny 10d` in the bot's discord channel. (`!weather` or `!w`)

# cembot
Cembot is a Telegram bot written in Python. It helps people manage their debts and credits. The acronym cembot means: **C**ollective **E**xpenses **M**anagement **BOT**.

## Requirements
- Python 3
- `telepot`: a framework for Telegram Bot APIs. `telepot` can be installed using `pip`.
- `psycopg2`: a PostgreSQL adapter for Python. `psycopg2` can be installed using `pip`.
- a PostgreSQL running instance
  - install PostgreSQL
  - set up your database using `/schema.sql`

## Set up
1. Clone this repository
2. Get into it with `cd cembot`
3. Get your token from BotFather
4. Set an environment variable with an identificator like this: `CEM_` with appended the code of the desired language. This variable must be equal to your Telegram token. For example, if you want to set up an english bot you have to digit the following command: `export CEM_EN=[TOKEN]`. Note that the previous command does **not** make persistent your changes. If you want to you will have to add that line into `.bashrc`.
5. Start the bot with the following command:
```bash
python main.py [db name] [db user] [db password] [db host] [language code]
```
Database host is 127.0.0.1 if you have installed a local PostgreSQL instance.

## Supported languages
**The code of the language is surrounded by parenthesis**
- Italian (`IT`)
- English (`EN`), partial

## Running instances
- italian instance of cembot: [@it_cembot](https://t.me/it_cembot)

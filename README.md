# Telegram Message Aggregator

Telegram Message Aggregator is a Python project that collects messages from multiple Telegram channels and sends them to a single channel. The bot uses the Pyrogram library to interact with the Telegram API.

## Features

- Collects messages from multiple channels
- Filters out duplicate messages
- Sends messages to a single destination channel
- Shows progress bars while processing and sending messages
- Monitors channels for new messages and forwards them to the destination channel in real-time

## Files

- `bot.py`: The main script that connects to Telegram, collects messages, and sends them to the destination channel
- `register.py`: A script to register a new Pyrogram session, useful when using Docker or other containerized environments
- `config.py`: Configuration file containing a list of Telegram channel links
- `example.env`: An example of environment variables required for the project (API_ID, API_HASH, SESSION_NAME)
- `.env`: A file containing your own API_ID, API_HASH, and SESSION_NAME (not included in the repository for security reasons)

## Installation

1. Install Python 3.10 or higher
2. Clone the repository:

```
git clone https://github.com/NikitaPanferov/posts_stealer.git
cd telegram-message-aggregator
```

3. Install the required packages:

```
pip install -r requirements.txt
```

4. Create a `.env` file in the project directory and add your API_ID, API_HASH, and SESSION_NAME:

```
API_ID=your_api_id
API_HASH=your_api_hash
SESSION_NAME=your_session_name
```

5. Edit `config.py` to add the list of Telegram channel links and your destination channel link.

## Usage

1. Register a new session if needed (useful for Docker or other containerized environments):

```
python register.py
```

2. Start the bot:

```
python bot.py
```

3. The bot will collect messages from the specified channels and send them to your destination channel. Progress bars will be displayed during the process. The bot will also monitor the channels for new messages and forward them to the destination channel in real-time.

## License

This project is licensed under the MIT License.

## Contributing

Feel free to open issues or submit pull requests for any improvements or bug fixes.
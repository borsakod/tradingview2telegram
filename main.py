import logging
import logging.config

from flask import Flask, request
from telegram import Bot

telegram_token = '<telegram_bot_token>'
telegram_bot = Bot(token=telegram_token)

logging.config.fileConfig(fname='log.ini', disable_existing_loggers=True, defaults={'logfilename': 'tvsender.log'})
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # { "telegram_chat_id": "-1001456871846", "message": "Long #{{ticker}} at `{{close}}`" }
    try:
        if request.method == 'POST':
            json_data = request.get_json()
            logging.info(str(json_data))
            telegram_bot.sendMessage(chat_id=json_data['telegram_chat_id'], text=json_data['message'], parse_mode='MARKDOWN')
            return {'success': True}, 200
    except Exception as e:
        logging.exception(e, exc_info=True)
        return {'success': False, 'message': str(e)}, 400

if __name__ == '__main__':
    app.run(port=80, debug=True, host='0.0.0.0')
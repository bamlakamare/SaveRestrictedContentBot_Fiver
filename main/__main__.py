import glob
from pathlib import Path
from main.utils import load_plugins
import logging
from . import bot

from threading import Thread
from flask import Flask, jsonify
from decouple import config


PORT = config("PORT", default=None, cast=int)


# Flask application
app = Flask(__name__)


@app.route('/endpoint', methods=['GET'])
def simple_endpoint():
    return jsonify({"message": "Hello, World!"})


def run_flask():
    app.run(host='0.0.0.0', port=PORT, debug=True)


# Start Flask application in a separate thread
flask_thread = Thread(target=run_flask)
flask_thread.start()

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

path = "main/plugins/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        load_plugins(plugin_name.replace(".py", ""))

#Don't be a thief 
print("Successfully deployed!")
print("By MaheshChauhan • DroneBots")

if __name__ == "__main__":
    bot.run_until_disconnected()

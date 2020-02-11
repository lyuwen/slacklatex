#!/usr/bin/env python3
import os
import sys
import hmac
import time
import hashlib
import configparser
from io import BytesIO, FileIO
import matplotlib as mpl
mpl.use("pgf")
pgf_with_custom_preamble = {
  "pgf.texsystem": "pdflatex", # Use pdflatex
  "text.usetex": True,    # use tex renderer
  "pgf.rcfonts": False,   # don't setup fonts from rc parameters
  "pgf.preamble": [
     r"\usepackage{amsmath,amsfonts,amssymb}",  # Added some math packages
     ]
}
mpl.rcParams.update(pgf_with_custom_preamble)
import matplotlib.pyplot as plt
from flask import Flask, request
import slack

basepath = os.path.dirname(os.path.abspath(__file__))

config = configparser.ConfigParser()
config.read(os.path.join(basepath, 'config.ini'))
SLACK_SIGNING_SECRET = config.get('Slack', 'signing_secret')
API_TOKEN = config.get('Slack', 'bot_user_api_token')
app = Flask(__name__)
slack_client = slack.WebClient(token=API_TOKEN)

@app.route("/", methods=['POST'])
def render_latex():
    timestamp = request.headers['X-Slack-Request-Timestamp']
    if abs(time.time() - float(timestamp)) > 60 * 5:
        print("Timestamp not match")
        return
    sig_basestring = str.encode('v0:' + timestamp + ':') + request.get_data()
    my_signature = 'v0=' + hmac.new(
        str.encode(SLACK_SIGNING_SECRET),
        sig_basestring,
        digestmod=hashlib.sha256
        ).hexdigest()
    slack_signature = request.headers['X-Slack-Signature']
    if my_signature != slack_signature:
        print("Signature not match.")
    print(request.form['text'],file=sys.stderr)
    try:
        rendered = render_latex_mpl('{}'.format(request.form['text']), fontsize=12, dpi=300, format_='png')
    except Exception as e:
        print(e)
        return "Invalid LaTeX? {}".format(request.form['text'])
    #
    if request.form["channel_name"] == "directmessage":
      # DM
      channel = "@" + request.form["user_name"]
    else:
      channel = request.form["channel_name"]
      slack_client.channels_join(name=channel)
      channel = "#" + channel
    slack_client.files_upload(
        channels=channel,
        file=rendered,
        text=request.form['text'])
    slack_client.chat_postMessage(
        channel=channel,
        text=request.form['text'])
    return ""


def render_latex_mpl(formula, fontsize=12, dpi=300, format_='svg'):
    """Renders LaTeX formula into image.
    """
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0.0, 0.0, r'{}'.format(formula), fontsize=fontsize, va='center')
    buffer_ = BytesIO()
    fig.savefig(buffer_, dpi=dpi, transparent=True, format=format_, bbox_inches='tight', pad_inches=0.02)
    plt.close(fig)
    buffer_.seek(0)
    #print(buffer_.getvalue())
    return buffer_


if __name__=="__main__":
    app.run("0.0.0.0", port=5000)

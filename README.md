#slack-latex

This is a Slack bot that implements a `/latex` [slash command](https://api.slack.com/slash-commands).

Example usage from within Slack:

`/latex $ E = mc^2 $`

![Demo](https://cloud.githubusercontent.com/assets/1005545/13491495/8405756a-e0e7-11e5-8d22-d76b99ff7a36.gif)

This version has now been updated to work with the latest Slack API version.
This version also uses **matplotlib** to render the latex equations, though PDFLaTeX is still required.

## Installation

This server requires:

* [Flask](http://flask.pocoo.org/)
* [matplotlib](https://github.com/matplotlib/matplotlib)
* [slackclient](https://github.com/slackapi/python-slackclient)
* `pdflatex` from [TeXLive](https://www.tug.org/texlive/)

On a Ubuntu server, you can install all of these with the following command:

```bash
sudo apt-get install python3-pip texlive
sudo pip install --upgrade matplotlib slackclient flask
```

## Configuring slack-latex

`slack-latex` requires a [Bot User OAuth Access Token](https://api.slack.com/docs/oauth) 
and a [Signing Secret](https://api.slack.com/docs/verifying-requests-from-slack).
To begin with, create a new Slack App, enable **Incoming Webhooks**, **Slash Commands** and **Bots**.
Add permissions including `channels:join`, `channels:read`, `chat:write`, `commands`, `files:write`,
`im:read`, `im:write`, `users:read`, `incoming-webhook`, and install the App.
The bot user token can be found in *OAuth & Permission* section and the signing secret in *Basic Information*.

### Create a config file for slack-latex

Start by copying the example config file:

```bash
cp config.ini.example config.ini
```

Save the tokens into the config file, and keep it safe.

### Launch the server

Start up your server:

```bash
python3 main.py
```

Then, try testing out your new slash command.


## Known issues

* Slack slash command has a ~3 seconds timeout and due to the slow speed of the compilation of the LaTeX equation,
  it could happen that Slack will assume the command timed out while it actually is working and post the rendered
  equation some moment later.

# Duty Notify
Notify your duty when you need it.

# Introduction
This is a tool for our school, St. Mark's School students only.
And, yes, this is for notifying your duty.

# WARNING
Do not execute this everyday. Currently, it will not cache what this have received in the past.
Over-executing will cause Spam issue. You will not like it.

# Usage
Create a 'config.json' file under this directory. Containing the followings:
```json
[
  {
    "name": "<Your Name>",
    "email": "<Your email>"
  }, {
    "name": "<Another name>",
    "email": "<Another email>"
  }
]
```

In fact, Regular Express is used on `name` for searching. Therefore, you can use RegExp in it.

Then, go to [Google Developers Console](https://console.developers.google.com).
Create a credentials with Gmail API enabled and save that key, as JSON, to `client_id.json`.

Launch this with invoking `main.py`. This ment to be a cron job.

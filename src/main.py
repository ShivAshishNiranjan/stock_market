from datetime import datetime
from datetime import timedelta

from flask import Flask, render_template

from bse.corporate_actions import get_corporate_actions
from bse.live_announcement import get_live_announcement

app = Flask(__name__)
port = 8082


@app.route("/")
def home_page():
    return render_template("home_page.html", port=port)


@app.route("/live_announcements")
def live_announcements():
    start_date = datetime.today().strftime('%Y%m%d')
    end_date = datetime.today().strftime('%Y%m%d')
    live_announcement_types = ["Board+Meeting", "Corp.+Action", "AGM/EGM"]
    dividend = []
    bonus = []
    split = []
    buyback = []
    for corporate_action in live_announcement_types:
        result = get_live_announcement(corporate_action, start_date, end_date)
        if result.get("dividend"):
            dividend.append(result.get("dividend"))
        if result.get("bonus"):
            bonus.append(result.get("bonus"))
        if result.get("split"):
            split.append(result.get("split"))
        if result.get("buyback"):
            buyback.append(result.get("buyback"))

    return render_template("live_announcements.html", dividend=dividend, bonus=bonus, split=split, buyback=buyback,
                           start_date=datetime.today().strftime('%Y-%m-%d'),
                           end_date=datetime.today().strftime('%Y-%m-%d'))


@app.route("/corporate_actions")
def corporate_actions():
    start_date = (datetime.now() + timedelta(days=1)).strftime('%Y%m%d')
    end_date = "20211231"
    result = get_corporate_actions(start_date, end_date)
    return render_template("corporate_actions.html", dividend=result.get("dividend"), bonus=result.get("bonus"),
                           split=result.get("split"), buyback=result.get("buyback"),
                           start_date=(datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
                           end_date="2021-12-31")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, debug=True)

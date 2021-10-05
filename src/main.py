from flask import Flask, render_template
from bse.live_announcement import get_corporate_action
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def index():
    start_date = datetime.today().strftime('%Y%m%d')
    end_date = datetime.today().strftime('%Y%m%d')
    corporate_actions = ["Board+Meeting", "Corp.+Action", "AGM/EGM"]
    dividend = []
    bonus = []
    split = []
    buyback = []
    for corporate_action in corporate_actions:
        result = get_corporate_action(corporate_action, start_date, end_date)
        if result.get("dividend"):
            dividend.append(result.get("dividend"))
        if result.get("bonus"):
            bonus.append(result.get("bonus"))
        if result.get("split"):
            split.append(result.get("split"))
        if result.get("buyback"):
            buyback.append(result.get("buyback"))

    return render_template("index.html", dividend=dividend, bonus=bonus, split=split, buyback=buyback,
                           start_date=datetime.today().strftime('%Y-%m-%d'),
                           end_date=datetime.today().strftime('%Y-%m-%d'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082, debug=True)

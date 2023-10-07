from flask import Flask, render_template, url_for, request
from scrab_curr import API

app = Flask(__name__)


def convert_usd_to_ugx(usd: int | float) -> float:
    one_usd = float(API["curr_ex"].split()[-2])
    return round(usd * one_usd, 4)


def convert_ugx_to_usd(ugx: int | float) -> float:
    one_ugx = 1 / float(API["curr_ex"].split()[-2])
    return round(ugx * one_ugx, 4)


@app.route("/", methods=["POST", "GET"])
def index():
    on_start = "active"
    on_curr = ""
    unit_ugx = round(1 / float(API["curr_ex"].split()[-2]), 4)
    cov_ugx, cov_usd = (0, 0)
    if request.method == "POST":
        usd = request.form["usd"]
        ugx = request.form["ugx"]
        if usd:
            cov_ugx = convert_usd_to_ugx(int(usd))
            cov_usd = usd
        elif ugx:
            cov_usd = convert_ugx_to_usd(int(ugx))
            cov_ugx = ugx
        on_start = ""
        on_curr = "active"
    return render_template(
        "index.html",
        unit_ugx=unit_ugx,
        API=API,
        on_start=on_start,
        on_curr=on_curr,
        cov_ugx=cov_ugx,
        cov_usd=cov_usd,
    )


if __name__ == "__main__":
    app.run(debug=True)

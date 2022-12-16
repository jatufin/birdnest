from src.app import app

from flask import redirect, render_template

from src.config import PAGE_REFRESH, SHOW_ADDTIONAL_DATA


@app.route("/")
def main():
    return redirect("/index")


@app.route("/index")
def index():
    pilots = app.drones.get_offending_pilots()

    return render_template("index.html",
                           pilots=pilots,
                           page_refresh=PAGE_REFRESH,
                           show_additional_data=SHOW_ADDTIONAL_DATA)

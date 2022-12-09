from app import app

from flask import redirect, render_template

from config import PAGE_REFRESH

@app.route("/")
def main():
    return redirect("/index")


@app.route("/index")
def index():
    pilots = app.drones.get_offending_pilots()

    return render_template("index.html",
                           pilots=pilots,
                           page_refresh=PAGE_REFRESH)

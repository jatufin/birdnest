from app import app

from flask import redirect, render_template


@app.route("/")
def main():
    return redirect("/index")

@app.route("/index")
def index():
    # Static test data
    pilots = \
        [
            {
                "distance":     10,
                "firstName":	"Makenzie",
                "lastName":	"Hackett",
                "email":	"makenzie.hackett@example.com"
            },
            {
                "distance":     20,
                "firstName":	"Foo",
                "lastName":	"Bar",
                "email":	"foo@bar.baz"
            }
        ]
    return render_template("index.html", pilots=pilots)
    

from flask import Flask

app = Flask(_name_)


@app.route("/")
def index():
    return "Hello from Flask!"

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=8000)
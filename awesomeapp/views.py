from awesomeapp import app, db


@app.route('/')
def hello():
    return 'Hello'
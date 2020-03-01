from flask import Flask, render_template

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/scores')
def scores():
    return render_template("scores.html")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

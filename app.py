from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weed')
def weed(): 
    return render_template('weed.html')

@app.route('/meth')
def meth(): 
    return render_template('meth.html')

@app.route('/cocaine')
def cocaine(): 
    return render_template('cocaine.html')


if __name__ == '__main__':
    app.run(debug=True)

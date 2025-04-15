from flask import Flask, render_template, request, redirect, url_for
from connection import DatabaseConnection
from weed import WeedStrainCreator

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

@app.route('/add-strain', methods=['GET', 'POST'])
def add_strain():
    if request.method == 'GET':
        connection = DatabaseConnection()
        db, cursor = connection.get_connection()
        creator = WeedStrainCreator(db, cursor)
        base_strains = creator.get_base_strains() 
        ingredients = creator.get_ingredients()
        return render_template('add_strain.html', base_strains = base_strains, ingredients = ingredients)

    if request.method == 'POST':
        connection = DatabaseConnection()
        db, cursor = connection.get_connection()

@app.route("/view-weed")
def view_weed():
    return "List of all weed strains (to be implemented)"

@app.route("/search-weed")
def search_weed():
    return "Search weed strains (to be implemented)"


if __name__ == "__main__":
    app.run(debug=True)

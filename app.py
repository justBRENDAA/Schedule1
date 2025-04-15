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
        creator = WeedStrainCreator(db, cursor)

        strain_name = request.form.get('strain_name') 
        market_price = float(request.form.get('market_price'))
        addictiveness =  float(request.form.get('addictiveness'))/100
        base_strain_id = int(request.form.get('base_strain'))
        ingredient_ids = request.form.getlist('ingredient[]')
        sale_price = creator.calc_sale_price(addictiveness, market_price)
        total_profit = creator.calc_total_profit(sale_price, ingredient_ids, base_strain_id)
        ingredient_ids = ", ".join(x for x in ingredient_ids)

        print("Strain Name:", strain_name)
        print("Market Price:", market_price)
        print("Addictiveness:", addictiveness)
        print("Base Strain ID:", base_strain_id)
        print("Selected Ingredients:", ingredient_ids)
        print("Sale price: ", sale_price)
        print("Total profit: ", total_profit)

        creator.sql_insert(base_strain_id, ingredient_ids, strain_name, market_price, addictiveness, sale_price, total_profit)

        return redirect(url_for('insertion_confirmation'))

@app.route("/insertion-confirmation")
def insertion_confirmation():
    return render_template("confirmation.html")

@app.route("/view-weed")
def view_weed():
    return "List of all weed strains (to be implemented)"

@app.route("/search-weed")
def search_weed():
    return "Search weed strains (to be implemented)"


if __name__ == "__main__":
    app.run(debug=True)

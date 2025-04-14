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

@app.route("/add-weed", methods=["GET", "POST"])
def add_weed():
    db_obj = DatabaseConnection()
    db, cursor = db_obj.get_connection()
    creator = WeedStrainCreator(db, cursor)

    if request.method == "POST":
        strain_name = request.form["strain_name"]
        market_price = float(request.form["market_price"])
        addictiveness = float(request.form["addictiveness"]) / 100
        base_weed_id = int(request.form["base_weed_id"])
        ingredient_ids = request.form.getlist("ingredient_ids")
        ingredient_ids_str = ", ".join(ingredient_ids)

        # Fetch ingredient prices to calculate cost
        all_ingredients = creator.get_ingredients()
        ingredient_costs = {str(row[0]): float(row[2]) for row in all_ingredients}
        total_ingredient_cost = sum(ingredient_costs[iid] for iid in ingredient_ids)

        # Get base weed info
        base_strains = creator.get_base_strains()
        base_weed_price = next((float(bud_price) for ID, _, bud_price, *_ in base_strains if ID == base_weed_id), 0.0)

        sale_price = creator.calc_sale_price(addictiveness, market_price)
        total_profit = sale_price - total_ingredient_cost - base_weed_price

        sql = "INSERT INTO custom_strains (base_weed_id, ingredient_ids, name, market_price, addictiveness, sale_price, total_profit) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (base_weed_id, ingredient_ids_str, strain_name, market_price, addictiveness, sale_price, total_profit)
        cursor.execute(sql, val)
        db.commit()

        db_obj.close()
        return "Strain added successfully!"

    # GET request: show the form
    base_strains = creator.get_base_strains()
    ingredients = creator.get_ingredients()
    db_obj.close()
    return render_template("add_weed.html", base_strains=base_strains, ingredients=ingredients)


@app.route("/view-weed")
def view_weed():
    return "List of all weed strains (to be implemented)"

@app.route("/search-weed")
def search_weed():
    return "Search weed strains (to be implemented)"


if __name__ == '__main__':
    app.run(debug=True)

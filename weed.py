class WeedStrainCreator: 
    def __init__ (self, db, cursor):
        self.db = db
        self.cursor = cursor
        
    def get_base_strains(self):
        self.cursor.execute("SELECT * FROM og_weed")
        return self.cursor.fetchall()                  # List of tuples (id, name, price)

    def get_ingredients(self):
        self.cursor.execute("SELECT * FROM ingredients")
        return self.cursor.fetchall()                  # List of tuples (id, name, price)

    def calc_sale_price(self, addictiveness, market_price):
        if addictiveness == 1:
            return market_price + 35
        elif addictiveness >= 0.9:          
            return market_price + 30
        elif addictiveness >= 0.7:
            return market_price + 25
        elif addictiveness >= 0.5:
            return market_price + 20
        elif addictiveness >= 0.3:
            return market_price + 15
        else: 
            return market_price + 10

    def input_validation(self, options, user_selection):
        if user_selection < 1 or user_selection > options:
            print("Invalid option")

    def calc_total_profit(self, sale_price, ingredient_ids, base_strain_id):
        ingredients = self.get_ingredients()
        ingredient_index = [int(x) - 1 for x in ingredient_ids]  # do this because the ingredients list is 0 indexed and our ids are 1 indexed
        ingredient_cost = sum(float(ingredients[i][2]) for i in ingredient_index)
        
        base_strains = self.get_base_strains()
        base_strain_index = base_strain_id - 1  # again the list is 0 indexed and our ids are 1 indexed
        base_strain_bud_cost = float(base_strains[base_strain_index][2])
        

        total_profit = sale_price - ingredient_cost - base_strain_bud_cost

        return total_profit
        
        



    def sql_insert(self, base_strain_id, ingredient_ids, strain_name, market_price, addictiveness, sale_price, total_profit):
        sql = "INSERT INTO custom_strains (base_weed_id, ingredient_ids, name, market_price, addictiveness, sale_price, total_profit) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (base_strain_id, ingredient_ids, strain_name, market_price, addictiveness, sale_price, total_profit)
        self.cursor.execute(sql, val)
        
        self.db.commit()
        

    def create_strain(self):
        # BASE STRAIN INFORMATION
        base_strains = self.get_base_strains()   # list of tuples with all base weed information
        
        print("BASE WEED")
        for ID, name, bud_price, _, _, _ in base_strains:   # print menu for user to select
            print(f"{ID}. {name} - ${bud_price:.2f}")

        base_strain_id = int(input("Enter base weed ID: "))
        base_weed_info = base_strains[base_strain_id-1]  # select only the information for the base weed chosen from the list of tuples
        print()

        # INGREDIENT INFORMATION
        ingredients = self.get_ingredients()     # list of tuples with all ingredient information

        print("INGREDIENTS")
        for ID, name, price in ingredients:      # print menu for user to select
            print(f"{ID}. {name} - ${price:.2f}")

        all_ingredients_used = []
        while True: 
            ingredient_id = int(input("Enter the ingredient ID: "))

            ingredient_info = ingredients[ingredient_id-1]  #-1 because list of tuples is 0 indexed
            all_ingredients_used.append(ingredient_info)  # stores tuple with ID, NAME, COST
            print()
            
            keep_going = input("Add another ingredient? (y/n): ").lower()
            if keep_going != 'y':
                break

        strain_name = input("Enter the new strain name: ")                  # this information is provided in game
        market_price = float(input("Enter the market price: "))             # this information is provided in game
        addictiveness = float(input("Enter the strains addictiveness: "))   # this information is provided in game
        addictiveness = addictiveness/100
        
        total_ingredient_cost = sum(float(price) for ID, name, price in all_ingredients_used)
        sale_price = self.calc_sale_price(addictiveness, market_price)
        ingredient_ids = ", ".join(str(ID) for ID, _, _ in all_ingredients_used)

        total_profit = sale_price - total_ingredient_cost - float(base_weed_info[2])

        print(f"\nStrain: {strain_name}")
        print(f"Base: {base_weed_info[1]}")
        for i, (_, name, _) in enumerate(all_ingredients_used, 1):
            print(f"Ingredient {i}: {name}")
        print(f"Sale Price: ${sale_price:.2f}")
        print(f"Total Ingredient Cost: ${total_ingredient_cost:.2f}\n")
        print(f"Total Profit: ${total_profit:.2f}\n")

        
        
        confirm = input("Save this strain to the database? (y/n): ").lower()
        if confirm == 'y':
            sql = "INSERT INTO custom_strains (base_weed_id, ingredient_ids, name, market_price, addictiveness, sale_price, total_profit) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (base_strain_id, ingredient_ids, strain_name, market_price, addictiveness, sale_price, total_profit)
            self.cursor.execute(sql, val)
    
            self.db.commit()
            print(self.cursor.rowcount, "strain inserted")
        else:
            print("Strain not saved.")
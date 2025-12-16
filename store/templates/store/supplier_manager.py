def send_order_to_supplier(order):
    if order.country.lower() == 'india':
        # ... (Printrove API Logic Here) ...
        # If success:
        order.supplier_name = "Printrove"
        order.print_cost = 300 # API response-ல இருந்து எடுக்கணும்
        order.shipping_cost = 50
    else:
        # ... (Printify API Logic Here) ...
        # If success:
        order.supplier_name = "Printify"
        order.print_cost = 600 # Convert USD to INR
        order.shipping_cost = 200

    # 🔥 Update Profit Automatically
    order.save() # This triggers the calculate_profit method in models.py
    return True
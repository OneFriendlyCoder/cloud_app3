from flask import Blueprint, request, jsonify, session
from shopeasy.dynamodb import get_cart, update_cart
from shopeasy.models import Product

cart_bp = Blueprint("cart", __name__)

@cart_bp.route("/add", methods=["POST"])
def add_to_cart():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json(force=True)
    product_id = data.get("product_id")
    quantity = int(data.get("quantity", 1))
    
    if not product_id:
        return jsonify({"error": "product_id is required"}), 400
        
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
        
    items = session.get("cart", [])
    
    # Check if item already in cart
    found = False
    for item in items:
        if item.get("product_id") == product_id:
            item["quantity"] += quantity
            found = True
            break
            
    if not found:
        items.append({
            "product_id": str(product_id),
            "name": product.name,
            "price": str(product.price), # DynamoDB floats must be strings or Decimals, string is safer for JSON
            "quantity": quantity
        })
        
    session["cart"] = items
    session.modified = True
    return jsonify({"status": "success"})

@cart_bp.route("/save", methods=["POST"])
def save_cart():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401

    user_id = session["user_id"]
    items = session.get("cart", [])
    update_cart(user_id, items)
    return jsonify({"status": "success", "cart": {"user_id": user_id, "items": items}})

@cart_bp.route("/remove", methods=["POST"])
def remove_from_cart():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json(force=True)
    product_id = str(data.get("product_id"))
    
    if not product_id:
        return jsonify({"error": "product_id is required"}), 400
        
    items = session.get("cart", [])
    items = [item for item in items if str(item.get("product_id")) != product_id]
    
    session["cart"] = items
    session.modified = True
    return jsonify({"status": "success"})

@cart_bp.route("/clear", methods=["POST"])
def clear_cart():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401

    session["cart"] = []
    session.modified = True
    return jsonify({"status": "success"})

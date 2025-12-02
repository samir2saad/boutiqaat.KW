import requests

def main(conversationId:str, language: str = "english", cart_items: str = "", total_amount: str = "") -> dict:
    """
    Display shopping cart contents and options to customer.

    Args:
        phone_number: The recipient's phone number in international format (e.g., "+201033505065")
        language: Selected language ("english" or "arabic")
        cart_items: Current cart items summary (optional)
        total_amount: Total cart amount (optional)

    Returns:
        dict: The API response
    """
     # WhatsApp API endpoint
    url = f"https://system.trypair.ai/v1/ai-agent/conversations/{conversationId}/messages/interactive"
    # Authorization header with your token
    headers = {
        "Authorization": "Bearer z5XAntXPnY+RLPVQyaNgCZNTArFtXq6mOf+7mHyh+CniMbD7G9ZuiTC2yhInIGPuJM+HoVB/NdEKNO1P31Y246nqwjP6KimXUt7igRibIgj4KQHpQLbkuQqhTRF6XTK9xyaipZFUOTGJotXfe/VckfiSgRFTx4wolQa8OGm2WecGkMOLrvaPqLPoomEYgg==",
        "Content-Type": "application/json"
    }

    # Define content based on language
    if language.lower() == "arabic":
        header_text = "🛒 سلة التسوق"
        if cart_items and total_amount:
            body_text = f"محتويات سلة التسوق:\n\n{cart_items}\n\n💰 المجموع الفرعي: {total_amount} دينار كويتي\n🚚 رسوم التوصيل: 1 دينار كويتي"
        elif cart_items:
            body_text = f"محتويات سلة التسوق:\n\n{cart_items}"
        else:
            body_text = "سلة التسوق فارغة حالياً.\n\nابدأ التسوق لإضافة منتجات إلى سلتك!"
        footer_text = "تسوق آمن"
        buttons = [
            {
                "type": "reply",
                "reply": {
                    "id": "cart_checkout",
                    "title": "✅ إتمام الطلب"
                }
            },
            {
                "type": "reply",
                "reply": {
                    "id": "cart_continue",
                    "title": "🛍️ متابعة التسوق"
                }
            },
            {
                "type": "reply",
                "reply": {
                    "id": "cart_clear",
                    "title": "🗑️ إفراغ السلة"
                }
            }
        ]
    else:
        header_text = "🛒 Shopping Cart"
        if cart_items and total_amount:
            body_text = f"Cart Contents:\n\n{cart_items}\n\n💰 Subtotal: {total_amount} KWD\n🚚 Delivery Fee: 1 KWD\n\nChoose what you'd like to do:"
        elif cart_items:
            body_text = f"Cart Contents:\n\n{cart_items}\n\nChoose what you'd like to do:"
        else:
            body_text = "Your cart is currently empty.\n\nStart shopping to add products to your cart!"
        footer_text = "Secure Shopping"
        buttons = [
            {
                "type": "reply",
                "reply": {
                    "id": "cart_checkout",
                    "title": "✅Checkout"
                }
            },
            {
                "type": "reply",
                "reply": {
                    "id": "cart_continue",
                    "title": "🛍️ Continue "
                }
            },
            {
                "type": "reply",
                "reply": {
                    "id": "cart_clear",
                    "title": "🗑️ Clear Cart"
                }
            }
        ]

    # Payload for cart display
 payload = {
        "interactive_type": "quick_reply",
  "body_text": body_text,
  "header_text": header_text,
  "footer_text": footer_text,
  "quick_reply_config": {
    "quick_reply_buttons": buttons
  }
    }
    # Send the request
    response = requests.post(url, headers=headers, json=payload)

    print("Status Code:", response.status_code)

    try:
        result = response.json()
        print("Response JSON:", result)
    except ValueError:
        result = {"error": "Invalid JSON response", "raw": response.text}
        print("Raw response:", response.text)

    return {
        "result": result
    }

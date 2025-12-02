import requests
import json

def main(conversationId: str, language: str = "english", total_amount: str = None) -> dict:
    """
    Sends a WhatsApp message requesting the customer's location for delivery,
    optionally showing the total amount.

    Args:
        phone_number (str): The recipient's phone number in international format (e.g., "+201033505065").
        language (str): Selected language ("english" or "arabic"). Default is "english".
        total_amount (str, optional): Total amount of the order (e.g., "2.9 KWD" or "٣ د.ك").

    Returns:
        dict: The API response.
    """

    # WhatsApp API endpoint
    url = f"https://system.trypair.ai/v1/ai-agent/conversations/{conversationId}/messages/location-request"

    headers = {
        "Authorization": "Bearer So+MR00BCG1dpI+EMkOiwDcQbBxUIxdcC9kwGof/zhc9vtyDtMAWpMqEs/fdzPMVCX2CBCe4dXo8J0nsLWGWOZwJnFe/UfSqJ7fqNjZ6Iq/1koVlRePxtwRa2mcbImN/0zwelBhcs4eJ32nSCqk1+IFb705/F3xT2BNNWPAZsK9DxNzi4Serm1gVxyr9CA==",
        "Content-Type": "application/json"
    }


    # Build message text based on language
    if language.lower() == "arabic":
        if total_amount:
            body_text = (
                f"📍 طلب الموقع للتوصيل\n"
                f"السعر الإجمالي: {total_amount}\n\n"
                "يرجى مشاركة موقعك لنتمكن من توصيل طلبك. اضغط على الزر أدناه لمشاركة موقعك الحالي.\n\n"
                "🚚 سيتم التوصيل خلال 2-4 أيام عمل"
            )
        else:
            body_text = (
                "📍 طلب الموقع للتوصيل\n\n"
                "يرجى مشاركة موقعك لنتمكن من توصيل طلبك. اضغط على الزر أدناه لمشاركة موقعك الحالي.\n\n"
                "🚚 سيتم التوصيل خلال 2-4 أيام عمل"
            )
    else:
        if total_amount:
            body_text = (
                f"📍 Location Request for Delivery\n"
                f"Total Price: {total_amount}\n\n"
                "Please share your location so we can deliver your order. Tap the button below to share your current location.\n\n"
                "🚚 Delivery within 2-4 business days"
            )
        else:
            body_text = (
                "📍 Location Request for Delivery\n\n"
                "Please share your location so we can deliver your order. Tap the button below to share your current location.\n\n"
                "🚚 Delivery within 2-4 business days"
            )

    # Payload for WhatsApp interactive message
 payload = {
             "text": body_text
                 }

    # Send the request
    response = requests.post(url, headers=headers, json=payload)

    # Log response
    print("Status Code:", response.status_code)
    try:
        result = response.json()
        print("Response JSON:", json.dumps(result, indent=2, ensure_ascii=False))
    except ValueError:
        result = {"error": "Invalid JSON response", "raw": response.text}
        print("Raw response:", response.text)

    return {"result": result}

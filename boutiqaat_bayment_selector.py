import requests
import json

def main(conversationId:str, language: str = "english", total_amount: str = "", delivery_address: str = "", building_number: str = "", department_number: str = "") -> dict:
    """
    Send payment method selection options to customer with address geocoding.

    Args:
        phone_number: The recipient's phone number in international format (e.g., "+201033505065")
        language: Selected language ("english" or "arabic")
        total_amount: Total order amount including delivery (optional)
        delivery_address: Delivery address (coordinates will be converted to readable address)
        building_number: Building number (optional)
        department_number: Apartment/Department number (optional)

    Returns:
        dict: The API response with success message
    """
    # WhatsApp API endpoint
    url = f"https://system.trypair.ai/v1/ai-agent/conversations/{conversationId}/messages/interactive"
    # Authorization header with your token
    headers = {
        "Authorization": "Bearer So+MR00BCG1dpI+EMkOiwDcQbBxUIxdcC9kwGof/zhc9vtyDtMAWpMqEs/fdzPMVCX2CBCe4dXo8J0nsLWGWOZwJnFe/UfSqJ7fqNjZ6Iq/1koVlRePxtwRa2mcbImN/0zwelBhcs4eJ32nSCqk1+IFb705/F3xT2BNNWPAZsK9DxNzi4Serm1gVxyr9CA==",
        "Content-Type": "application/json"
    }

    readable_address = delivery_address
    
    # Add building and apartment details to the address
    if readable_address and (building_number or department_number):
        address_suffix = []
        
        if language.lower() == "arabic":
            # Arabic format
            if building_number:
                address_suffix.append(f"عمارة رقم {building_number}")
            if department_number:
                address_suffix.append(f"شقة رقم {department_number}")
            
            if address_suffix:
                readable_address = f"{delivery_address}، {' ، '.join(address_suffix)}"
        else:
            # English format
            if building_number:
                address_suffix.append(f"Building No. {building_number}")
            if department_number:
                address_suffix.append(f"Apartment No. {department_number}")
            
            if address_suffix:
                readable_address = f"{delivery_address}, {', '.join(address_suffix)}"
        
        print(f"Final address with building details: {readable_address}")

    # Define content based on language
    if language.lower() == "arabic":
        header_text = "💳 اختيار طريقة الدفع"
        if total_amount and readable_address:
            body_text = f"📍 عنوان التوصيل: {readable_address}\n💰 المبلغ الإجمالي: {total_amount} دينار كويتي\n\nيرجى اختيار طريقة الدفع المفضلة لديك:"
        elif total_amount:
            body_text = f"💰 المبلغ الإجمالي: {total_amount} دينار كويتي\n\nيرجى اختيار طريقة الدفع المفضلة لديك:"
        elif readable_address:
            body_text = f"📍 عنوان التوصيل: {readable_address}\n\nيرجى اختيار طريقة الدفع المفضلة لديك:"
        else:
            body_text = "يرجى اختيار طريقة الدفع المفضلة لديك:"
        footer_text = "آمن ومضمون"
        buttons = [
            {

                    "id": "payment_knet",
                    "text": "💳 كي نت (K-Net)"
                }
            ,
            {

                    "id": "payment_credit",
                    "text": "💳 بطاقة ائتمان"
                }
            ,
            {

                    "id": "payment_cash",
                    "text": "💵 الدفع نقداً"
                }
            
        ]
    else:
        header_text = "💳 Payment Method Selection"
        if total_amount and readable_address:
            body_text = f"📍 Delivery Address: {readable_address}\n💰 Total Amount: {total_amount} KWD\n\nPlease select your preferred payment method:"
        elif total_amount:
            body_text = f"💰 Total Amount: {total_amount} KWD\n\nPlease select your preferred payment method:"
        elif readable_address:
            body_text = f"📍 Delivery Address: {readable_address}\n\nPlease select your preferred payment method:"
        else:
            body_text = "Please select your preferred payment method:"
        footer_text = "Secure & Safe"
        buttons = [
            {

                    "id": "payment_knet",
                    "text": "💳 K-Net"
                }
            ,
            {
                    "id": "payment_credit",
                    "text": "💳 Credit Card"
                }
            ,
            {

                    "id": "payment_cash",
                    "text": "💵 Cash on Delivery"
                }

        ]

    # Payload for payment selection
    payload = {
        "interactive_type": "quick_reply",
  "body_text": body_text,
  "header_text": header_text,
  "footer_text": footer_text,
  "quick_reply_config": {
    "quick_reply_buttons":buttons
  }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return {
            "result": json.dumps(response.json())
        }
    except Exception as e:
        return {"result": str(e)}

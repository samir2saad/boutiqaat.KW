import requests
import json

def main(link_url: str, caption: str, cta_text: str, header: str,conversationId:str) -> dict:
    """
    Sends an interactive message with a clickable button (link) via WhatsApp Business API.

    Args:
        link_url (str): The URL to open when button is clicked.
        caption (str): Body text of the message.
        cta_text (str): The text label on the button.
        header (str): The header text.
        conversationId (str): The ID of the conversation to send the message to.

    Returns:
        dict: API response or error message.
    """

    url = f"https://system.trypair.ai/v1/ai-agent/conversations/{conversationId}/messages/interactive"

    headers = {
        "Authorization": "Bearer So+MR00BCG1dpI+EMkOiwDcQbBxUIxdcC9kwGof/zhc9vtyDtMAWpMqEs/fdzPMVCX2CBCe4dXo8J0nsLWGWOZwJnFe/UfSqJ7fqNjZ6Iq/1koVlRePxtwRa2mcbImN/0zwelBhcs4eJ32nSCqk1+IFb705/F3xT2BNNWPAZsK9DxNzi4Serm1gVxyr9CA==",
        "Content-Type": "application/json"
    }

    payload = {
            "interactive_type": "cta_button",
    "body_text": caption,
    "header_text": header,
    "footer_text": "Click the button below",
    "cta_button_config": {
        "cta_buttons": [
        {
            "type": "url",
            "display_text": cta_text,
            "url": link_url
        }
        ]
    }
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return {
            "result": json.dumps(response.json())
        }
    except Exception as e:
        return {
            "result": str(e)
        }

import requests
import json

def main(latitude: str, longitude: str, conversationId: str,direction:str ,location_name:str,caption:str="") -> dict:
    """
    Sends a location message to a conversation.
    
    Args:
        latitude (str): The latitude of the location.
        longitude (str): The longitude of the location.
        conversationId (str): The ID of the conversation to send the message to.
        direction (str): The address of the location.
        location_name (str): The name of the location.
        caption (str): A caption for the location.
    
    Returns:
        dict: API response or error message.
    """
    url = f"https://system.trypair.ai/v1/ai-agent/conversations/{conversationId}/messages/location"

    headers = {
        "Authorization": "Bearer So+MR00BCG1dpI+EMkOiwDcQbBxUIxdcC9kwGof/zhc9vtyDtMAWpMqEs/fdzPMVCX2CBCe4dXo8J0nsLWGWOZwJnFe/UfSqJ7fqNjZ6Iq/1koVlRePxtwRa2mcbImN/0zwelBhcs4eJ32nSCqk1+IFb705/F3xT2BNNWPAZsK9DxNzi4Serm1gVxyr9CA==",
        "Content-Type": "application/json"
    }

    payload = {
  "latitude": latitude,
  "longitude": longitude,
  "name": location_name,
  "address": direction,
  "text": caption
}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return {
            "result": json.dumps(response.json())
        }
    except Exception as e:
        return {"result": str(e)}

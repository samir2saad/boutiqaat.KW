import requests
import json

def main(media_url:str, caption:str, conversationId:str, media_type:str ="image" ) -> dict:
    """
    Sends a media message with a caption to a conversation.
    
    Args:
        media_url (str): URL of the media to send.
        caption (str): Caption to include with the media.
        conversationId (str): The ID of the conversation to send the message to.
        media_type (str): Type of media ("image", "video", etc.). Defaults to "image".
    
    Returns:
        dict: API response or error message.
    """
    url = f"https://system.trypair.ai/v1/ai-agent/conversations/{conversationId}/messages/media"

    headers = {
        "Authorization": "Bearer z5XAntXPnY+RLPVQyaNgCZNTArFtXq6mOf+7mHyh+CniMbD7G9ZuiTC2yhInIGPuJM+HoVB/NdEKNO1P31Y246nqwjP6KimXUt7igRibIgj4KQHpQLbkuQqhTRF6XTK9xyaipZFUOTGJotXfe/VckfiSgRFTx4wolQa8OGm2WecGkMOLrvaPqLPoomEYgg==",
        "Content-Type": "application/json"
    }

    payload = {
  "media_url": media_url,
  "media_type": media_type,
  "caption": caption
}


    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return{
            "result":json.dumps(response.json())
        } 
    except Exception as e:
        return {"result": str(e)}

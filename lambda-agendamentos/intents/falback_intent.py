import json

def handle_fallback_intent(event):
    return {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                "name": "FallbackIntent", 
                "state": "Failed"
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": "Desculpe, não entendi a sua solicitação. Pode me dizer novamente ou fornecer mais detalhes?"
            }
        ]
    }

import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def handle_fallback_intent(event):
    user_input = event.get('inputTranscript', '').strip()
    logger.debug(f"Entrada do usuário: {user_input}")

    if user_input:
        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "ElicitIntent"
                },
                "intent": {
                    "name": "FallbackIntent",
                    "state": "InProgress"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": f"Desculpe, o valor '{user_input}' não é reconhecido. Por favor, tente novamente com uma das opções válidas."
                },
                {
                    "contentType": "ImageResponseCard",
                    "imageResponseCard": {
                        "title": "Por favor, selecione uma opção:",
                        "buttons": [
                            {"text": "Agendar compromisso", "value": "Agendar compromisso"},
                            {"text": "Listar compromissos", "value": "Listar compromissos"},
                            {"text": "Editar compromisso", "value": "Editar compromisso"},
                            {"text": "Cancelar compromisso", "value": "Cancelar compromisso"}
                        ]
                    }
                }
            ]
        }
    else:
        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "ElicitIntent"
                },
                "intent": {
                    "name": "FallbackIntent",
                    "state": "InProgress"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "Desculpe, não entendi a sua solicitação. Pode me dizer novamente ou fornecer mais detalhes?"
                },
                {
                    "contentType": "ImageResponseCard",
                    "imageResponseCard": {
                        "title": "Por favor, selecione uma opção:",
                        "buttons": [
                            {"text": "Agendar compromisso", "value": "Agendar compromisso"},
                            {"text": "Listar compromissos", "value": "Listar compromissos"},
                            {"text": "Editar compromisso", "value": "Editar compromisso"},
                            {"text": "Cancelar compromisso", "value": "Cancelar compromisso"}
                        ]
                    }
                }
            ]
        }

    logger.debug(f"Resposta do fallback: {response}")
    return response

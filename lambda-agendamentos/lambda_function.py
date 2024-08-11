import json
from intents.agendar_compromisso_intent import handle_agendar_compromisso_intent
from intents.listar_compromisso_intent import handle_listar_compromissos_intent
from intents.editar_compromisso_intent import handle_editar_compromisso_intent
from intents.cancelar_compromisso_intent import handle_cancelar_compromisso_intent

def lambda_handler(event, context):
    try:
        # Extrai a intenção do evento
        intent_name = event['sessionState']['intent']['name']
        
        # Mapeia a intenção para a função correspondente
        if intent_name == 'AgendarCompromissoIntent':
            response = handle_agendar_compromisso_intent(event)
        elif intent_name == 'ListarCompromissosIntent':
            response = handle_listar_compromissos_intent(event)
        elif intent_name == 'EditarCompromissoIntent':
            response = handle_editar_compromisso_intent(event)
        elif intent_name == 'CancelarCompromissoIntent':
            response = handle_cancelar_compromisso_intent(event)
        else:
            return handle_fallback_intent(event)
        
    except Exception as e:
        # Trata erros inesperados
        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": intent_name,
                    "state": "Failed"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "Desculpe, ocorreu um erro ao processar sua solicitação. Por favor, tente novamente mais tarde."
                }
            ]
        }
        print(f"Error: {e}")
    
    return response

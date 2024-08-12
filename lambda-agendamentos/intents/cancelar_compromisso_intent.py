import json
import boto3
import logging

# Inicializar cliente DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('agendamentos')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def query_compromisso_by_id(compromisso_id):
    try:
        response = table.get_item(Key={'id': compromisso_id})
        return response.get('Item', None)
    except Exception as e:
        logger.error(f"Erro ao consultar o compromisso: {e}")
        return None

def handle_cancelar_compromisso_intent(event):
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']

    if event['invocationSource'] == 'DialogCodeHook':
        compromissoId = slots.get('compromissoId', {}).get('value', {}).get('originalValue', '').strip()
        if compromissoId:
            compromisso = query_compromisso_by_id(compromissoId)
            if compromisso:
                return {
                    "sessionState": {
                        "dialogAction": {
                            "type": "Delegate"
                        },
                        "intent": {
                            "name": intent,
                            "slots": slots
                        }
                    }
                }
            else:
                return {
                    "sessionState": {
                        "dialogAction": {
                            "slotToElicit": 'compromissoId',
                            "type": "ElicitSlot"
                        },
                        "intent": {
                            "name": intent,
                            "slots": slots
                        }
                    },
                    "messages": [
                        {
                            "contentType": "PlainText",
                            "content": "O ID do compromisso fornecido não é válido. Por favor, forneça um ID de compromisso correto."
                        }
                    ]
                }
        else:
            return {
                "sessionState": {
                    "dialogAction": {
                        "slotToElicit": 'compromissoId',
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        "name": intent,
                        "slots": slots
                    }
                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": "Por favor, informe o ID do compromisso que você deseja cancelar."
                    }
                ]
            }

    elif event['invocationSource'] == 'FulfillmentCodeHook':
        compromissoId = slots.get('compromissoId', {}).get('value', {}).get('originalValue', '').strip()
        if compromissoId:
            compromisso = query_compromisso_by_id(compromissoId)
            if compromisso:
                try:
                    # Remover o compromisso do DynamoDB
                    table.delete_item(Key={'id': compromissoId})
                    
                    # Preparar a mensagem com os detalhes do compromisso cancelado
                    compromisso_data = compromisso.get('data', 'N/A')
                    compromisso_hora = compromisso.get('hora', 'N/A')
                    compromisso_local = compromisso.get('local', 'N/A')
                    compromisso_tipo = compromisso.get('tipoCompromisso', 'N/A')

                    return {
                        "sessionState": {
                            "dialogAction": {
                                "type": "Close",
                                "fulfillmentState": "Fulfilled"
                            },
                            "intent": {
                                "name": intent,
                                "slots": slots,
                                "state": "Fulfilled"
                            }
                        },
                        "messages": [
                            {
                                "contentType": "PlainText",
                                "content": (f"Seu compromisso com o ID {compromissoId} foi cancelado com sucesso. "
                                            f"Detalhes do compromisso: Data - {compromisso_data}, "
                                            f"Horário - {compromisso_hora}, Local - {compromisso_local}, "
                                            f"Tipo - {compromisso_tipo}.")
                            }
                        ]
                    }
                except Exception as e:
                    logger.error(f"Erro ao cancelar compromisso: {e}")
                    return {
                        "sessionState": {
                            "dialogAction": {
                                "type": "Close",
                                "fulfillmentState": "Failed"
                            },
                            "intent": {
                                "name": intent,
                                "slots": slots,
                                "state": "Failed"
                            }
                        },
                        "messages": [
                            {
                                "contentType": "PlainText",
                                "content": "Ocorreu um erro ao cancelar seu compromisso. Por favor, tente novamente mais tarde."
                            }
                        ]
                    }
            else:
                return {
                    "sessionState": {
                        "dialogAction": {
                            "type": "Close",
                            "fulfillmentState": "Failed"
                        },
                        "intent": {
                            "name": intent,
                            "slots": slots,
                            "state": "Failed"
                        }
                    },
                    "messages": [
                        {
                            "contentType": "PlainText",
                            "content": "O compromisso com o ID fornecido não foi encontrado. Não foi possível cancelar."
                        }
                    ]
                }


import json
import boto3
import logging

# Inicializar cliente DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('agendamentos')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def get_agendamento_by_id(compromisso_id):
    try:
        response = table.get_item(Key={'id': compromisso_id})
        return response.get('Item', None)
    except Exception as e:
        logger.error(f"Erro ao buscar compromisso por ID: {e}")
        return None

def handle_cancelar_compromisso_intent(event):
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']

    if event['invocationSource'] == 'DialogCodeHook':
        # Validar se o usuário forneceu um compromisso
        compromissoId = slots.get('compromissoId', {}).get('value', {}).get('originalValue', '').strip()
        if compromissoId:
            # Verificar se o ID do compromisso é válido
            compromisso = get_agendamento_by_id(compromissoId)
            if not compromisso:
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
                        "content": "Por favor, informe o ID do compromisso que você deseja cancelar."
                    }
                ]
            }

    elif event['invocationSource'] == 'FulfillmentCodeHook':
        compromissoId = slots.get('compromissoId', {}).get('value', {}).get('originalValue', '').strip()
        if compromissoId:
            try:
                # Buscar o compromisso antes de removê-lo
                compromisso = get_agendamento_by_id(compromissoId)
                
                if not compromisso:
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
                                "content": "Ocorreu um erro ao encontrar o compromisso. Por favor, tente novamente mais tarde."
                            }
                        ]
                    }

                # Remover o compromisso do DynamoDB
                table.delete_item(Key={'id': compromissoId})

                # Mensagem de resposta com todos os dados do compromisso cancelado
                response_message = (
                    f"Seu compromisso foi cancelado com sucesso.\n"
                    f"Tipo de Compromisso: {compromisso['tipoCompromisso']}"
                    f"Data: {compromisso['data']}\n"
                    f"Hora: {compromisso['hora']}\n"
                    f"local: {compromisso['local']}\n"
                )

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
                            "content": response_message
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
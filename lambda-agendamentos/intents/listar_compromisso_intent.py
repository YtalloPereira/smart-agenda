import json
import boto3
from datetime import datetime

# Inicializar cliente DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('agendamentos')

def query_todos_agendamentos():
    try:
        response = table.scan()
        return response.get('Items', [])
    except Exception as e:
        return []

def convert_date_to_datetime(date_str):
    """Converte uma string de data no formato DD/MM/AAAA para um objeto datetime.
       Retorna datetime.min para datas inválidas ou None."""
    if date_str:
        try:
            return datetime.strptime(date_str, '%d/%m/%Y')
        except ValueError:
            return datetime.min
    return datetime.min

def handle_listar_compromissos_intent(event):
    # Verificar se o evento possui o campo 'invocationSource' com valor esperado
    invocation_source = event.get('invocationSource', 'Unknown')
    if invocation_source in ['FulfillmentCodeHook', 'DialogCodeHook']:
        todos_agendamentos = query_todos_agendamentos()

        if todos_agendamentos:
            # Ordenar compromissos por data
            todos_agendamentos_sorted = sorted(
                todos_agendamentos,
                key=lambda comp: convert_date_to_datetime(comp.get('data', '01/01/0001'))
            )

            lista_compromissos = "\n".join([
                f"ID: {comp.get('id', 'N/A')}, Data: {comp.get('data', 'N/A')}, Hora: {comp.get('hora', 'N/A')}, Tipo: {comp.get('tipoCompromisso', 'N/A')}, Local: {comp.get('local', 'N/A')}"
                for comp in todos_agendamentos_sorted
            ])

            return {
                "sessionState": {
                    "dialogAction": {
                        "type": "Close",
                        "fulfillmentState": "Fulfilled"
                    },
                    "intent": {
                        "name": "ListarCompromissosIntent",
                        "state": "Fulfilled"
                    }
                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": f"Aqui está a lista dos seus compromissos:\n{lista_compromissos}"
                    }
                ]
            }
        else:
            return {
                "sessionState": {
                    "dialogAction": {
                        "type": "Close",
                        "fulfillmentState": "Fulfilled"
                    },
                    "intent": {
                        "name": "ListarCompromissosIntent",
                        "state": "Fulfilled"
                    }
                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": "Não há compromissos agendados no momento."
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
                    "name": "ListarCompromissosIntent",
                    "state": "Failed"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "Erro ao processar a solicitação de listagem de compromissos."
                }
            ]
        }

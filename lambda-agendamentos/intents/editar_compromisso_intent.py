import json
import boto3
from datetime import datetime
import urllib3

# Inicializar o cliente do DynamoDB e o gerenciador HTTP
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('agendamentos')
http = urllib3.PoolManager()

def validate_future_date(date_str):
    """Verifica se a data fornecida é futura."""
    try:
        date = datetime.strptime(date_str, '%d/%m/%Y').date()
        today = datetime.now().date()
        return date >= today
    except ValueError:
        return False

def validate_future_time(date_str, time_str):
    """Verifica se a data e a hora fornecidas são futuras."""
    try:
        date_time = datetime.strptime(f"{date_str} {time_str}", '%d/%m/%Y %H:%M')
        now = datetime.now()
        return date_time > now
    except ValueError:
        return False

def format_date(date_str):
    """Formata a data no formato necessário para o DynamoDB."""
    try:
        return datetime.strptime(date_str, '%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError:
        return date_str

def format_time(time_str):
    """Formata o horário no formato necessário (24 horas)."""
    try:
        return datetime.strptime(time_str, '%H:%M').strftime('%H:%M')
    except ValueError:
        return time_str

def generate_audio(message):
    """Gera o áudio da mensagem usando um serviço externo."""
    api_url = 'https://9xmnluesl2.execute-api.us-east-1.amazonaws.com/v1/tts'
    payload = json.dumps({'phrase': message})
    headers = {'Content-Type': 'application/json'}

    response = http.request('POST', api_url, body=payload, headers=headers)
    response_data = json.loads(response.data.decode('utf-8'))

    if response.status == 200:
        return response_data.get('url_to_audio')
    else:
        return None

def validate_compromisso_id(compromisso_id):
    """Valida se o ID do compromisso existe na tabela."""
    try:
        response = table.get_item(Key={'id': compromisso_id})
        return 'Item' in response
    except Exception as e:
        print(f"Erro ao validar ID do compromisso: {e}")
        return False

def handle_editar_compromisso_intent(event):
    """Manipula a intenção de edição de compromisso."""
    print("Evento recebido:", json.dumps(event, indent=4))  # Log do evento recebido

    if 'sessionState' not in event or 'intent' not in event['sessionState']:
        raise KeyError("Falta 'sessionState' ou 'intent' no evento")

    intent = event['sessionState']['intent']
    
    if 'slots' not in intent:
        raise KeyError("Falta 'slots' na intenção")

    slots = intent['slots']
    
    compromisso_id = slots.get('compromissoId', {}).get('value', {}).get('originalValue', '').strip() if slots.get('compromissoId') else ''
    nova_data = slots.get('data', {}).get('value', {}).get('originalValue', '').strip() if slots.get('data') else ''
    novo_hora = slots.get('horario', {}).get('value', {}).get('originalValue', '').strip() if slots.get('horario') else ''
    novo_tipo_compromisso = slots.get('tipoCompromisso', {}).get('value', {}).get('originalValue', '').strip() if slots.get('tipoCompromisso') else ''
    novo_local = slots.get('local', {}).get('value', {}).get('originalValue', '').strip() if slots.get('local') else 'não especificado'

    print(f"Compromisso ID: {compromisso_id}")
    print(f"Nova data: {nova_data}")
    print(f"Novo horário: {novo_hora}")
    print(f"Novo tipo de compromisso: {novo_tipo_compromisso}")
    print(f"Novo local: {novo_local}")

    if not compromisso_id:
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": "EditarCompromissoIntent",
                    "state": "Failed"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "Por favor, forneça um ID válido do compromisso para alterar."
                }
            ]
        }

    if not validate_compromisso_id(compromisso_id):
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": "EditarCompromissoIntent",
                    "state": "Failed"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "O ID do compromisso fornecido não é válido. Verifique o ID e tente novamente."
                }
            ]
        }

    if nova_data and not validate_future_date(nova_data):
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": "EditarCompromissoIntent",
                    "state": "Failed"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "A data fornecida deve ser uma data futura. Por favor, informe uma data válida."
                }
            ]
        }

    if novo_hora and nova_data and not validate_future_time(nova_data, novo_hora):
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": "EditarCompromissoIntent",
                    "state": "Failed"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "A hora fornecida deve ser uma hora futura. Por favor, informe um horário válido."
                }
            ]
        }

    nova_data_formatada = format_date(nova_data)
    novo_hora_formatado = format_time(novo_hora)

    try:
        response = table.update_item(
            Key={'id': compromisso_id},
            UpdateExpression="SET compromissoData = :d, compromissoHora = :h, tipoCompromisso = :t, local = :l",
            ExpressionAttributeValues={
                ':d': nova_data_formatada,
                ':h': novo_hora_formatado,
                ':t': novo_tipo_compromisso,
                ':l': novo_local
            },
            ReturnValues="UPDATED_NEW"
        )

        if response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200:
            audio_message = f"Seu compromisso foi alterado com sucesso para a data {nova_data_formatada} às {novo_hora_formatado} horas e para o tipo {novo_tipo_compromisso}."
            audio_url = generate_audio(audio_message)

            response_message = f"Compromisso alterado com sucesso para {nova_data_formatada} às {novo_hora_formatado} horas e tipo {novo_tipo_compromisso}."
            if audio_url:
                response_message += f" Aqui está o áudio do seu compromisso: {audio_url}"

            return {
                "sessionState": {
                    "dialogAction": {
                        "type": "Close"
                    },
                    "intent": {
                        "name": "EditarCompromissoIntent",
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
        else:
            return {
                "sessionState": {
                    "dialogAction": {
                        "type": "Close"
                    },
                    "intent": {
                        "name": "EditarCompromissoIntent",
                        "state": "Failed"
                    }
                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": "Não foi possível alterar o compromisso. Por favor, tente novamente mais tarde."
                    }
                ]
            }
    except Exception as e:
        print(f"Erro: {e}")
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": "EditarCompromissoIntent",
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

def lambda_handler(event, context):
    """Função principal do Lambda para tratar o evento."""
    intent_name = event['sessionState']['intent']['name']

    if intent_name == 'EditarCompromissoIntent':
        return handle_editar_compromisso_intent(event)
    else:
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "Intent não reconhecida. Por favor, tente novamente."
                }
            ]
        }

import json
import boto3
from datetime import datetime
import urllib3

# Inicializar clientes DynamoDB e HTTP
http = urllib3.PoolManager()
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('agendamentos')

# Função para validar se o compromisso existe na tabela DynamoDB
def validate_compromisso_id(compromisso_id):
    response = table.get_item(Key={'id': compromisso_id})
    return 'Item' in response

# Função para formatar a data no formato necessário para o DynamoDB
def format_date(date_str):
    try:
        return datetime.strptime(date_str, '%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError:
        return date_str

# Função para formatar o horário no formato necessário (24 horas)
def format_time(time_str):
    try:
        return datetime.strptime(time_str, '%H:%M').strftime('%H:%M')
    except ValueError:
        return time_str

# Função para gerar áudio a partir de uma mensagem usando um serviço externo
def generate_audio(message):
    api_url = 'https://9xmnluesl2.execute-api.us-east-1.amazonaws.com/v1/tts'
    payload = json.dumps({'phrase': message})
    headers = {'Content-Type': 'application/json'}

    try:
        response = http.request('POST', api_url, body=payload, headers=headers)
        response_data = json.loads(response.data.decode('utf-8'))

        if response.status == 200:
            return response_data.get('url_to_audio')
        else:
            return None
    except Exception as e:
        print(f"Erro ao gerar áudio: {e}")
        return None

# Função para validar os slots e retornar a resposta apropriada
def validate_slots(slots):
    compromisso_id = slots.get('idCompromisso', {}).get('value', {}).get('originalValue', '').strip()
    nova_data = slots.get('data', {}).get('value', {}).get('originalValue', '').strip()
    novo_hora = slots.get('horario', {}).get('value', {}).get('originalValue', '').strip()
    novo_tipo_compromisso = slots.get('tipoCompromisso', {}).get('value', {}).get('originalValue', '').strip()
    novo_local = slots.get('local', {}).get('value', {}).get('originalValue', '').strip()

    # Verificar se o ID do compromisso é válido
    if not compromisso_id or not validate_compromisso_id(compromisso_id):
        return {
            'isValid': False,
            'invalidSlot': 'idCompromisso',
            'message': 'Por favor, forneça um ID válido do compromisso para alterar.'
        }

    # Verificar a validade da nova data
    if nova_data:
        try:
            datetime.strptime(nova_data, '%d/%m/%Y')  # Testar se a data está no formato correto
        except ValueError:
            return {
                'isValid': False,
                'invalidSlot': 'data',
                'message': 'A data fornecida está em um formato inválido. Por favor, informe uma data no formato DD/MM/AAAA.'
            }

    # Verificar a validade do novo horário
    if novo_hora:
        try:
            datetime.strptime(novo_hora, '%H:%M')  # Testar se o horário está no formato correto
        except ValueError:
            return {
                'isValid': False,
                'invalidSlot': 'horario',
                'message': 'O horário fornecido está em um formato inválido. Por favor, informe o horário no formato HH:MM.'
            }

    return {'isValid': True}

# Função principal para lidar com a intenção de editar compromisso
def handle_editar_compromisso_intent(event):
    if event['invocationSource'] == 'DialogCodeHook':
        # Validar slots
        edit_validation_result = validate_slots(event['sessionState']['intent']['slots'])

        if not edit_validation_result['isValid']:
            response_message = edit_validation_result.get('message', '')
            return {
                "sessionState": {
                    "dialogAction": {
                        "slotToElicit": edit_validation_result.get('invalidSlot', ''),
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        "name": "EditarCompromissoIntent",
                        "slots": event['sessionState']['intent']['slots']
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
                        "type": "Delegate"
                    },
                    "intent": {
                        "name": "EditarCompromissoIntent",
                        "slots": event['sessionState']['intent']['slots']
                    }
                }
            }

    elif event['invocationSource'] == 'FulfillmentCodeHook':
        slots = event['sessionState']['intent']['slots']
        compromisso_id = slots.get('idCompromisso', {}).get('value', {}).get('originalValue', '').strip()
        nova_data = slots.get('data', {}).get('value', {}).get('originalValue', '').strip()
        novo_hora = slots.get('horario', {}).get('value', {}).get('originalValue', '').strip()
        novo_tipo_compromisso = slots.get('tipoCompromisso', {}).get('value', {}).get('originalValue', '').strip()
        novo_local = slots.get('local', {}).get('value', {}).get('originalValue', '').strip()

        nova_data_formatada = format_date(nova_data)
        novo_hora_formatado = format_time(novo_hora)

        try:
            response = table.update_item(
                Key={'id': compromisso_id},
                UpdateExpression="SET compromissoData = :d, compromissoHora = :h, tipoCompromisso = :t, #loc = :l",
                ExpressionAttributeNames={
                    '#loc': 'local'
                },
                ExpressionAttributeValues={
                    ':d': nova_data_formatada,
                    ':h': novo_hora_formatado,
                    ':t': novo_tipo_compromisso,
                    ':l': novo_local
                },
                ReturnValues="UPDATED_NEW"
            )

            if response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200:
                audio_message = (
                    f"Seu compromisso foi alterado com sucesso para a data {nova_data_formatada} "
                    f"às {novo_hora_formatado} horas, para o tipo {novo_tipo_compromisso} e no local {novo_local}."
                )
                audio_url = generate_audio(audio_message)

                response_message = f"Compromisso alterado com sucesso para {nova_data_formatada} às {novo_hora_formatado} horas, tipo {novo_tipo_compromisso} e local {novo_local}."
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
                        "content": "Desculpe, ocorreu um erro ao tentar alterar o compromisso. Por favor, tente novamente mais tarde."
                    }
                ]
            }

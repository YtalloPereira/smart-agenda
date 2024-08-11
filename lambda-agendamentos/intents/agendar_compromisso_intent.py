import json
import boto3
import uuid
from datetime import datetime, timedelta
import urllib3

# Inicializar clientes DynamoDB
http = urllib3.PoolManager()
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('agendamentos')

# Função para converter horário para o formato de 24 horas
def convert_to_24_hour_format(time_str):
    if not time_str:
        return None
    
    time_str = time_str.lower().strip()
    try:
        if 'am' in time_str:
            time_str = time_str.replace('am', '').strip()
            return datetime.strptime(time_str, '%I:%M').strftime('%H:%M')
        elif 'pm' in time_str:
            time_str = time_str.replace('pm', '').strip()
            return (datetime.strptime(time_str, '%I:%M') + timedelta(hours=12)).strftime('%H:%M')
        else:
            return datetime.strptime(time_str, '%H:%M').strftime('%H:%M')
    except ValueError:
        return None

# Função para converter a data para o formato brasileiro
def convert_date_to_brazilian_format(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').strftime('%d/%m/%Y')
    except ValueError:
        return None

# Função para gerar um ID único para o compromisso
def generate_id(data, hora, tipoCompromisso, local):
    return str(uuid.uuid4())

# Função para salvar o compromisso no DynamoDB
def save_compromisso_to_dynamodb(compromisso):
    table.put_item(Item=compromisso)

# Função para gerar áudio a partir de uma mensagem
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

# Função para validar a data futura
def validate_future_date(date_str):
    try:
        for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y'):
            try:
                date = datetime.strptime(date_str, fmt).date()
                today = datetime.now().date()
                return date >= today  # Permitir hoje também
            except ValueError:
                continue
        return False
    except Exception as e:
        print(f"Erro na validação da data: {e}")
        return False

# Função para validar a hora futura
def validate_future_time(date_str, time_str):
    try:
        # Cria um objeto datetime para a data e hora fornecida
        date_time = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')
        now = datetime.now()

        # Verifica se a data é futura ou se é a data de hoje, mas a hora deve ser futura
        if date_time.date() > now.date():
            return True
        elif date_time.date() == now.date():
            return date_time >= now
        return False
    except ValueError:
        return False

# Função para validar os slots e retornar a resposta apropriada
def validate_slots(slots):
    tipoCompromisso = slots.get('tipoCompromisso', {}).get('value', {}).get('originalValue', '').strip() if slots.get('tipoCompromisso') else ''
    data = slots.get('data', {}).get('value', {}).get('originalValue', '').strip() if slots.get('data') else ''
    hora = slots.get('horario', {}).get('value', {}).get('originalValue', '').strip() if slots.get('horario') else ''

    # Verificar a validade da data assim que fornecida
    if data and not validate_future_date(data):
        return {
            'isValid': False,
            'invalidSlot': 'data',
            'message': 'A data fornecida deve ser uma data futura. Por favor, informe uma data válida.'
        }

    # Verificar se a hora é futura, se a data e a hora foram fornecidas
    if hora and data:
        hora_formatada = convert_to_24_hour_format(hora)
        if hora_formatada and not validate_future_time(data, hora_formatada):
            return {
                'isValid': False,
                'invalidSlot': 'horario',
                'message': 'A hora fornecida deve ser uma hora futura. Por favor, informe um horário válido.'
            }

    return {'isValid': True}

# Função principal para lidar com a intent de agendar compromisso
def handle_agendar_compromisso_intent(event):
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']

    if event['invocationSource'] == 'DialogCodeHook':
        # Validar slots
        agendamento_validation_result = validate_slots(slots)

        if not agendamento_validation_result['isValid']:
            response_message = agendamento_validation_result.get('message', '')
            return {
                "sessionState": {
                    "dialogAction": {
                        "slotToElicit": agendamento_validation_result.get('invalidSlot', ''),
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
                        "content": response_message
                    }
                ]
            }
        else:
            # Caso todos os slots estejam preenchidos corretamente
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

    elif event['invocationSource'] == 'FulfillmentCodeHook':
        data = slots['data']['value']['interpretedValue']
        hora = slots['horario']['value']['interpretedValue']
        tipoCompromisso = slots['tipoCompromisso']['value']['originalValue'].strip().lower()
        local = slots.get('local', {}).get('value', {}).get('originalValue', 'não especificado')

        if data.lower() == 'amanha':
            data = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

        hora = convert_to_24_hour_format(hora)
        data_brazilian_format = convert_date_to_brazilian_format(data)

        id = generate_id(data_brazilian_format, hora, tipoCompromisso, local)

        compromisso = {
            'id': id,
            'data': data_brazilian_format,
            'hora': hora,
            'tipoCompromisso': tipoCompromisso,
            'local': local
        }

        save_compromisso_to_dynamodb(compromisso)

        audio_message = (
            f"Seu compromisso de {tipoCompromisso} foi agendado com sucesso para "
            f"{data_brazilian_format} às {hora} horas no local {local}."
        )
        audio_url = generate_audio(audio_message)

        response = {
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
                    "content": audio_message
                }
            ]
        }

        if audio_url:
            response['messages'].append({
                "contentType": "PlainText",
                "content": f"Aqui está o áudio do seu compromisso: {audio_url}"
            })
        else:
            response['messages'].append({
                "contentType": "PlainText",
                "content": "O áudio não pôde ser gerado. No entanto, seu compromisso foi agendado com sucesso."
            })

        return response


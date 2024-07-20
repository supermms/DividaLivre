import boto3
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from botocore.exceptions import ClientError

# Load .env file
load_dotenv("./.env")

# Configurar o cliente DynamoDB
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name='sa-east-1'
)

# Referenciar a tabela
leads_table = dynamodb.Table('SerasaLivre_NovosClientes')


def verificar_lead_existente(telefone):
    """verifica se um item já existe na tabela de novos clientes"""
    response = leads_table.get_item(
        Key={'telefone': telefone}
    )
    return 'Item' in response


# Adicionar um novo lead com atributos adicionais
def adicionar_novo_lead(nome, telefone, cnpj=None):
    """insere um novo item na tabela de novos clientes"""
    if verificar_lead_existente(telefone):
        print(f"Lead com telefone {telefone} já existe.")
        return None
         
    data_criacao = datetime.now(timezone.utc).isoformat()
    if cnpj !=None:
        novo_lead = {
            "telefone": telefone,
            "data_criacao": data_criacao,
            "nome": nome,
            "lead_status": "novo",
            "CNPJ": cnpj
        }
    else:
        novo_lead = {
            "telefone": telefone,
            "data_criacao": data_criacao,
            "nome": nome,
            "lead_status": "novo"
        }

    try:
        leads_table.put_item(Item=novo_lead)
        print(f"Lead adicionado: {novo_lead}")
        return None
    except ClientError as e:
        print(f"Erro ao adicionar lead: {e}")
    return novo_lead

def get_new_leads():
    try:
        response = leads_table.scan(
            FilterExpression="lead_status = :lead_status",
            ExpressionAttributeValues={":lead_status": "novo"}
        )
        items = response.get('Items', [])
        return items
    except ClientError as e:
        print(f"Erro ao obter leads: {e}")
        return []


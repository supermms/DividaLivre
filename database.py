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
    region_name='us-east-1'
)

# Referenciar as tabelas
leads_table = dynamodb.Table('DividaLivre_NovosClientes')



def verificar_lead_existente(telefone):
    """verifica se um item já existe na tabela de novos clientes"""
    response = leads_table.get_item(
        Key={'telefone': telefone}
    )
    return 'Item' in response


# Adicionar um novo lead com atributos adicionais
def adicionar_novo_lead(nome, telefone, cnpj=None, lead_status='novo'):
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
            "lead_status": lead_status,
            "CNPJ": cnpj
        }
    else:
        novo_lead = {
            "telefone": telefone,
            "data_criacao": data_criacao,
            "nome": nome,
            "lead_status": lead_status
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

def get_all_leads():
    try:
        response = leads_table.scan()
        items = response.get('Items', [])

        # Verificar se há mais páginas de resultados
        while 'LastEvaluatedKey' in response:
            response = leads_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response.get('Items', []))

        return items
    except ClientError as e:
        print(f"Erro ao obter leads: {e}")
        return []


def check_lead_status(phone):
    try:
        # Buscar o item com base na chave primária (telefone)
        response = leads_table.get_item(Key={'telefone': phone})
        
        # Verificar se o item existe na tabela
        if 'Item' in response:
            return response['Item'].get('lead_status', None)
        else:
            print(f"Nenhum lead encontrado com o telefone {telefone}.")
            return None
    except ClientError as e:
        print(f"Erro ao buscar o lead: {e.response['Error']['Message']}")
        return None


def update_lead_status(phone, lead_status):
    try:
        response = leads_table.update_item(Key={'telefone':phone},
        UpdateExpression="SET lead_status = :new_status", 
        ExpressionAttributeValues={
            ':new_status':lead_status
            },
        ReturnValues="UPDATED_NEW"
        )
        return response
    except ClientError as e:
        print(f"Erro ao atualizar o status do lead: {e.response['Error']['Message']}")
        return None
    



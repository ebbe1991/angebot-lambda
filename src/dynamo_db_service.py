import os
import boto3
from angebot_dto import AngebotDTO
from boto3.dynamodb.conditions import Key


def get_angebote_table():
    dynamodb = boto3.resource('dynamodb')
    table_name = os.getenv('ANGEBOT_TABLE_NAME')
    return dynamodb.Table(table_name)


def put_angebot(tenant_id: str, angebot: AngebotDTO):
    table = get_angebote_table()
    table.put_item(
        Item={
            'tenant-id': tenant_id,
            'id': angebot.id,
            'bezeichnung': angebot.bezeichnung,
            'preisInEuro': str(angebot.preisInEuro),
            'gueltigVon': angebot.gueltigVon.isoformat() if angebot.gueltigVon is not None else None,
            'gueltigBis': angebot.gueltigBis.isoformat() if angebot.gueltigBis is not None else None,
            'ttl': angebot.ttl
        }
    )


def get_angebot(tenant_id: str, id: str):
    table = get_angebote_table()
    result = table.get_item(
        Key={
            "tenant-id": tenant_id,
            "id": id
        }
    )
    return result.get('Item')


def get_angebote(tenant_id: str) -> list:
    table = get_angebote_table()
    response = table.query(
        KeyConditionExpression=Key('tenant-id').eq(tenant_id)
    )
    return response['Items']

def delete_angebot(tenant_id: str, id: str):
    table = get_angebote_table()
    table.delete_item(
        Key={
            "tenant-id": tenant_id,
            "id": id
        }
    )

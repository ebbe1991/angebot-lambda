import json
from src import angebot_controller

from src import angebot_handler
from tests.helper import event, lambda_response, DEFAULT_TENANT_ID


def test_delete_angebot_ok(lambda_context, dynamodb_table):
    item = {
        'bezeichnung': "Testangebot",
        "preisInEuro": "5.21",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    createdAngebot = angebot_controller.create_angebot(
        DEFAULT_TENANT_ID, item)

    angebote = angebot_controller.get_angebote(DEFAULT_TENANT_ID)
    assert len(angebote) == 1

    pathParameters = {
        "id": createdAngebot.id
    }
    response = angebot_handler.handle(event(
        '/api/angebot/{id}', 'DELETE', None, pathParameters), lambda_context)
    
    assert response == lambda_response(204)
    angebote = angebot_controller.get_angebote(DEFAULT_TENANT_ID)
    assert len(angebote) == 0


def test_delete_angebot_not_ok(lambda_context, dynamodb_table):
    pathParameters = {
        "id": "abc123"
    }
    response = angebot_handler.handle(event(
        '/api/angebot/{id}', 'DELETE', None, pathParameters), lambda_context)
   
    assert response == lambda_response(404)


def test_delete_angebot_without_tenant_id_not_ok(lambda_context, dynamodb_table):
    pathParameters = {
        "id": "abc123"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = angebot_handler.handle(event(
        '/api/angebot/{id}', 'DELETE', None, pathParameters, headers), lambda_context)
    
    assert response == lambda_response(400, json.dumps(
        {'error_text': 'tenant not present.'}))

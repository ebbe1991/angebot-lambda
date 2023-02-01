import json
from src import angebot_controller

from src import angebot_handler
from tests.helper import event, lambda_response, DEFAULT_TENANT_ID


def test_get_angebot_not_found(lambda_context, dynamodb_table):
    pathParameters = {
        "id": "unknown_id"
    }
    response = angebot_handler.handle(event(
        '/api/angebot/{id}', 'GET', None, pathParameters), lambda_context)

    assert response == lambda_response(404)


def test_get_angebot_ok(lambda_context, dynamodb_table):
    item = {
        'bezeichnung': "Testangebot",
        "preisInEuro": "5.21",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    createdAngebot = angebot_controller.create_angebot(
        DEFAULT_TENANT_ID, item)

    pathParameters = {
        "id": createdAngebot.id
    }
    response = angebot_handler.handle(event(
        '/api/angebot/{id}', 'GET', None, pathParameters), lambda_context)

    assert response == lambda_response(200, createdAngebot.to_json())

def test_get_angebot_without_tenant_id_not_ok(lambda_context, dynamodb_table):
    headers = {
        'Content-Type': 'application/json'
    }
    item = {
        'bezeichnung': "Testangebot",
        "preisInEuro": "5.21",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    createdAngebot = angebot_controller.create_angebot(
        DEFAULT_TENANT_ID, item)

    pathParameters = {
        "id": createdAngebot.id
    }
    response = angebot_handler.handle(event(
        '/api/angebot/{id}', 'GET', None, pathParameters, headers), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'tenant not present.'}))

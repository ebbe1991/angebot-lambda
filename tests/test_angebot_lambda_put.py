import json
from datetime import date
from src import angebot_controller

from src import angebot_handler
from src.angebot_dto import AngebotDTO
from tests.helper import event, lambda_response, DEFAULT_TENANT_ID


def test_update_angebot_ok(lambda_context, dynamodb_table):
    item = {
        'bezeichnung': "Testangebot",
        "preisInEuro": "5.21",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    createdAngebot = angebot_controller.create_angebot(
        DEFAULT_TENANT_ID, item
    )

    pathParameters = {
        "id": createdAngebot.id
    }
    itemUpdate = {
        'bezeichnung': "Testangebot",
        "preisInEuro": "9.9",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    response = angebot_handler.handle(event(
        '/api/angebot/{id}', 'PUT', json.dumps(itemUpdate), pathParameters), lambda_context)

    assert response == lambda_response(200, AngebotDTO(
        "Testangebot", 9.9, date.fromisoformat("2022-01-01"), date.fromisoformat("2022-02-01"), createdAngebot.id).to_json())


def test_update_angebot_required_field_to_null_not_ok(lambda_context, dynamodb_table):
    item = {
        'bezeichnung': "Testangebot",
        "preisInEuro": "5.21",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    createdAngebot = angebot_controller.create_angebot(
        DEFAULT_TENANT_ID, item
    )

    pathParameters = {
        "id": createdAngebot.id
    }
    itemUpdate = {
        'bezeichnung': "",
        "preisInEuro": "5.21",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    response = angebot_handler.handle(event(
        '/api/angebot/{id}', 'PUT', json.dumps(itemUpdate), pathParameters), lambda_context)

    assert response == lambda_response(
        400, json.dumps({'error_text': "'bezeichnung' not present."}))


def test_update_angebot_with_unknown_id_not_ok(lambda_context, dynamodb_table):
    pathParameters = {
        "id": 'unknown'
    }
    itemUpdate = {
        'bezeichnung': "Testangebot",
        "preisInEuro": "5.21",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    response = angebot_handler.handle(event(
        '/api/angebot/{id}', 'PUT', json.dumps(itemUpdate), pathParameters), lambda_context)

    assert response == lambda_response(
        400, json.dumps({'error_text': "unknown id 'unknown' (tenant='mytenant1')."}))


def test_update_angebot_set_null_value(lambda_context, dynamodb_table):
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

    itemUpdate = {
        'bezeichnung': "Testangebot",
        "preisInEuro": "5.21",
        "gueltigVon": "2022-01-01"
    }
    response = angebot_handler.handle(event(
        '/api/angebot/{id}', 'PUT', json.dumps(itemUpdate), pathParameters), lambda_context)

    assert response == lambda_response(200, AngebotDTO(
        "Testangebot", 5.21, date.fromisoformat("2022-01-01"), None, createdAngebot.id).to_json())


def test_update_angebot_without_body_not_ok(lambda_context, dynamodb_table):
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

    response = angebot_handler.handle(
        event('/api/angebot/{id}', 'PUT', None, pathParameters), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'body not present.'}))


def test_update_angebot_without_id_not_ok(lambda_context, dynamodb_table):
    item = {
        'bezeichnung': "Testangebot",
        "preisInEuro": "5.21",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    angebot_controller.create_angebot(
        DEFAULT_TENANT_ID, item)

    pathParameters = {
        "id": ''
    }

    response = angebot_handler.handle(
        event('/api/angebot/{id}', 'PUT', json.dumps(item), pathParameters), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'id not present.'}))


def test_update_angebot_without_tenant_id_not_ok(lambda_context, dynamodb_table):
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
    itemUpdate = {
        'bezeichnung': "Testangebot",
        "preisInEuro": "5.99",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    response = angebot_handler.handle(event(
        '/api/angebot/{id}', 'PUT', json.dumps(itemUpdate), pathParameters, headers), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'tenant not present.'}))

import json
from datetime import date
from src import angebot_handler
from src.angebot_dto import AngebotDTO
from tests.helper import event, lambda_response, extract_id


def test_create_angebot_ok(lambda_context, dynamodb_table):
    item = {
        'bezeichnung': "Testangebot",
        "preisInEuro": "5.21",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    response = angebot_handler.handle(
        event('/api/angebot', 'POST', json.dumps(item)), lambda_context)

    id = extract_id(response)

    assert id is not None
    assert response == lambda_response(201, AngebotDTO(
        "Testangebot", 5.21, date.fromisoformat("2022-01-01"), date.fromisoformat("2022-02-01"), id).to_json())

def test_create_angebot_ok_with_float_value(lambda_context, dynamodb_table):
    item = {
        'bezeichnung': "Testangebot",
        "preisInEuro": 5.21,
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    response = angebot_handler.handle(
        event('/api/angebot', 'POST', json.dumps(item)), lambda_context)

    id = extract_id(response)

    assert id is not None
    assert response == lambda_response(201, AngebotDTO(
        "Testangebot", 5.21, date.fromisoformat("2022-01-01"), date.fromisoformat("2022-02-01"), id).to_json())


def test_create_angebot_invalid_dateformat_bad_request(lambda_context, dynamodb_table):
    item = {
        'bezeichnung': "Testangebot",
        "preisInEuro": "9",
        "gueltigVon": "2022.01-01",
        "gueltigBis": "2022-02-01"
    }
    response = angebot_handler.handle(
        event('/api/angebot', 'POST', json.dumps(item)), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': "Invalid isoformat string: '2022.01-01'"}))


def test_create_angebot_missing_field_bezeichnung_bad_request(lambda_context, dynamodb_table):
    item = {
        "preisInEuro": "5.21",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    response = angebot_handler.handle(
        event('/api/angebot', 'POST', json.dumps(item)), lambda_context)

    assert response == lambda_response(
        400, json.dumps({'error_text': "'bezeichnung' not present."}))


def test_create_angebot_missing_field_preisInEuro_bad_request(lambda_context, dynamodb_table):
    item = {
        'bezeichnung': "Testangebot",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    response = angebot_handler.handle(
        event('/api/angebot', 'POST', json.dumps(item)), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': "'preisInEuro' not present."}))


def test_create_angebot_without_optional_parameters_ok(lambda_context, dynamodb_table):
    item = {
        'bezeichnung': "Testangebot",
        "preisInEuro": "5.21"
    }
    response = angebot_handler.handle(
        event('/api/angebot', 'POST', json.dumps(item)), lambda_context)
    id = extract_id(response)

    assert id is not None
    assert response == lambda_response(201, AngebotDTO(
        "Testangebot", 5.21, None, None, id).to_json())



def test_create_angebot_without_body_not_ok(lambda_context, dynamodb_table):
    response = angebot_handler.handle(
        event('/api/angebot', 'POST'), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'body not present.'}))

def test_create_angebot_without_tenant_id_not_ok(lambda_context, dynamodb_table):
    headers = {
        'Content-Type': 'application/json'
    }
    item = {
        'bezeichnung': "Testangebot",
        "preisInEuro": "5.21",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    response = angebot_handler.handle(
        event('/api/angebot', 'POST', json.dumps(item), None, headers), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'tenant not present.'}))

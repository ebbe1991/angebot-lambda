import json
from src import angebot_controller
from src import angebot_handler
from tests.helper import event, extract_body, extract_status_code, lambda_response, DEFAULT_TENANT_ID


def test_get_angebote_ok(lambda_context, dynamodb_table):
    item1 = {
        'bezeichnung': "Testangebot",
        "preis": "5.21",
        "preisEinheit": "€/Stück",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    item2 = {
        'bezeichnung': "Testangebot 2",
        "preis": "9",
        "preisEinheit": "€/Stück",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    angebot_controller.create_angebot(DEFAULT_TENANT_ID, item1)
    angebot_controller.create_angebot(DEFAULT_TENANT_ID, item2)

    response = angebot_handler.handle(
        event('/api/angebot', 'GET'), lambda_context)
    body = extract_body(response)

    assert extract_status_code(response) == 200
    assert len(body) == 2


def test_get_angebote_by_stichtag_ok(lambda_context, dynamodb_table):
    item1 = {
        'bezeichnung': "Testangebot",
        "preis": "5.21",
        "preisEinheit": "€/Stück",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    item2 = {
        'bezeichnung': "Testangebot 2",
        "preis": "9",
        "preisEinheit": "€/Stück",
        "gueltigVon": "2023-01-01",
        "gueltigBis": "2023-02-01"
    }
    angebot_controller.create_angebot(DEFAULT_TENANT_ID, item1)
    item2023 = angebot_controller.create_angebot(DEFAULT_TENANT_ID, item2)

    response = angebot_handler.handle(
        event('/api/angebot', 'GET', queryParameters={"stichtag": "2023-01-27"}), lambda_context)
    body = extract_body(response)

    assert extract_status_code(response) == 200
    assert len(body) == 1
    assert json.dumps(body[0]) == item2023.to_json()


def test_get_angebote_by_stichtag_with_angebot_in_future_ok(lambda_context, dynamodb_table):
    item1 = {
        'bezeichnung': "Testangebot",
        "preis": "5.21",
        "preisEinheit": "€/Stück",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    item2 = {
        'bezeichnung': "Testangebot 2",
        "preis": "9",
        "preisEinheit": "€/Stück",
        "gueltigVon": "2023-01-01",
        "gueltigBis": "2023-02-01"
    }
    item3 = {
        'bezeichnung': "Testangebot 3",
        "preis": "9",
        "preisEinheit": "€/Stück",
        "gueltigVon": "2024-01-01",
        "gueltigBis": "2024-02-01"
    }
    angebot_controller.create_angebot(DEFAULT_TENANT_ID, item1)
    angebot_controller.create_angebot(DEFAULT_TENANT_ID, item2)
    angebot_controller.create_angebot(DEFAULT_TENANT_ID, item3)

    response = angebot_handler.handle(
        event('/api/angebot', 'GET', queryParameters={"stichtag": "2023-01-27"}), lambda_context)
    body = extract_body(response)

    assert extract_status_code(response) == 200
    assert len(body) == 2


def test_get_angebote_by_stichtag_with_angebot_without_gueltigkeit_ok(lambda_context, dynamodb_table):
    item1 = {
        'bezeichnung': "Testangebot",
        "preis": "5.21",
        "preisEinheit": "€/Stück",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    item2 = {
        'bezeichnung': "Testangebot 2",
        "preis": "9",
        "preisEinheit": "€/Stück",
        "gueltigVon": "2023-01-01",
        "gueltigBis": "2023-02-01"
    }
    item3 = {
        'bezeichnung': "Testangebot 3",
        "preis": "9",
        "preisEinheit": "€/Stück"
    }
    angebot_controller.create_angebot(DEFAULT_TENANT_ID, item1)
    angebot_controller.create_angebot(DEFAULT_TENANT_ID, item2)
    angebot_controller.create_angebot(DEFAULT_TENANT_ID, item3)

    response = angebot_handler.handle(
        event('/api/angebot', 'GET', queryParameters={"stichtag": "2023-01-27"}), lambda_context)
    body = extract_body(response)

    assert extract_status_code(response) == 200
    assert len(body) == 2


def test_get_angebote_empty_ok(lambda_context, dynamodb_table):
    response = angebot_handler.handle(
        event('/api/angebot', 'GET'), lambda_context)
    body = extract_body(response)

    assert extract_status_code(response) == 200
    assert len(body) == 0


def test_get_angebote_without_tenant_id_not_ok(lambda_context, dynamodb_table):
    headers = {
        'Content-Type': 'application/json'
    }
    response = angebot_handler.handle(
        event('/api/angebot', 'GET', None, None, headers), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'tenant not present.'}))

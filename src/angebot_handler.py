from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
import angebot_controller
from angebot_controller import AngebotDTO
from lambda_utils.response_utils import response, empty_response
from lambda_utils.event_utils import extract_body, extract_id, extract_tenant
from lambda_utils.exception import ValidationException
import json
app = APIGatewayHttpResolver()


def handle(event: dict, context: dict):
    return app.resolve(event, context)


@app.post('/api/angebot')
def post():
    event = app.current_event
    tenant_id = extract_tenant(event)
    body = extract_body(event)
    angebot = angebot_controller.create_angebot(tenant_id, body)
    return response(201, angebot.to_json())


@app.put('/api/angebot/{id}')
def put():
    event = app.current_event
    tenant_id = extract_tenant(event)
    id = extract_id(event)
    body = extract_body(event)
    angebot = angebot_controller.update_angebot(tenant_id, id, body)
    return response(200, angebot.to_json())


@app.get('/api/angebot/{id}')
def get():
    event = app.current_event
    tenant_id = extract_tenant(event)
    id = extract_id(event)
    angebot = angebot_controller.get_angebot(tenant_id, id)
    if angebot:
        return response(200, angebot.to_json())
    else:
        return empty_response(404)


@app.get('/api/angebot')
def getAll():
    event = app.current_event
    tenant_id = extract_tenant(event)
    angebote = angebot_controller.get_angebote(tenant_id)
    return response(200, json.dumps(angebote, default=AngebotDTO.to_json))


@app.delete('/api/angebot/{id}')
def delete():
    event = app.current_event
    tenant_id = extract_tenant(event)
    id = extract_id(event)
    deleted = angebot_controller.delete_angebot(tenant_id, id)
    if deleted:
        return empty_response(204)
    else:
        return empty_response(404)


@app.exception_handler(ValidationException)
def handle_http_exception(exception: ValidationException):
    return response(exception.http_status, exception.to_json())
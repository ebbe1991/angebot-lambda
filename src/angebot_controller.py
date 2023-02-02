from angebot_dto import AngebotDTO, create
from lambda_utils.exception import UnknownIdException
from datetime import date
import dynamo_db_service


def create_angebot(tenant_id: str, dto: dict) -> AngebotDTO:
    angebot = create(dto)
    dynamo_db_service.put_angebot(tenant_id, angebot)
    return angebot


def update_angebot(tenant_id: str, id: str, dto: dict) -> AngebotDTO:
    dto.update({'id': id})
    angebot = create(dto)
    to_update = get_angebot(tenant_id, id)
    if to_update:
        dynamo_db_service.put_angebot(tenant_id, angebot)
        return angebot
    else:
        raise UnknownIdException(id, tenant_id)


def get_angebot(tenant_id: str, id: str) -> AngebotDTO:
    item = dynamo_db_service.get_angebot(tenant_id, id)
    if item:
        angebot = create(item)
        return angebot
    else:
        return None


def get_angebote(tenant_id: str, stichtag: date = None) -> list[AngebotDTO]:
    angebote = []
    items = dynamo_db_service.get_angebote(tenant_id)
    for item in items:
        angebot = create(item)
        if stichtag is None or angebot.gueltigBis is None or angebot.gueltigBis >= stichtag:
            angebote.append(angebot)
    return angebote


def delete_angebot(tenant_id: str, id: str) -> bool:
    angebot = get_angebot(tenant_id, id)
    if angebot:
        dynamo_db_service.delete_angebot(tenant_id, id)
        return True
    else:
        return False

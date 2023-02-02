import uuid
import json
from datetime import date
from lambda_utils.validation import check_required_field, check_daterange
from lambda_utils.env_utils import getenv_as_boolean
from lambda_utils.date_utils import fromisoformat, compute_ttl_for_date


def create(item: dict):
    bezeichnung = item.get('bezeichnung')
    check_required_field(bezeichnung, 'bezeichnung')
    preisInEuro = item.get('preisInEuro')
    check_required_field(preisInEuro, 'preisInEuro')
    gueltigVon = item.get('gueltigVon')
    gueltigBis = item.get('gueltigBis')
    gueltigVonDate = None if gueltigVon is None else fromisoformat(gueltigVon)
    gueltigBisDate = None if gueltigBis is None else fromisoformat(gueltigBis)
    check_daterange(gueltigVonDate, gueltigBisDate)
    return AngebotDTO(
        bezeichnung,
        float(preisInEuro),
        gueltigVonDate,
        gueltigBisDate,
        item.get('id')
    )


class AngebotDTO:

    def __init__(self, bezeichnung: str, preisInEuro: float, gueltigVon: date, gueltigBis: date, id: str = None):
        if id:
            self.id = id
        else:
            self.id = str(uuid.uuid4())
        self.bezeichnung = bezeichnung
        self.preisInEuro = preisInEuro
        self.gueltigVon = gueltigVon
        self.gueltigBis = gueltigBis
        self.ttl = compute_ttl_for_date(gueltigBis, 7) if getenv_as_boolean(
            'TTL_FEATURE_ACTIVE', True) else None

    def to_json(self):
        return json.dumps(self.__dict__, cls=AngebotDTOEncoder)


class AngebotDTOEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        else:
            return super().default(obj)

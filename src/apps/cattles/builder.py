from apps.dailytrans.builders.cattle import Api
from apps.dailytrans.builders.utils import (
    director,
    date_generator,
    DirectData,
)
from .models import Cattle


MODELS = [Cattle]
CONFIG_CODE = 'COG14'
LOGGER_TYPE_CODE = 'LOT-cattles'
# Cattle api has no date range filter, most set date_delta to 1
DELTA_DAYS = 1


@director
def direct(start_date=None, end_date=None, *args, **kwargs):

    data = DirectData(CONFIG_CODE, 2, LOGGER_TYPE_CODE)

    for model in MODELS:
        api = Api(model=model, **data._asdict())
        for delta_start_date, delta_end_date in date_generator(start_date, end_date, DELTA_DAYS):
            response = api.request(date=delta_start_date)
            api.load(response)

    return data

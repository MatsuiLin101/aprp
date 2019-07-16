import datetime
from django.test import TestCase
from django.core.management import call_command
from apps.dailytrans.models import DailyTran
from apps.rices.models import Rice
from apps.dailytrans.builders.rice_avg import Api


class BuilderTestCase(TestCase):

    def setUp(self):
        # load fixtures
        call_command('loaddata', 'configs.yaml', verbosity=0)
        call_command('loaddata', 'cog01.yaml', verbosity=0)

        self.start_date = datetime.date(year=2019, month=1, day=1)
        self.end_date = datetime.date(year=2019, month=1, day=1)

    def test_rice(self):
        # test create
        obj = Rice.objects.filter(code='pt_1japt').filter(track_item=True).first()

        api = Api(model=Rice, config_code='COG01', type_id=None)

        response = api.request(start_date=self.start_date,
                               end_date=self.end_date)
        api.load(response)

        count_qs = DailyTran.objects.filter(date=self.start_date,
                                            product=obj)

        self.assertEquals(count_qs.count(), 1)

        # test update by load again
        api.load(response)

        self.assertEquals(count_qs.count(), 1)

        # rice dailytran count
        count_qs = DailyTran.objects.filter(date=self.start_date)
        self.assertEquals(count_qs.count(), 15)

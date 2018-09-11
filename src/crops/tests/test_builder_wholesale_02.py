import datetime
from django.core.management import call_command
from django.test import TestCase
from crops.builder import direct_wholesale_02
from dailytrans.models import DailyTran
from crops.models import Crop
from configs.models import Source
from django.db.models import Q


class BuilderTestCase(TestCase):
    def setUp(self):
        # load fixtures
        call_command('loaddata', 'configs.yaml', verbosity=0)
        call_command('loaddata', 'sources.yaml', verbosity=0)
        call_command('loaddata', 'cog02.yaml', verbosity=0)

        self.start_date = datetime.date(year=2017, month=1, day=1)
        self.end_date = datetime.date(year=2017, month=1, day=3)

    def test_direct_single(self):
        direct_wholesale_02(start_date=self.start_date, end_date=self.end_date)
        crop = Crop.objects.filter(code='F').first()
        sources = Source.objects.filter(Q(name__exact='臺北一') | Q(name__exact='臺北二'))

        qs = DailyTran.objects.filter(product=crop,
                                      source__in=sources,
                                      date__range=(self.start_date, self.end_date))
        self.assertEquals(qs.count(), 2)

    def test_direct_multi(self):
        start_date = datetime.date(year=2017, month=1, day=1)
        end_date = datetime.date(year=2017, month=1, day=10)

        direct_wholesale_02(start_date=start_date, end_date=end_date)
        crop_ids = Crop.objects.filter(Q(code='F') | Q(code='O')).values('id')
        sources = Source.objects.filter(Q(name__exact='臺北一') | Q(name__exact='臺北二'))

        qs = DailyTran.objects.filter(product__id__in=crop_ids,
                                      source__in=sources,
                                      date__range=(start_date, end_date))
        self.assertEquals(qs.count(), 28)

    def test_delete(self):
        crop = Crop.objects.filter(code='F').first()
        source = Source.objects.last()

        # this item should be deleted
        DailyTran.objects.create(product=crop,
                                 source=source,
                                 avg_price=120,
                                 date=self.start_date,
                                 update_time=datetime.datetime.now())

        direct_wholesale_02(start_date=self.start_date, end_date=self.end_date)
        qs = DailyTran.objects.filter(product=crop,
                                      date__range=(self.start_date, self.end_date))
        self.assertEquals(qs.count(), 20)

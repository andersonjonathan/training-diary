from django.core.management.base import BaseCommand
from activities.convert import convert, strip_units
from activities.models import Activity, Lap, DataPoint
from django.db.utils import IntegrityError
from pathlib import Path


class Command(BaseCommand):
    help = 'Checks schedule and performs internal action.'

    def add_arguments(self, parser):
        parser.add_argument('folder', nargs=1, type=str)

    def handle(self, *args, **options):
        path_list = Path(options['folder'][0]).glob('*.fit')
        for path in sorted(path_list):
            print(str(path))
            activity = strip_units(convert(str(path)))
            laps = activity['laps']
            data = activity['data']
            del activity['laps']
            del activity['data']
            try:
                a = Activity.objects.create(**activity)
                ln = 1
                django_laps = []
                django_data_points = []
                for lap in laps:
                    lap['activity'] = a
                    django_laps.append(Lap(lap_nr=ln, **lap))
                    ln += 1
                Lap.objects.bulk_create(django_laps)
                for datum in data:
                    datum['activity'] = a
                    django_data_points.append(DataPoint(**datum))
                DataPoint.objects.bulk_create(django_data_points)
            except IntegrityError:
                print('{} already exists.'.format(activity['timestamp']))

from django.core.management.base import BaseCommand

from covid_update.descarga import descargar_catalogos
from covid_update.catalogos import procesar_catalogos
from covid_update.actualizar.catalogos import actualizar_catalogos


class Command(BaseCommand):
    help = 'Actualizar los catalogos de la base de datos de COVID'

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-descargar',
            action='store_true',
            help='Descargar los datos',
        )

    def handle(self, *args, **options):
        if not options['no_descargar']:
            descargar_catalogos()

        procesar_catalogos()
        actualizar_catalogos()

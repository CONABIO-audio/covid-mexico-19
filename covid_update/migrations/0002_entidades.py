# Generated by Django 3.0.5 on 2020-04-14 07:30
import os

from django.db import migrations
from django.db import transaction
from django.contrib.gis.geos import MultiPolygon
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.gdal import DataSource


RUTA_ENTIDADES_SHP = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'data',
    'marco_geoestadistico',
    'ent',
    '01_32_ent.shp')


@transaction.atomic
def cargar_entidades(apps, schema_editor):
    Entidad = apps.get_model("covid_data", "Entidad")

    fuente = DataSource(RUTA_ENTIDADES_SHP)
    capa = fuente[0]

    for entidad in capa:
        descripcion = entidad.get('NOMGEO')
        clave = entidad.get('CVE_ENT')

        geometria = entidad.geom
        geometria = GEOSGeometry(geometria.wkt, srid=6372)
        geometria_web = geometria.transform(3857, clone=True)

        if geometria.geom_type == 'Polygon':
            geometria = MultiPolygon(geometria)
            geometria_web = MultiPolygon(geometria_web)

        entidad, creado = Entidad.objects.get_or_create(
            clave=clave,
            descripcion=descripcion,
            defaults=dict(
                geometria=geometria,
                geometria_web=geometria_web))

        if creado:
            print(f'entidad creado {entidad}')


class Migration(migrations.Migration):
    dependencies = [
        ('covid_update', '0001_actualizacion'),
    ]
    operations = [
        migrations.RunPython(cargar_entidades)
    ]
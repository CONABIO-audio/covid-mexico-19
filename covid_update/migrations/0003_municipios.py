# Generated by Django 3.0.5 on 2020-04-14 07:31
import os

from django.db import migrations
from django.db import transaction
from django.contrib.gis.geos import MultiPolygon
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.gdal import DataSource


RUTA_MUNICIPIOS_SHP = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'data',
    'marco_geoestadistico',
    'mun',
    '01_32_mun.shp')


@transaction.atomic
def cargar_municipios(apps, schema_editor):
    Entidad = apps.get_model("covid_data", "Entidad")
    Municipio = apps.get_model("covid_data", "Municipio")

    fuente = DataSource(RUTA_MUNICIPIOS_SHP)
    capa = fuente[0]

    for municipio in capa:
        descripcion = municipio.get('NOMGEO')
        clave_municipio = municipio.get('CVE_MUN')
        clave_entidad = municipio.get('CVE_ENT')
        clave = municipio.get('CVEGEO')

        entidad = Entidad.objects.get(clave=clave_entidad)
        geometria = municipio.geom

        geometria = GEOSGeometry(geometria.wkt, srid=6372)
        geometria_web = geometria.transform(3857, clone=True)

        if geometria.geom_type == 'Polygon':
            geometria = MultiPolygon(geometria, srid=6372)
            geometria_web = MultiPolygon(geometria_web, srid=3857)

        municipio, creado = Municipio.objects.get_or_create(
            clave=clave,
            descripcion=descripcion,
            defaults=dict(
                clave_municipio=clave_municipio,
                entidad=entidad,
                geometria=geometria,
                geometria_web=geometria_web))

        if creado:
            print(f'Municipio creado {municipio}')


class Migration(migrations.Migration):

    dependencies = [
        ('covid_update', '0002_entidades'),
    ]

    operations = [
        migrations.RunPython(cargar_municipios)
    ]

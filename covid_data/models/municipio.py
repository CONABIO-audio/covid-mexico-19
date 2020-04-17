from django.db import models
from django.contrib.gis.db.models import MultiPolygonField, PointField
from covid_data.models.base import ModeloBase


class Municipio(ModeloBase):
    clave = models.IntegerField(unique=True)
    descripcion = models.CharField(max_length=80)

    clave_municipio = models.IntegerField()
    entidad = models.ForeignKey(
        'Entidad',
        on_delete=models.CASCADE)

    geometria = MultiPolygonField(srid=4326)
    geometria_web = MultiPolygonField(srid=3857)

    centroide = PointField(srid=4326)
    centroide_web = PointField(srid=3857)

    def __repr__(self):
        return self.descripcion

    def __str__(self):
        return self.descripcion

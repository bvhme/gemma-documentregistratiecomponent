"""
Serializers of the Document Registratie Component REST API
"""

from drf_extra_fields.fields import Base64FileField
from rest_framework import serializers
from zds_schema.validators import URLValidator

from drc.datamodel.models import (
    EnkelvoudigInformatieObject, ZaakInformatieObject
)


class AnyFileType:
    def __contains__(self, item):
        return True


class AnyBase64File(Base64FileField):
    ALLOWED_TYPES = AnyFileType()

    def get_file_extension(self, filename, decoded_file):
        return "bin"


class EnkelvoudigInformatieObjectSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the EnkelvoudigInformatieObject model
    """
    inhoud = AnyBase64File()

    class Meta:
        model = EnkelvoudigInformatieObject
        fields = (
            'url',
            'identificatie',
            'bronorganisatie',
            'creatiedatum',
            'titel',
            'vertrouwelijkaanduiding',
            'auteur',
            'formaat',
            'taal',
            'inhoud',
            'link',
            'beschrijving',

            'informatieobjecttype'  # van-relatie
        )
        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid',
            },
            'informatieobjecttype': {
                'validators': [URLValidator()],
            }
        }


class ZaakInformatieObjectSerializer(serializers.HyperlinkedModelSerializer):
    # TODO: valideer dat ZaakInformatieObject.informatieobjecttype hoort bij zaak.zaaktype
    class Meta:
        model = ZaakInformatieObject
        fields = (
            'url',
            'zaak',
            'informatieobject'
        )
        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid',
            },
            'informatieobject': {
                'lookup_field': 'uuid',
            }
        }

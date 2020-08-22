from typing import Dict

from django import forms
from django.db.models import Model


class SingleObject:
    model = None
    pk_attr = "pk"

    def get_object_id(self) -> str:
        oid = self.kwargs[self.pk_attr]
        return oid

    def get_object(self) -> Model:
        oid = self.get_object_id()
        obj = self.model.objects.filter(pk=oid).first()
        return obj

    @classmethod
    def shadow_pk(cls, dct: Dict) -> None:
        try:
            del dct[cls.pk_attr]
        except KeyError:
            pass

    @classmethod
    def update_object(cls, obj, form: forms.Form) -> None:
        for attr, value in form.cleaned_data.items():
            setattr(obj, attr, value)

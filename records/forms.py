from django import forms
from django.core.exceptions import ValidationError

from records.models import Record

EMPTY_RECORD_ERROR = '你不能提交一条空的记录！'
DUPLICATE_RECORD_ERROR = '你已经提交过此成长记录！'


class RecordForm(forms.models.ModelForm):

    def save(self, for_pack):
        self.instance.pack = for_pack
        return super().save()

    class Meta:
        model = Record
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(
                attrs={
                    'placeholder': '输入一条成长记录',
                    'class': 'form-control input-lg'
                }
            )
        }
        error_messages = {
            'text': {'required': EMPTY_RECORD_ERROR}
        }


class ExistingRecordForm(RecordForm):

    def __init__(self, for_pack, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.pack = for_pack

    def save(self):
        return forms.models.ModelForm.save(self)

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_RECORD_ERROR]}
            self._update_errors(e)

from django import forms

from records.models import Record

EMPTY_RECORD_ERROR = '你不能输入一条空的记录！'


class RecordForm(forms.models.ModelForm):

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

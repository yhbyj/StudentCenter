from django import forms

from records.models import Record

EMPTY_RECORD_ERROR = '你不能提交一条空的记录！'


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

from django.forms import ModelForm
from uni_form.helper import FormHelper
from uni_form.layout import Layout, Fieldset, ButtonHolder, Submit, MultiField, Row, Div
from samklang_media.models import Document
from samklang_media.widgets import UploadWidget

class ImageForm(ModelForm):
    class Meta:
        model = Document
        fields = ('file', 'filename', 'tags', 'show', 'group')

class UploadForm(ModelForm):

    class Meta:
        model = Document
        fields = ('file',)
        widgets = {'file': UploadWidget(upload={'rowselector': 'div.ctrlHolder'})}

class ManageDocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ('filename','show','group','tags')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
                Fieldset(
                    '',
                    'filename',
                    'tags',
                    Row(
                        'show',
                        'group',
                        css_class="share",
                        ),
                    )
        )
        #ButtonHolder(
                #Submit('submit', 'Save', css_class='button white')
            #)
        return super(ManageDocumentForm, self).__init__(*args, **kwargs)

class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ('file', 'filename', 'tags', 'show', 'group')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.add_input(Submit('button', 'Submit'))
        return super(DocumentForm, self).__init__(*args, **kwargs)

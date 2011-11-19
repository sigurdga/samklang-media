from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

__all__ = ( 'UploadWidget', )

class UploadWidget(forms.ClearableFileInput):
    """
    Widget for background uploading of files
    """

    default_options = {
        'rowselector': 'p',
    }

    def __init__(self, *args, **kwargs):
        self.options = self.default_options.copy()
        if "upload" in kwargs:
            self.options.update(kwargs.pop("upload"))
        super(UploadWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs):
        data = super(UploadWidget, self).render(name, value, attrs)
        self.options['id'] = attrs.get('id')

        javascript = """
<div id="upl_status"></div>
<script>
    document.addEvent('domready', function(){
        var uploader = new Uploader('%(id)s', { rowselector: '%(rowselector)s' });
    });
</script>
        """ % self.options
        return mark_safe(data + javascript)

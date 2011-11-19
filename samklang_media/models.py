from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site

from hashlib import sha1

from samklang_media.storage import UpdateIgnoreStorage
from samklang_utils import slugify

import os
from os.path import splitext

from taggit.managers import TaggableManager

def githash(data):
    """
    Hash the contents of a file like git does. Taken from
    http://stackoverflow.com/questions/552659/assigning-git-sha1s-without-git
    """

    s = sha1()
    s.update("blob %u\0" % len(data))
    s.update(data)
    return s.hexdigest()

def get_upload_to(instance, filename):
    """
    Generate funny file path / url
    """

    # TODO: attach celery command (if that's what it's called) to resize images or do other stuff
    # maybe it is possible to extend image or other models with fields for randomized parts of url

    hexdigest = githash(instance.file.read())
    folder1 = hexdigest[:2]
    folder2 = hexdigest[2:4]
    folder3 = hexdigest
    folder = os.path.join(folder1, folder2, folder3, "o")

    name, ext = splitext(filename)
    return os.path.join(folder, slugify(name) + ext)

class MediaBase(models.Model):
    """
    Base model for media types
    """

    file = models.FileField(upload_to=get_upload_to, storage=UpdateIgnoreStorage(), verbose_name=_('File'))
    filename = models.CharField(max_length=60, verbose_name=_('Filename'))
    content_type = models.CharField(verbose_name=_('Content type'), max_length=80, blank=True)
    content_category = models.SmallIntegerField(verbose_name=_('Content category'), blank=True)
    submit_date = models.DateTimeField(auto_now_add=True)
    site = models.ForeignKey(Site, verbose_name=_('Site'), blank=True)
    user = models.ForeignKey(User, verbose_name=_('User'), blank=True)
    group = models.ForeignKey(Group, null=True, blank=True, verbose_name=_('Group'))
    show = models.BooleanField(_('Published'), default=False)
    tags = TaggableManager(_('Tags'), blank=True)

    class Meta:
        abstract = True
        ordering = ["-submit_date"]

    def __unicode__(self):
        return self.filename

    @models.permalink
    def get_absolute_url(self):
        return ('media-file-detail', [self.pk])


class Document(MediaBase):
    """Generic document type"""


    class Meta:
        verbose_name, verbose_name_plural = _("Document"), _("Documents")
        db_table = 'samklang_media'

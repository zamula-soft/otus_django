import os
from io import BytesIO
from urllib.parse import quote, urljoin

from PIL import Image, ImageOps
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import models


class UserProfile(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to=settings.USER_IMAGE_DIR)

    # todo resize image only if user.created or image field has been updated
    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)
        if self.avatar:
            buffer = BytesIO()
            image = Image.open(self.avatar)
            thumbnail = ImageOps.fit(image, settings.USER_IMAGE_SIZE, Image.ANTIALIAS)
            thumbnail.save(buffer, format="PNG")
            default_storage.save(self.thumbnail_name, ContentFile(buffer.getvalue()))

    @property
    def thumbnail_name(self):
        if not self.avatar:
            return
        basename, _ = os.path.splitext(os.path.basename(self.avatar.name))
        filename = '%s/thumbnail.%s.png' % (settings.USER_IMAGE_DIR, basename)
        return filename

    @property
    def thumbnail_url(self):
        if self.thumbnail_name and default_storage.exists(self.thumbnail_name):
            return default_storage.url(self.thumbnail_name)
        else:
            placeholder = settings.USER_IMAGE_PLACEHOLDER
            if apps.is_installed('django.contrib.staticfiles'):
                from django.contrib.staticfiles.storage import staticfiles_storage
                return staticfiles_storage.url(placeholder)
            else:
                return urljoin(settings.STATIC_URL, quote(placeholder))
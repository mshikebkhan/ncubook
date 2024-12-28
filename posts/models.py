from django.db import models
from django.contrib.auth.models import User
import os
from django.conf import settings
from PIL import Image

# Where Post Pic Will Store
def post_pic_dir_path(instance, filename):
    post_pic_name = 'user_data/{0}/post_pics/{1}'.format(instance.user.username,filename)
    full_path = os.path.join(settings.MEDIA_ROOT, post_pic_name)

    if os.path.exists(full_path):
    	os.remove(full_path)

    return post_pic_name

# Where Post PDF Will Store
def post_pdf_dir_path(instance, filename):
    post_pdf_name = 'user_data/{0}/post_pdfs/{1}'.format(instance.user.username,filename)
    full_path = os.path.join(settings.MEDIA_ROOT, post_pdf_name)

    if os.path.exists(full_path):
    	os.remove(full_path)

    return post_pdf_name

# File Input Validation
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

def file_size(value): # add this to some file where you can import it from
    limit = 10 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 10 MB.')

class Post(models.Model):
    # User
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Main Content
    body = models.TextField(max_length=200)
    url = models.URLField(max_length=200, blank=True, null=True)
    pic = models.ImageField(upload_to=post_pic_dir_path, validators=[file_size], blank=True, null=True)
    pdf = models.FileField(upload_to=post_pdf_dir_path, validators=[file_size, FileExtensionValidator(allowed_extensions=["pdf"])], blank=True, null=True)

    # Meta Info
    likes = models.PositiveIntegerField(default=0)
    reported = models.BooleanField(default=False)

    # Date
    date_created = models.DateTimeField(auto_now_add=True, null=True)


    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs) # Save it here as image cmprss needed saved post

        if self.pic:
            # Compress Profile Pic 
            image = Image.open(self.pic.path)
            try:
              exif = image.info['exif']
            except KeyError:
              exif = None

            if exif != None: # Check If exif Is Not Empty          
                image.save(self.pic.path,quality=33,optimize=True, exif=exif)

    def __str__(self):
        return self.body[:50]

class Comment(models.Model):
    # User & Post
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    # Main Content
    body = models.TextField(max_length=100)

    # Meta Info
    reported = models.BooleanField(default=False)

    # Date
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.body[:50]
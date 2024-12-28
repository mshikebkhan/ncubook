from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image, ImageOps
import os
from django.conf import settings
from posts.models import Post

class CoarseBranch(models.Model):
    title = models.CharField(max_length=30)
    def __str__(self):
        return str(self.title) 

    class Meta:
         verbose_name_plural = "Coarse Branches"

# Where Profile Pic Will Store
def profile_pic_dir_path(instance, filename):
    profile_pic_name = 'user_data/{0}/profile_pic/{1}'.format(instance.user.username,filename)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)

    if os.path.exists(full_path):
    	os.remove(full_path)

    return profile_pic_name

# Year Validator To Make Sure That User Is A Current Student Of NCU
from_year = datetime.date.today().year-5 # 5 Years Ago
to_year = datetime.date.today().year # Current Year

# Gender choice
genders = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

class Profile(models.Model):
    # User
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Profile Information
    profile_pic = models.ImageField(default='website_data/default_profile_pic/default.png', upload_to=profile_pic_dir_path)
    roll = models.CharField(max_length=30, unique=True, null=True)
    verified_roll = models.CharField(max_length=30, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=genders, null=True)
    coarse_branch = models.ForeignKey(CoarseBranch, on_delete=models.PROTECT, null=True)
    year = models.IntegerField(validators=[MinValueValidator(from_year), MaxValueValidator(to_year)], null=True)
    hometown = models.CharField(max_length=100, blank=True, null=True)
    interests = models.CharField(max_length=300, blank=True, null=True)
    birthday =  models.DateField(null=True)
    otp = models.IntegerField(max_length=5, blank=True, null=True)
    email = models.EmailField(blank=True ,null=True)
    verified = models.BooleanField(default=False)

    liked_posts = models.ManyToManyField(Post, blank=True, related_name="liked_posts")

    # Buddy Requests Sent
    requested = models.ManyToManyField(User, blank=True, related_name="requested")

    # Buddies
    buddies = models.ManyToManyField(User, blank=True, related_name="buddies")

    def save(self, *args, **kwargs):
        # Capitalise Roll No. & Update Email
        if self.roll: # Avoid Signup Errors
            roll = self.roll
            self.roll = roll.upper()
            
            self.email = str(self.roll) + settings.UNIVERSITY_DOMAIN

        super(Profile, self).save(*args, **kwargs) # Save it here as image cmprss needed saved profile

        # Compress Profile Pic 
        image = Image.open(self.profile_pic.path)
        try:
          exif = image.info['exif']
        except KeyError:
          exif = None

        if exif != None: # Check If exif Is Not Empty          
            image.save(self.profile_pic.path,quality=33,optimize=True, exif=exif)

    def __str__(self):
        return str(self.user)

class BuddyRequest(models.Model):
    # Users
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buddy_request_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)

    # Meta Info
    seen = models.BooleanField(default=False)

    # Date
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.sender} to {self.receiver}"   

    class Meta:
         verbose_name_plural = "Buddy Requests"

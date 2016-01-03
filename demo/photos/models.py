from django.db import models

# Create your models here.

class Photo( models.Model ):
    """The slug field is really not necessary, but makes the code simpler. 
    ImageField depends on PIL or pillow (where Pillow is easily installable
    in a virtualenv. If you have problems installing pillow, use a more 
    generic FileField instead.
    """
    
    file = models.ImageField(upload_to = "pictures")
    slug = models.SlugField(max_length=50, blank=True)

    def __unicode__(self):
        return self.file.name

    @models.permalink
    def get_absolute_url(self):
        return ('jfu_upload', )

    def save(self, *args, **kwargs):
        self.slug = self.file.name
        super(Photo, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """delete -- Remove to leave file."""
        self.file.delete(False)
        super(Photo, self).delete(*args, **kwargs)

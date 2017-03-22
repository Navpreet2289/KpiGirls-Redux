from django.db import models
from django.conf import settings
from django.core.cache import cache
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from imagekit.processors import Adjust, ResizeToFill
from django.utils.translation import ugettext_lazy as _
from imagekit.models import ProcessedImageField, ImageSpecField

from slugify import UniqueSlugify
from girls_proj.utils.model_utils import UploadToPathAndRename


class FacemashQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)
    def count_average(self):
        return self.aggregate(
            rating=models.Avg('ratings'),
            rd=models.Avg('rd'),
            sigma=models.Avg('sigma'),
            vk_aver=models.Avg('vk_id')
        )


class Facemash(models.Model):
    RELATION_CHOICES = (
        (-1, 'status -1'),
        (0, 'status 0'),
        (1, 'status 1'),
        (2, 'status 2'),
        (3, 'status 3'),
        (4, 'status 4'),
        (5, 'status 5'),
        (6, 'status 6'),
        (7, 'status 7'),
        (8, 'status 8'),
    )
    user = models.OneToOneField(User, related_name='facemash', on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    status = models.CharField(max_length=256, null=True, blank=True, verbose_name=_('статус в соц мережі'))
    relation = models.IntegerField(choices=RELATION_CHOICES, verbose_name=_('заміжній статус'))
    vk_id = models.PositiveIntegerField(unique=True)
    photo = ProcessedImageField(upload_to=UploadToPathAndRename('girls_images'),
                                processors=[
                                ResizeToFill(200, 200),
                                Adjust(sharpness=1.1, contrast=1.1)],
                                format='JPEG',
                                options={'quality': 90})

    ratings = models.FloatField(default=1500)
    rd = models.FloatField(default=350, help_text='rating deviation')
    sigma = models.FloatField(default=0.06, help_text='sigma is used as the expression for volatility')

    slug = models.SlugField(unique=True, null=True, blank=True, max_length=100, help_text=_("automatically generated, don't change manually !"))
    is_active = models.BooleanField(
        help_text=_(
            "Tick to make this entry live (see also the publication date). "
            "Note that administrators (like yourself) are allowed to preview "
            "inactive entries whereas the general public aren't."
        ),
        default=True,
    )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    objects = FacemashQuerySet.as_manager()

    class Meta:
        verbose_name='Girl'
        verbose_name_plural = 'Girls'

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def delete(self):
        cache.delete('girl_{id}'.format(id=self.id))
        super(Facemash, self).delete()

    def get_absolute_url(self):
        return reverse('facemash:detail', kwargs={'slug': self.slug})

    def get_hits_count(self):
        return cache.get('girl_{}'.format(self.id), [set(), 0])[1]

    photo_sm = ImageSpecField(
        source='photo',
        processors=[ResizeToFill(100, 100)],
        format='JPEG',
        options={'quality': 80}
    )

    # thumbnail for admin interface
    def admin_image_thumb(self):
        return '<img src="{0}{1}" width="50" height="50" />'.format(settings.MEDIA_URL, self.photo)
    admin_image_thumb.allow_tags = True

    def get_vk(self):
        return "https://vk.com/id{}".format(self.vk_id)

    def get_relation(self):
        for choice in Facemash.RELATION_CHOICES:
            if choice[0] == self.relation:
                return choice[1]


def my_unique_check(text, uids):
    if text in uids:
        return False
    return not Facemash.objects.filter(slug=text).exists()


@receiver(post_save, sender=Facemash)
def create_facemash(sender, instance, created, **kwargs):
    if created:
        slugify_unique = UniqueSlugify(
            unique_check=my_unique_check,
            separator='-',
            to_lower=True,
            max_length=100
        )
        instance.slug = slugify_unique(instance.first_name + '.' + instance.last_name)
        instance.save()
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin

# Create your models here.
from django.db.models import Avg, Count
from django.forms import ModelForm, Select, TextInput, FileInput
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.urls import reverse


class Category(MPTTModel):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField()
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children',on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return '/'.join(full_path[::-1])

    class MPTTMeta:
        order_insertion_by = ['title']

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    # Automatically Creating Slug
    def get_absolute_url(self):
        return reverse('category_detail',kwargs={'slug':self.slug})

class Note(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # relation with Category table
    title = models.CharField(max_length=200)
    keywords = models.CharField(blank=True,max_length=255)
    description = models.CharField(blank=True,max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    file = models.FileField(blank=True, upload_to='images/')
    detail = RichTextUploadingField()
    slug = models.SlugField(null=False, unique=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('note_details',kwargs={'slug':self.slug})

    def averagereview(self):
        reviews = Comment.objects.filter(note=self).aggregate(average = Avg('rate'))
        avg = 0
        if reviews["average"] is not None:
            avg = float(reviews["average"])
        return avg

    def countreview(self):
        reviews = Comment.objects.filter(note=self).aggregate(count = Count('id'))
        cnt = 0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt


class Images(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def _str_(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'

class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    note= models.ForeignKey(Note,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    subject= models.CharField(max_length=50)
    comment = models.TextField(max_length=50, blank=True)
    rate= models.IntegerField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='False')
    ip = models.CharField(blank=True,max_length=20 )
    create_at=models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['category', 'title', 'keywords', 'description', 'image', 'file',  'detail', 'slug']
        widgets = {
            'category': Select(attrs={'class': 'input', 'placeholder': 'amount'}, choices={Category.objects.all()}),
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'title'}),
            'keywords': TextInput(attrs={'class': 'input', 'placeholder': 'keywords'}),
            'description': TextInput(attrs={'class': 'input', 'placeholder': 'description'}),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'image', }),
            'file': FileInput(attrs={'class': 'input', 'placeholder': 'file', }),
            'detail': CKEditorWidget(),  # Ckeditor input
        }

        def get_absolute_url(self):
            return reverse('addnote', kwargs={'slug': self.slug})


class NoteImageForm(ModelForm):
    class Meta:
        model = Images
        fields = ['title', 'image']
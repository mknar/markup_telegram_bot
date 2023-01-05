from django.contrib.auth.models import User
from django.db import models
from django.utils.html import mark_safe


class Object(models.Model):
    image = models.ImageField(upload_to='objects')
    marked = models.BooleanField(default=False)

    @property
    def thumbnail_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="120" height="auto" />'.format(self.image.url))
        return ""

    def __str__(self):
        return f'object: {self.id}'

    class Meta:
        db_table = 'objects'


class Classification(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'classifications'


class MarkingTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    object = models.ForeignKey(Object, on_delete=models.CASCADE, null=True)
    classification = models.ForeignKey(Classification, on_delete=models.CASCADE, null=True, related_name='marking_tasks')

    def __str__(self):
        return f'Marking task: {self.id}| User: {self.user.username}| object: {self.object.id}| classification: {self.classification.title}'

    def save(self, *args, **kwargs):
        self.object.marked = True
        self.object.save()
        super(MarkingTask, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.object.marked = False
        self.object.save()
        super(MarkingTask, self).delete(*args, **kwargs)

    class Meta:
        db_table = 'marking_tasks'


class TelegramUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='telegram_user')
    telegram_user_id = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'telegram_user'

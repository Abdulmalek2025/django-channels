from django.db import models
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
# Create your models here.

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=100)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.body
    

    def save(self, *args, **kwargs):
        channel_layer = get_channel_layer()
        noteification_objs = Notification.objects.filter(is_read=False).count()
        data = {'count':noteification_objs,'current':self.body}

        async_to_sync(channel_layer.group_send)(
            'test_consumer_group',{
                'type': 'send_notification',
                'value':json.dumps(data)
            }
        )
        print("saved")
        super(Notification, self).save(*args,**kwargs)
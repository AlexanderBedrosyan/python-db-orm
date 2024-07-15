from django.core.exceptions import ValidationError
from django.db import models
from datetime import date

# Create your models here.

from django.db import models


class UserProfile(models.Model):

    username = models.CharField(max_length=70, unique=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)


class Message(models.Model):
    sender = models.ForeignKey(
        to=UserProfile,
        related_name='sent_messages',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        to=UserProfile,
        related_name='received_messages',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateField(auto_now=True)
    is_read = models.BooleanField(default=False)

    def mark_as_read(self):
        self.is_read = True

    def reply_to_message(self, reply_content: str):
        new_message = Message.objects.create(
            sender=self.receiver,
            receiver=self.sender,
            content=reply_content
        )
        new_message.save()
        return new_message

    def forward_message(self, receiver: UserProfile):
        new_message = Message.objects.create(
            sender=self.receiver,
            receiver=receiver,
            content=self.content
        )
        new_message.save()
        return new_message
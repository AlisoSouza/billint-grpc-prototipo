from django.db import models
import uuid


class Project(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.id} {self.name}"


class Channel(models.Model):
    # project = models.ForeignKey(Project, on_delete=models.CASCADE)
    uuid = models.UUIDField(
        "UUID",
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    active_contacts = models.PositiveIntegerField(default=0)

    def increase_active_contacts(self):
        self.active_contacts += 1
        self.save()


class Contact(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    last_seen_on = models.DateTimeField()
    message_uuid = models.UUIDField()
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)


    def __str__(self) -> str:
        return f"{self.uuid}"
from ..models import Contact, Channel
from .dto import ContactDTO


def create_contacts(contact_dto: ContactDTO):
    channel = get_or_create_channel(contact_dto.channel_uuid)
    try:
        contact = Contact.objects.get(uuid=contact_dto.contact_uuid)
        # depende do plano, se for contato ativo 30 dias se for atendimento 24 horas
        timedelta = contact_dto.last_seen_on - contact.last_seen_on
        if timedelta.days > 0:
            channel = contact.channel
            channel.increase_active_contacts()

    except Contact.DoesNotExist:
        contact = Contact.objects.create(
            uuid=contact_dto.contact_uuid,
            last_seen_on=contact_dto.last_seen_on,
            message_uuid=contact_dto.message_uuid,
            channel=channel
        )
        channel = contact.channel
        channel.increase_active_contacts()

    print(f"Created: {contact}")


def get_or_create_channel(channel_uuid: str) -> Channel:
    try:
        return Channel.objects.get(uuid=channel_uuid)
    except Channel.DoesNotExist:
        return Channel.objects.create(uuid=channel_uuid)

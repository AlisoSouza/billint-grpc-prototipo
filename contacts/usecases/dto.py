from dataclasses import dataclass


@dataclass
class ContactDTO:
    contact_uuid: str
    last_seen_on: str
    message_uuid: str
    channel_uuid: str

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "billing.settings")

if __name__ == '__main__':
   django.setup()

from concurrent import futures
import logging

import grpc
import contacts_pb2
import contacts_pb2_grpc
from contacts.usecases import ContactDTO, create_contacts


class Contacts(contacts_pb2_grpc.ContactsServicer):
    def CreateContacts(self, request, context):
        contacts = request.contacts
        for contact in contacts:
            contact_dto = ContactDTO(
                contact_uuid=contact.contact_uuid,
                message_uuid=contact.message_uuid,
                channel_uuid=contact.channel_uuid,
                last_seen_on=contact.message_date,
                
            )
            create_contacts(contact_dto)
        return contacts_pb2.CreateContactsResponse()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    contacts_pb2_grpc.add_ContactsServicer_to_server(Contacts(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    print("Starting server in: %s" % ('localhost:50051'))
    serve()
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "billing.settings")

if __name__ == '__main__':
   django.setup()

from concurrent import futures
import logging

import grpc
import message_pb2
import message_pb2_grpc
from contacts.usecases import ContactDTO, create_contacts


class Contacts(message_pb2_grpc.FlowsMesssageServicer):
    def CreateMessage(self, request, context):
        contact_message = request
        contact_dto = ContactDTO(
            contact_uuid=contact_message.contact_uuid,
            message_uuid=contact_message.message_uuid,
            channel_uuid=contact_message.channel_uuid,
            last_seen_on=contact_message.message_date,
            
        )
        create_contacts(contact_dto)
        return message_pb2.CreateFlowsMessageResponse(message="Created")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    message_pb2_grpc.add_FlowsMesssageServicer_to_server(Contacts(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    print("Starting server in: %s" % ('localhost:50051'))
    serve()
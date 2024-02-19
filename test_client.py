import grpc
import uuid
import contacts_pb2
import contacts_pb2_grpc
from datetime import datetime

channel_uuid = str(uuid.uuid4())
print(channel_uuid)

contacts = []

for _ in range(15):
    contact = contacts_pb2.Contact(
        contact_uuid=str(uuid.uuid4()),
        channel_uuid=channel_uuid,
        message_date=str(datetime.now()),
        message_uuid=str(uuid.uuid4()),
    )
    contacts.append(contact)

print(contacts)


def run():
    response = []
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = contacts_pb2_grpc.ContactsStub(channel)
        response = stub.CreateContacts(contacts_pb2.CreateContactsRequest(contacts=contacts))
        print(response)

if __name__ == "__main__":
    run()
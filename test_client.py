import grpc
import uuid
import message_pb2
import message_pb2_grpc
from datetime import datetime

channel_uuid = str(uuid.uuid4())

def run():
    response = []
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = message_pb2_grpc.FlowsMesssageStub(channel)
        for _ in range(15):
            response = stub.CreateMessage(
                message_pb2.CreateFlowsMessageRequest(
                    contact_uuid=str(uuid.uuid4()),
                    channel_uuid=channel_uuid,
                    message_date=str(datetime.now()),
                    message_uuid=str(uuid.uuid4()),
                )
            )
        print(response)

if __name__ == "__main__":
    run()

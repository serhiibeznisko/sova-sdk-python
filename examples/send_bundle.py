"""
Example: Send a bundle to Sova Network.
"""
import asyncio
import os
from datetime import datetime, timedelta
from google.protobuf.timestamp_pb2 import Timestamp
from sova_sdk import SovaClient, dto_pb2


async def main():
    # Create testnet client
    client = SovaClient.new_testnet_client()

    # Get private key from environment
    private_key_hex = os.getenv("SOVA_PRIVATE_KEY")
    if not private_key_hex:
        print("Please set SOVA_PRIVATE_KEY environment variable")
        return

    private_key = bytes.fromhex(private_key_hex)

    # Authenticate
    print("Authenticating...")
    client.authenticate(private_key)
    print("Authenticated!")

    # Get searcher client
    searcher = client.searcher()

    # Create bundle expiration time (5 minutes from now)
    expiration = Timestamp()
    expiration.FromDatetime(datetime.now() + timedelta(minutes=5))

    # Create a bundle with external messages
    # Note: Replace with your actual message data (BOC format)
    message_data = bytes.fromhex("your_message_boc_hex_here")

    bundle = dto_pb2.Bundle(
        message=[
            dto_pb2.ExternalMessage(data=message_data),
        ],
        expiration_ns=expiration,
        verification_rules=[]  # Add verification rules if needed
    )

    # Send the bundle
    print("Sending bundle...")
    try:
        response = await searcher.send_bundle(bundle)
        print(f"Bundle sent successfully!")
        print(f"Bundle ID: {response.id}")
    except Exception as e:
        print(f"Failed to send bundle: {e}")


if __name__ == "__main__":
    asyncio.run(main())

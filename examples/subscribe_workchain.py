"""
Example: Subscribe to mempool by workchain.
"""
import asyncio
import os
from sova_sdk import SovaClient


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

    # Define callback
    def on_packet(packet):
        print(f"Received packet with {len(packet.external_messages)} messages")
        for msg in packet.external_messages:
            print(f"  - Workchain {msg.workchain_id}, Gas: {msg.gas_spent}")

    # Subscribe to workchain 0 (basechain)
    workchain_id = 0
    print(f"\nSubscribing to workchain {workchain_id}...")
    await searcher.subscribe_by_workchain(workchain_id, on_packet)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped by user")

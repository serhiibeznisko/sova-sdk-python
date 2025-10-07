"""
Example: Subscribe to mempool by address.
"""
import asyncio
import os
from sova_sdk import SovaClient


async def main():
    # Create testnet client
    client = SovaClient.new_testnet_client()

    # Get private key from environment or use your own
    private_key_hex = os.getenv("SOVA_PRIVATE_KEY")
    if not private_key_hex:
        print("Please set SOVA_PRIVATE_KEY environment variable")
        return

    private_key = bytes.fromhex(private_key_hex)

    # Authenticate
    print("Authenticating...")
    token = client.authenticate(private_key)
    print(f"Authenticated! Token expires at: {token.expires_at_utc}")

    # Get searcher client
    searcher = client.searcher()

    # Define callback for mempool packets
    def on_packet(packet):
        print(f"\n=== Received Mempool Packet ===")
        print(f"Server timestamp: {packet.server_ts}")
        print(f"Expiration: {packet.expiration_ns} ns")
        print(f"Number of external messages: {len(packet.external_messages)}")

        for i, msg in enumerate(packet.external_messages):
            print(f"\nMessage {i + 1}:")
            print(f"  Hash: {msg.hash.hex()}")
            print(f"  Workchain ID: {msg.workchain_id}")
            print(f"  Shard: {msg.shard.hex()}")
            print(f"  Address: {msg.std_smc_address.hex()}")
            print(f"  Gas spent: {msg.gas_spent}")
            print(f"  Out messages: {len(msg.out_msgs)}")

    # Subscribe to specific addresses
    addresses = [
        "EQAvDfWFG0oYX19jwNDNBBL1rKNT9XfaGP9HyTb5nb2Eml6y",  # Example TON address
    ]

    print(f"\nSubscribing to addresses: {addresses}")
    await searcher.subscribe_by_address(addresses, on_packet)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped by user")

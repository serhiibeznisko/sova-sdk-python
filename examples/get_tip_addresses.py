"""
Example: Get tip addresses for bundle inclusion.
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

    # Get tip addresses
    print("\nFetching tip addresses...")
    try:
        response = await searcher.get_tip_addresses()
        print(f"\nTip Addresses:")
        for i, address in enumerate(response.address, 1):
            print(f"  {i}. {address}")
    except Exception as e:
        print(f"Failed to get tip addresses: {e}")


if __name__ == "__main__":
    asyncio.run(main())

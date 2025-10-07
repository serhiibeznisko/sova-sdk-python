"""
Example: Subscribe to bundle results.
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

    # Define callback for bundle results
    def on_result(result):
        print(f"\n=== Bundle Result ===")
        print(f"Bundle ID: {result.id}")

        if result.HasField('win'):
            print(f"Status: WON")
            print(f"Auction ID: {result.win.auction_id}")
            print(f"Estimated tip: {result.win.estimated_nanoton_tip} nanoTON")
        elif result.HasField('loose'):
            print(f"Status: LOST")
            print(f"Auction ID: {result.loose.auction_id}")

    print("\nSubscribing to bundle results...")
    await searcher.subscribe_bundle_result(on_result)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped by user")

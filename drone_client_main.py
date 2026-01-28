import asyncio
import signal
import sys
from drone_client import DroneClient, DroneConfig, DroneStatus

async def main():
    config = DroneConfig(
        base_url="http://localhost:8080/api",
        username="test_drone",
        password="123456",
        drone_id="test_drone",
        camera_index=0,
        image_quality=70,
        send_interval=0.5,
        max_retries=3,
        retry_delay=1.0,
        timeout=10.0
    )
    
    client = DroneClient(config)
    
    def signal_handler(signum, frame):
        print("\nReceived interrupt signal, shutting down...")
        client.stop_continuous_send()
        client.cleanup()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        if not client.login():
            print("Failed to login")
            return
        
        print("Starting continuous image sending...")
        await client.start_continuous_send()
        
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.stop_continuous_send()
        client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())

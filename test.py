import time
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    bootstrap_servers=['10.250.98.159:9092'],
    auto_offset_reset='earliest',
    group_id='DTS-JLAB-4',
)
consumer.subscribe(['ingestionTopic'])

while True:
    try:
        message = consumer.poll(10.0)

        if not message:
            time.sleep(120)  # Sleep for 2 minutes

        if message.error():
            print(f"Consumer error: {message.error()}")
            continue

        print(f"Received message: {message.value().decode('utf-8')}")
    except:
        # Handle any exception here
        ...
    finally:
        consumer.close()
        print("Goodbye")

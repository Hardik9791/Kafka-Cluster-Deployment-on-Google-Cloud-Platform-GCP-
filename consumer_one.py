from kafka.consumer import KafkaConsumer # type: ignore

# Kafka consumer configuration
topic = "HardikRathod-console-topic"
brokers = "localhost:9092"

# Create the Kafka consumer
consumer = KafkaConsumer(topic, bootstrap_servers=brokers)

# Continuously poll for new messages
for message in consumer:
    print(message.value.decode())
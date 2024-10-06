from kafka.consumer import KafkaConsumer # type: ignore

# Kafka consumer configuration
topic = "HardikRathod-console-topic"
brokers = "localhost:9092"

# Create the Kafka consumer
consumer = KafkaConsumer(topic, bootstrap_servers=brokers)


for message in consumer:
    # Decode the message as a JSON string
    HardikRathod = message.value.decode()
    
    # Write the fields to a file or database
    with open("result.csv", "a") as f:
        f.write("{0}\n".format(HardikRathod))

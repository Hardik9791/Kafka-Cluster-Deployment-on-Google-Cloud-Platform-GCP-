from kafka.producer import KafkaProducer # type: ignore
import time

# Kafka producer configuration
topic = "HardikRathod-console-topic"
brokers = "localhost:9092"

# Create the Kafka producer
producer = KafkaProducer(bootstrap_servers=brokers)

# Read the file
filename = "/home/hardik9791/logfile.log"
with open(filename, "r") as file:
    while True:
        # Seek to the end of the file
        file.seek(0, 2)

        # Wait for new data to be written to the file
        while True:
            where = file.tell()		# get current position in file
            line = file.readline()	# read a line
            if not line:		# if there is an empty string (ie no data)
                time.sleep(1)		# wait one second
                file.seek(where)	# check if there is any new data in the position
            else:
                # there was a string, send new line to the Kafka broker
                producer.send(topic, line.encode())
                producer.flush()	# wait until acknowledgement is received from broker before continuing
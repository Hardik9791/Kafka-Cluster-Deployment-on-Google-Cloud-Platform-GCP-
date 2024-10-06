# Kafka-Cluster-Deployment-on-Google-Cloud-Platform-GCP-
This repository contains the implementation of a scalable Kafka cluster on Google Cloud Platform (GCP) for real-time data processing. The project demonstrates efficient Kafka setup and management for distributed messaging, along with Python scripts for creating Kafka consumers and producers.

# First install Zookeeper and Kafka. 
Then start the Zookeeper server, then Kafka. The Zookeeper server is required for Kafka to function.


Enter the directory cd zookeeper-3.4.14

The program code for Zookeeper is bin/zkServer.sh start


Enter the directory cd confluent-4.1.4

The program code for Kafka is bin/kafka-server-start etc/kafka/server.properties



# Code for topic creation: rm bin/kafka-topics --create --zookeeper localhost:2181 --partitions 1 --replication-factor 1 --topic HardikRathod-console-topic



# Create write-to-file: vi write-to-file.sh

A write-to-file's contents:

#
file="logfile.log"

if [ -f $file ] ; then
    rm $file
fi

y=0

while :

do
    echo "Big Data Systems Architecture $y" >> logfile.log
    y=`expr $y + 1`
    echo 'sleeping for 3 seconds ...'
    sleep 3
done



# To run write-to-file: sh ./write-to-file.sh



# Create first consumer file: vi consumer-one.py

Code:

from kafka.consumer import KafkaConsumer

# Kafka consumer configuration
topic = "HardikRathod-console-topic"
brokers = "localhost:9092"

# Create the Kafka consumer
consumer = KafkaConsumer(topic, bootstrap_servers=brokers)

# Continuously poll for new messages
for message in consumer:
    print(message.value.decode())



# Create second consumer file: vi consumer-two.py

Code:

from kafka.consumer import KafkaConsumer

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



# Create producer file: vi producer-file.py

Code:

from kafka.producer import KafkaProducer
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



# To view the results stored in a csv file: run vi result.csv in the home directory.



# install python in Kafka: pip install kafka-python


Open terminal 1 and run write-to-file.sh
Open terminal 2 and run python consumer-one.py
Open terminal 3 and run python consumer-two.py
Open terminal 4 and run python producer-file.py



# open result.csv to view the output stored of second consumer file: vi result.csv



# Create a directory called Flume in home directory 

mkdir flume

cd flume

mkdir hardik-linux

cd hardik-linux



# Create Hardik-flume.conf file

Code:

# Flume Config File for Two Channels

# Flume Components
agent.sources = tail-source
agent.sinks = local-sink hdfs-sink
agent.channels = local-memory-channel hdfs-memory-channel

# Channels
agent.channels.local-memory-channel.type = memory
agent.channels.hdfs-memory-channel.type = memory

# Source
agent.sources.tail-source.type = exec
agent.sources.tail-source.command = tail -F /home/hardik9791/result.csv
agent.sources.tail-source.channels =  local-memory-channel hdfs-memory-channel

# Define a sink that outputs to local file.
agent.sinks.local-sink.type = file_roll
agent.sinks.local-sink.sink.directory = /home/hardik9791/flume/hardik-linux
agent.sinks.local-sink.sink.rollInterval = 20
agent.sinks.local-sink.channel = local-memory-channel

# Define a sink that outputs to hdfs.
agent.sinks.hdfs-sink.type = hdfs
agent.sinks.hdfs-sink.hdfs.path = /BigDatahardik/flume/hardik-hdfs
agent.sinks.hdfs-sink.hdfs.fileType = DataStream
agent.sinks.hdfs-sink.hdfs.rollCount = 5
agent.sinks.hdfs-sink.hdfs.inUseSuffix = .hardik
agent.sinks.hdfs-sink.channel = hdfs-memory-channel




# To show replication, run a simple flume agent.

flume-ng agent --conf /home/hardik9791/flume/hardik-linux/ -f /home/hardik9791/flume/hardik-linux/hardik-flume.conf -Dflume.root.logger=DEBUG,console -n agent



# Run Flume in another SSH terminal after launching the conf file.

HDFS:

hadoop fs -ls /BigDatahardik/flume/hardik-hdfs

hadoop fs -cat /BigDatahardik/flume/hardik-hdfs/Any name will do for this file.


# To see the result of the Hadoop file:

hadoop fs -cat /BigDatahardik/flume/hardik-hdfs/FlumeData.1688516230348-15

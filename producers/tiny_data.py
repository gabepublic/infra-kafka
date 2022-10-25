##############################################################################
# Source: https://github.com/PacktPublishing/
#                     Snowflake---Build-and-Architect-Data-Pipelines-using-AWS/
#                     blob/main/Section%2011%20-kafka-streaming-snowflake/
#                     producer.py
##############################################################################from time import sleep
from json import dumps
from time import sleep
from kafka import KafkaProducer

no_of_data = 2
sleep_time_sec = 3 
topic_name='TestTopic'

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))


for e in range(no_of_data):
    data = {'number' : e}
    print(data)
    producer.send(topic_name, value=data)
    sleep(sleep_time_sec)
print("exiting...")
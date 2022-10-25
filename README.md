# infra-kafka

The Kafka infranstructure setup and various tests.

## SETUP Kafka

### Manual Startup (Debian)

[Source]: https://kafka.apache.org/quickstart

- Prerequisite - install Java 8+
```
$ sudo apt update
$ sudo apt install default-jre
$ java --version
openjdk 11.0.16 2022-07-19
OpenJDK Runtime Environment (build 11.0.16+8-post-Ubuntu-0ubuntu120.04)
OpenJDK 64-Bit Server VM (build 11.0.16+8-post-Ubuntu-0ubuntu120.04, mixed mode, sharing)
$
```

- The download page https://kafka.apache.org/downloads

- Download the latest version to the *user home directory*
```
$ cd ~
$ curl "https://downloads.apache.org/kafka/3.3.1/kafka_2.13-3.3.1.tgz" -o ~/kafka_2.13-3.3.1.tgz
$ ls -al kafka_2.13-3.3.1
total 76
drwxr-xr-x 8 gabe gabe  4096 Oct 16 20:37 .
drwxr-xr-x 9 gabe gabe  4096 Oct 24 15:21 ..
-rw-rw-r-- 1 gabe gabe 14842 Sep 29 12:03 LICENSE
-rw-rw-r-- 1 gabe gabe 28184 Sep 29 12:03 NOTICE
drwxr-xr-x 3 gabe gabe  4096 Sep 29 12:06 bin
drwxr-xr-x 3 gabe gabe  4096 Sep 29 12:06 config
drwxr-xr-x 2 gabe gabe  4096 Oct 15 22:01 libs
drwxr-xr-x 2 gabe gabe  4096 Sep 29 12:06 licenses
drwxrwxr-x 2 gabe gabe  4096 Oct 25 11:01 logs
drwxr-xr-x 2 gabe gabe  4096 Sep 29 12:06 site-docs
$
```

- Extract and go to the folder
```
$ cd ~
$ tar -xzf kafka_2.13-3.3.1.tgz
$ cd kafka_2.13-3.3.1
$
```

- Start all services in the following order is important

- Start kafka with zookeeper.
  From one terminal, let's call it **"zookeeper terminal"**:
```
$ cd ~/kafka_2.13-3.3.1
$ bin/zookeeper-server-start.sh config/zookeeper.properties
[...]
```

- Start Kafka broker.
  From another terminal, let's call it **"kafka terminal"**
```
$ cd ~/kafka_2.13-3.3.1
$ bin/kafka-server-start.sh config/server.properties
[...]
```

- Now the Kafka broker service is running and ready to receive message 

- NEXT, add a topic, and start the consumer of the topic; see below.

## Kafka - Topic

To publish and consume messages, we need to create a topic.
Producer publishes a message to a topic.
Consumer reads the messages from the topic.

### Add a Topic

- Open a new terminal and let's call it "publisher terminal".

- Create a topic named `TestTopic`:
```
$ cd ~/kafka_2.13-3.3.1
$ bin/kafka-topics.sh --create --topic TestTopic --bootstrap-server localhost:9092
Created topic TestTopic.
$
```

### Run a consumer of the topic

- Open a new terminal and let's call it "consumer terminal".

- Run the consumer to read messages from `TestTopic`.
  Note the use of the `--from-beginning` flag, which allows
  the consumption of messages that were published before the consumer was started:
```
$ cd kafka_2.13-3.3.1
$ bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic TestTopic --from-beginning
Hello, Kafka
[...]
```

### Run a Producer of the topic

There are many mechanisms for publishing messages to Kafka including:
manual or streaming.

- For manual publish, go to the "Test - Manual Producer" section below
  - Using Kafka script
  - Python Tiny data producer (`tiny_data.py`)
  - Python Faker data (`faker_data.py`)

- Streaming, go to "TESTS - Streaming Producer" section below
  - FileBeat - run manually


### Delete a Topic

NOTE: make sure `delete.topic.enable` property is set to true in
the Kafka configuration.

```
$ ~/kafka_2.13-3.3.1
$ bin/kafka-topics.sh --delete --topic TestTopic --bootstrap-server localhost:9092
$
```


## TESTS - Manual Producer

### SETUP 

- Prerequisite:
  - Python environment.
    Note: linux (Ubuntu) comes with python pre-installed:
```
$ lsb_release -a
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 20.04.4 LTS
Release:        20.04
Codename:       focal

$ python --version
Python 3.8.10

$ pip --version
pip 20.0.2 from /usr/lib/python3/dist-packages/pip (python 3.8)
```

- Create Python virtual environment
```
$ cd [projects-dir]/infra-kafka
$ virtualenv ./.venv
created virtual environment CPython3.8.2.final.0-64 in 2710ms
  creator CPython3Posix(dest=/mnt/c/zWSL/projects/infra-kafka/.venv, clear=False, global=False)
  seeder FromAppData(download=False, pip=latest, setuptools=latest, wheel=latest, pkg_resources=latest, via=copy, app_data_dir=/home/gabe/.local/share/virtualenv/seed-app-data/v1.0.1.debian.1)
  activators BashActivator,CShellActivator,FishActivator,PowerShellActivator,PythonActivator,XonshActivator
$ source .venv/bin/activate
(.venv) $
```

- Make sure to perform **CLEANUP** when done; see CLEANUP section below.

### Using Kafka script

- From a new terminal, "producer terminal":
```
$ cd ~/kafka_2.13-3.3.1
$ echo "Hello, Kafka" | bin/kafka-console-producer.sh --broker-list localhost:9092 --topic TestTopic > /dev/null
$
```

- Go to the Kafka consumer terminal; should already be running
```
$ cd ~/kafka_2.13-3.3.1
$ bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic TestTopic --from-beginning
Hello, Kafka

```

### Python Tiny data producer (`tiny_data.py`)

Generate very tiny data streama using Python and send to
the Kafka `TestTopic` topic.

- Prerequisite:
  - Python environment.
  - Kafka broker is running
  - Kafka topic, `TestTopic`, has been added
  - Kafka consumer is running monitoring on the TestTopic`

- Install the python module, `kafka-python`
```
(.venv) $ cd [projects-dir]/infra-kafka
(.venv) $ pip install kafka-python
Collecting kafka-python
  Downloading kafka_python-2.0.2-py2.py3-none-any.whl (246 kB)
     |████████████████████████████████| 246 kB 2.9 MB/s 
Installing collected packages: kafka-python
Successfully installed kafka-python-2.0.2
```

- [Optional] customized the following parameters in the code:
  - The number of data points to generate, `no_of_data`; (default: 2)
  - Sleep time in between data generation, `sleep_time_sec`; (default: 3) 
  - Kafka topic name, `topic_name`; (default: TestTopic)

- Run the producer from a terminal, "producer terminal"
```
(.venv) $ cd [projects-dir]/infra-kafka
(.venv) $ python producers/tiny_data.py
{'number': 0}
{'number': 1}
exiting...
(.venv) $
```

- Go to the Kafka consumer terminal; should already be running
```
$ cd ~/kafka_2.13-3.3.1
$ bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic TestTopic --from-beginning

{"number": 0}
{"number": 1}
```

### Python Faker data (`faker_data.py`)

Generate "fake" customer data stream using Python and send to
the Kafka `TestTopic` topic.

- Prerequisite:
  - Python environment.
  - Kafka broker is running
  - Kafka topic, `TestTopic`, has been added
  - Kafka consumer is running monitoring on the TestTopic`

- Install the python module, ``
```
(.venv) $ cd [projects-dir]/infra-kafka
(.venv) $ pip install Faker
Collecting Faker
  Downloading Faker-15.1.1-py3-none-any.whl (1.6 MB)
     |████████████████████████████████| 1.6 MB 2.8 MB/s 
Collecting python-dateutil>=2.4
  Downloading python_dateutil-2.8.2-py2.py3-none-any.whl (247 kB)
     |████████████████████████████████| 247 kB 13.5 MB/s 
Collecting six>=1.5
  Downloading six-1.16.0-py2.py3-none-any.whl (11 kB)
Installing collected packages: six, python-dateutil, Faker
Successfully installed Faker-15.1.1 python-dateutil-2.8.2 six-1.16.0
```

- [Optional] customized the following parameters in the code:
  - The number of data points to generate, `no_of_data`; (default: 2)
  - Sleep time in between data generation, `sleep_time_sec`; (default: 3) 
  - Kafka topic name, `topic_name`; (default: TestTopic)

- Run the producer from a terminal, "producer terminal"
```
(.venv) $ cd [projects-dir]/infra-kafka
(.venv) $ python producers/faker_data.py
{'transaction_date': '2021-04-03', 'name': 'Kyle Simmons', 'gender': 'M', 'city': 'Kingborough', 'email': 'lamkristina@francis.org', 'product_id': '38718250', 'amount_spent': 99.2}
{'transaction_date': '2021-01-17', 'name': 'Jordan Smith', 'gender': 'M', 'city': 'Veronicastad', 'email': 'mcguireashley@gmail.com', 'product_id': '91409218', 'amount_spent': 33.47}
{'transaction_date': '2021-03-07', 'name': 'Michael Richardson', 'gender': 'M', 'city': 'Adamsmouth', 'email': 'pperez@spencer-porter.com', 'product_id': '84556660', 'amount_spent': 52.67}
exiting...
(.venv) $
```

- Go to the Kafka consumer terminal; should already be running.
  NOTE: the data value will not be the same because they are generated on demand.
```
$ cd ~/kafka_2.13-3.3.1
$ bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic TestTopic --from-beginning

"{\"transaction_date\": \"2021-04-03\", \"name\": \"Kyle Simmons\", \"gender\": \"M\", \"city\": \"Kingborough\", \"email\": \"lamkristina@francis.org\", \"product_id\": \"38718250\", \"amount_spent\": 99.2}"
"{\"transaction_date\": \"2021-01-17\", \"name\": \"Jordan Smith\", \"gender\": \"M\", \"city\": \"Veronicastad\", \"email\": \"mcguireashley@gmail.com\", \"product_id\": \"91409218\", \"amount_spent\": 33.47}"
"{\"transaction_date\": \"2021-03-07\", \"name\": \"Michael Richardson\", \"gender\": \"M\", \"city\": \"Adamsmouth\", \"email\": \"pperez@spencer-porter.com\", \"product_id\": \"84556660\", \"amount_spent\": 52.67}"
```


### CLEANUP

- Delete the Python virtual environment, if no longer needed.
```
$ cd [projects-dir]/infra-kafka
$ rm -r ./.venv 
```

- If no longer needed, terminate:
  - Kafka consumer from the "consumer terminal"
  - Kafka broker from the "kafka terminal"
  - Kafka zookeeper from the "zookeeper terminal"

## TESTS - Streaming Producer

### FileBeat - run manually

Website: https://www.elastic.co/guide/en/beats/filebeat/8.4/filebeat-overview.html

Filebeat is a lightweight shipper for forwarding and centralizing log data. 
Installed as an agent on your servers, Filebeat monitors the log files or locations 
that you specify, collects log events, and forwards them to Kafka or other broker.

There are several ways to collect log data with Filebeat:
- Data collection modules: simplify the collection, parsing, and visualization of common log formats
- ECS loggers: structure and format application logs into ECS-compatible JSON
- Manual Filebeat configuration

- Prerequisite:
  - Python environment.
  - Kafka broker is running
  - Kafka topic, `TestTopic`, has been added
  - Kafka consumer is running monitoring on the TestTopic

- Install FileBeat; assuming we are installing on the user's home folder.
```
$ cd ~
$ curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.4.3-linux-x86_64.tar.gz
$ tar xzvf filebeat-8.4.3-linux-x86_64.tar.gz
$ cd filebeat-8.4.3-linux-x86_64
```

- List all the available data collection modules.
```
$ cd ~/filebeat-8.4.3-linux-x86_64
$ ./filebeat modules list
Enabled:

Disabled:
activemq
apache
[...]
zookeeper
zoom
zscaler
```  

- Configure the FileBeat in the `filebeat-8.4.3-linux-x86_64/filebeat.yml`
  Docs:
  - [Configure input](https://www.elastic.co/guide/en/beats/filebeat/8.4/configuration-filebeat-options.html)
  - [Configure the Kafka output](https://www.elastic.co/guide/en/beats/filebeat/8.4/kafka-output.html)
```
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - <project-folder>/logs/dummy.log
output.kafka:
  codec.format:
    string: '%{[@timestamp]} %{[message]}'
  # initial brokers for reading cluster metadata
  hosts: ["localhost:9092"]
  # message topic selection + partitioning
  topic: TestTopic
  partition.round_robin:
    reachable_only: false
  required_acks: 1
  compression: gzip
  max_message_bytes: 1000000  
```

- Run Filebeat agent manually from a terminal, "producer terminal"
```
$ cd ~/filebeat-8.4.3-linux-x86_64
$ ./filebeat run
```
  
- Run the dummy python program to generate log file, `logs/dummy.log`,
  from a terminal, "logger terminal".
  NOTE: remember to activate the python virtual environment, if not already.
```
(.venv) $ cd [projects-dir]/infra-kafka
(.venv) $ mkdir logs
(.venv) $ python utils/gen_dummy_logs.py
press CTRL-C to stop...
sleep 5 sec...
sleep 5 sec...
[...]
```

- Go to the Kafka consumer terminal; should already be running
```
$ cd ~/kafka_2.13-3.3.1
$ bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic TestTopic --from-beginning

2022-10-25T21:24:07.968Z 2022-10-25 13:32:05,874 Harmless debug Message
2022-10-25T21:24:10.878Z 2022-10-25 13:32:05,875 Just an information
2022-10-25T21:24:10.878Z 2022-10-25 13:32:05,876 Its a Warning
2022-10-25T21:24:10.878Z 2022-10-25 13:32:05,876 Did you try to divide by zero
2022-10-25T21:24:10.879Z 2022-10-25 13:32:05,876 Internet is down
2022-10-25T21:24:10.879Z 2022-10-25 13:32:05,876 *************************************
2022-10-25T21:24:10.879Z 2022-10-25 13:32:10,882 Harmless debug Message
2022-10-25T21:24:10.880Z 2022-10-25 13:32:10,884 Just an information
2022-10-25T21:24:10.880Z 2022-10-25 13:32:10,885 Its a Warning
2022-10-25T21:24:10.880Z 2022-10-25 13:32:10,886 Did you try to divide by zero
2022-10-25T21:24:10.881Z 2022-10-25 13:32:10,888 Internet is down
2022-10-25T21:24:10.881Z 2022-10-25 13:32:10,889 *************************************
```

- When done, terminate:
  - the python program on "logger terminal"; 
  - the filebeat agent on the "producer terminal"


### CLEANUP

- Delete the Python virtual environment, if no longer needed.
```
$ cd [projects-dir]/infra-kafka
$ rm -r ./.venv 
```

- If no longer needed, terminate:
  - Kafka consumer from the "consumer terminal"
  - Kafka broker from the "kafka terminal"
  - Kafka zookeeper from the "zookeeper terminal"
  

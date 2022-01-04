# PySparkML_20211

## Docker compose

To host spark cluster, elasticsearch, rabbitmq, kibana

```bash
cd cluster
docker-compose up -d
```

### Install Python Lib

```sh
conda activate 'your environment'
pip install -r requirements.txt
```

## Datasource

### Crawl reviews Amazon Web using scrapy

```sh
mkdir -p data/
cd amazon-python-scrapy-scraper
scrapy crawl amazon -o ../data/reviews.csv
```

## How to build spark cluster

### Quick Start

To deploy an the HDFS-Spark-Hive cluster, run:

```
cd docker-hadoop-spark
docker-compose up -d
```

- Namenode: http://<dockerhadoop_IP_address>:9870/dfshealth.html#tab-overview
- History server: http://<dockerhadoop_IP_address>:8188/applicationhistory
- Datanode 1: http://<dockerhadoop_IP_address>:9864/
- Datanode 2: http://<dockerhadoop_IP_address>:9865/
- Datanode 3: http://<dockerhadoop_IP_address>:9866/
- Nodemanager: http://<dockerhadoop_IP_address>:8042/node
- Resource manager: http://<dockerhadoop_IP_address>:8088/
- Spark master: http://<dockerhadoop_IP_address>:8080/
- Spark worker 1: http://<dockerhadoop_IP_address>:8081/
- Spark worker 2: http://<dockerhadoop_IP_address>:8082/
- Spark worker 3: http://<dockerhadoop_IP_address>:8083/
- Spark worker 4: http://<dockerhadoop_IP_address>:8084/
- Hive: http://<dockerhadoop_IP_address>:10000

Go to the bash shell on the namenode with that same Container ID of the namenode.

```
  docker exec -it namenode bash
```

Create a HDFS directory /data/input/.

```
  hdfs dfs -mkdir -p /data/input
  hdfs dfs -put /mnt/reviews_1.json
```

## Crawl using nodejs

```bash
# step 1
cd Crawl/amazon-js
# step 2
npm install
# step 3
node crawl.js
```

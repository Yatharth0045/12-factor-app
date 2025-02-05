## Microservice using 12 factor

### Codebase
Using git to store and collaborate
Each microservice should use separate codebase

### Dependency
Dependencies should be installed separately
```bash
pip install -r requirements.txt
```

Should be isolated for each project
```bash
## Create virtual environment
python -m venv .venv

## Activate virtual environment
source .venv/bin/activate 
```

Can use docker for system wide dependencies
```bash
## Build docker
docker build -t my-app .

## Run docker
docker run -p 8080:8080 --name microservice my-app
```

### Concurrency

Can be achieved via Scaling
- Requires application to be stateless

### Processes
Service should be stateless and should share nothing 

Eg: Storing visitor count

### Backing services
Run Redis
```bash
docker run -d --name redis -p 6379:6379 redis/redis-stack-server:latest
```

Run application with connection to redis
```bash
docker run -p 8080:8080 --link redis --name microservice my-app
```

### Config
Hard coded configs should be avoided. Pass them via ENV
```bash
## Run app via docker
## modify .env
docker run -p 8080:8080 --env-file .env --link redis my-app

## Run app locally
## modify .env
python app.py
```

### Build Release Run

- Build
    - Adding code
    - Containerize
- Release
    - Image
    - .env
- Run
    - Run Image specific to env

### Port mapping
Exposing application via some port.
Does not rely on runtime injection of a webserver into the execution environment to create a web-facing service.

### Disposable
Can be started or stopped without any notice.
- Process should work on minimizing startup time
- Can be started and stopped as per requirement (load) - Horizontal scaling
- Should shut down gracefully when receive SIGTERM signal.
    - SIGTERM
    - SIGKILL

### Dev Prod Parity
dev == staging == prod

CICD helps in here

### Logs
Store logs via some mechanism.
Used for troubleshooting issues.

Approaches
- Store logs in file locally
- Push logs to certain logging system - Fluentd

- All logs should be written to STDOUT | STDERR
- Can be then collected via an agent
    - Fluentd
    - ELK
    - Splunk

```bash
## Build fluentd image with elasticsearch plugin enabled
cd fluentd
docker build -t fluentd .
cd ..

## Create fluentd conf
cat << EOF > fluentd/fluent.conf
<source>
  @type forward
  port 24224
</source>

<match **>
  @type elasticsearch
  host elasticsearch
  port 9200
  logstash_format true
  index_name fluentd-logs
  type_name _doc
  include_tag_key true
  tag_key @log_name
</match>

<match **>
  @type stdout
</match>
EOF

## Run elasticsearch
docker run -d --name elasticsearch \
  -p 9200:9200 -e "discovery.type=single-node" \
  docker.elastic.co/elasticsearch/elasticsearch:7.17.0

## Run kibana
docker run -d --name kibana \
  --link elasticsearch \
  -p 5601:5601 \
  -e ELASTICSEARCH_HOSTS="http://elasticsearch:9200" \
  docker.elastic.co/kibana/kibana:7.17.0

## Run fluentd
docker run -d --name fluentd \
  --link elasticsearch \
  -p 24224:24224 \
  -v $(pwd)/fluentd/fluent.conf:/fluentd/etc/fluent.conf \
  fluentd

## Run app container
docker run -p 8080:8080 --log-driver=fluentd --log-opt fluentd-address=localhost:24224 --name microservice --env-file .env --link redis my-app
```
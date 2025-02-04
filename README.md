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
docker run -p 8080:8080 my-app 
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
docker run -p 8080:8080 --link redis my-app
```
## Benchmark for python by computing Monte Carlo estimates of pi

### Python/Flask application

Project structure:
```
.
├── Dockerfile
├── requirements.txt
├── app
    └── main.py

```

## Deploy with docker

```
docker run -dp 8000:8000 karl8080/pitest
```

## Expected result

Listing containers must show one container running and the port mapping as below:
```
$ docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS         PORTS                    NAMES
78e6c069e2f3   pitest    "flask --app app.mai…"   7 seconds ago   Up 4 seconds   0.0.0.0:8000->8000/tcp   optimistic_meninsky
```

After the application starts, navigate to `http://localhost:8000` in your web browser or run:
```
$ curl localhost:8000
Total: 400000 In: 314335.
Pi: 3.14335.
Elapsed time: 0.08 seconds.
```

Change parallel computing and number of sample for each thread, default setting is 4 threads, 100000 samples. Change web address to `http://localhost:8000/?procs=2&iters=200000`. Now it runs in 2 threads and each thread with 200000 samples.
```
Total: 400000 In: 314015.
Pi: 3.14015.
Elapsed time: 0.13 seconds.
```

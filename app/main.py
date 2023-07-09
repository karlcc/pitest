import multiprocessing
from flask import Flask, request, jsonify
import time
from random import random

app = Flask(__name__)

@app.route("/")
def index():
    return "App of computing Monte Carlo estimates of pi"

@app.route('/api')
@app.route('/api/')
@app.route("/api/<int:num>")
def pi(num=int(1E+5)):
    max_procs = multiprocessing.cpu_count()
    procs = min(int(request.args.get('procs', 4)), max_procs)
    iters = num // procs

    start_time = time.time()

    runtest = TestMC(procs, iters)
    result = runtest.test_mc()

    elapsed_time = time.time() - start_time
    strelapsed_time = f"{elapsed_time * 1000:.{0}f} ms"

    piout, total_in, total = result
    output = {
        "pi": piout,
        "total_in": total_in,
        "total": total,
        "time": strelapsed_time,
        "threads": procs,
    }

    return jsonify(output)


def calculate_pi(iters):
    """ Worker function """
    points = 0  # points inside circle

    for _ in range(iters):
        x = random()
        y = random()

        if x ** 2 + y ** 2 <= 1:
            points += 1

    return points


class TestMC:
    def __init__(self, procs, iters):
        self.procs = procs
        self.iters = iters

    def test_mc(self):
        with multiprocessing.Pool(processes=self.procs) as pool:
            results = pool.map(calculate_pi, [self.iters] * self.procs)
            total_in = sum(results)
            total = self.iters * self.procs
            piout = 4.0 * total_in / total

        return piout, total_in, total


if __name__ == '__main__':
    app.run(threaded=True)
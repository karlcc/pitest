from flask import Flask, request
import concurrent.futures
import time
from random import random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    procs = int(request.args.get('procs', 4))
    iters = int(request.args.get('iters', 1E+5))

    start_time = time.time()

    runtest = TestMC(procs, iters)
    result = runtest.test_mc()

    elapsed_time = time.time() - start_time
    strelapsed_time = f"{elapsed_time:.{2}f} seconds"

    piout, total_in, total = result

    return f"Total: {total} In: {total_in}.<br>Pi: {piout}.<br>Elapsed time: {strelapsed_time}."


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
        with concurrent.futures.ProcessPoolExecutor(max_workers=self.procs) as executor:
            total = self.iters * self.procs
            total_in = sum(executor.map(calculate_pi, [self.iters] * self.procs))
            piout = 4.0 * total_in / total

        return piout, total_in, total


if __name__ == '__main__':
    app.run(threaded=True)
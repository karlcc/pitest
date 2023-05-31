from flask import Flask, request
from random import random
import time
from multiprocessing import Pool

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    getprocs = request.args.get('procs')
    getiters = request.args.get('iters')
    if getprocs:
        procs = int(getprocs)
    else:
        procs = 4
    if getiters:
        iters = int(getiters)
    else:
        iters = int(1E+5)  # 1E+8 is cool

    start_time = time.time()

    runtest = TestMC(procs,iters)
    result = runtest.test_mc()

    elapsed_time = time.time() - start_time
    strelapsed_time = f"{elapsed_time:.{2}f} seconds"
    
    piout = str(result[0])
    total_in = str(result[1])
    total = str(result[2])

    return f"Total: {total} In: {total_in}.<br>Pi: {piout}.<br>Elapsed time: {strelapsed_time}."


def calculate_pi(iters):
    """ Worker function """

    points = 0  # points inside circle

    for i in range(iters):
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
        p = Pool(processes=self.procs)

        total = self.iters * self.procs
        total_in = 0

        for points in p.map(calculate_pi, [self.iters] * self.procs):
            total_in += points

        #print ("Total: ", total, "In: ", total_in)
        #print ("Pi: ", piout)
        piout = 4.0 * total_in / total
           
        return piout, total_in, total

if __name__ == '__main__':
    app.run()
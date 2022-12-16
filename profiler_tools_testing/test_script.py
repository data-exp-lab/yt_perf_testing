# generic test script
# python test_script.py
# gprof2dot -f pstats output.pstats | dot -Tpng -o output.png
# or to get a pdf
# gprof2dot -f pstats output.pstats | dot -Tpdf -o output.pdf

from profilehooks import profile
from time import sleep
import random 

def profile_wrapped_function(output_filename):

    @profile(filename=output_filename, profiler="cProfile")
    def sleep_cycles(x):
        first_sleep()
        not_so_sleepy()
        second_sleep(x)

    return sleep_cycles


def not_so_sleepy():
    it = 0 
    max_its = 1000000
    while it < max_its:
        if random.random() > .9999:
            it = max_its + 1
        it+=1
        

def first_sleep():
    sleep(0.2)

def second_sleep(x):
    sleep(x)

@profile(filename="output.pstats", profiler="cProfile")
def func1(x: float):
    first_sleep()
    second_sleep(x)

if __name__ == "__main__":
    
    for it in range(3):
        func1(1.)

    sleep_cycles = profile_wrapped_function('morestats.pstats')
    for it in range(3):
        sleep_cycles(1.)



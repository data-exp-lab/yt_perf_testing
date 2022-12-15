just a test directory for trying out different profiling tools 


To try out `profilehooks` and `gprof2dot`: 

```
$ pip install profilehooks graphviz gprof2dot
$ python test_script.py
$ gprof2dot -f pstats output.pstats | dot -Tpng -o output.png
```


`test_script.py` shows how to output profile stats to different files for different functions.

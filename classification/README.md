# Luigi Pipeline
Luigi pipeline for data preprocessing, classification and evaluation.
Luigi handles dependency resolution, workflow management and visualization of executed tasks.
[Luigi Documentation](https://luigi.readthedocs.io/en/latest/index.html)

### Run pipeline
run pipeline in combination with luigidaemon (webinterface)
webinterface is available on localhost:8082  
start luigi daemon  
`$ luigid`  
run luigi pipeline  
`$ python3 -m luigi --module Evaluator Evaluator --scheduler-host localhost`  

run pipeline with local scheduler (no webinterface)  
`$ python3 -m luigi --module Evaluator Evaluator --local-scheduler`  


# Start luigi pipelines
Luigi pipelines can be started with the shell-script: start_pipelines.sh  
The script starts for each config in _./configs/Configurations.py_ one independent pipeline in parallel.
The script needs as argument the end of all pipelines (i.e. DataVisualizer or MLClassifiers).

execute shell-script with _MLClassifiers.py_ as end:
`
./start_pipelines.sh MLClassifiers 
`


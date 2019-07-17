# Start luigi pipelines
Luigi pipelines can be started with the shell-script: start_pipelines.sh  
The script starts for each config in _./configs/Configurations.py_ one independent pipeline in parallel.
The script needs as argument the end of all pipelines (i.e. DataVisualizer or MLClassifiers).

execute shell-script with _MLClassifiers.py_ as end:
`
./start_pipelines.sh MLClassifiers 
`

# Starten von mehreren Luigi Pipelines
Mit dem Shell-script "start_pipelines.sh" können mehrere Pipelines auf einmal gestartet werden.
Für jede Konfiguration in "./configs/Configurations.py" wird eine unabhängige Pipeline parallel gestartet.
Das Shell-script benötigt als Argument das Ende aller Pipelines (z.B. DataVisualizer.py oder MLCLassifiers.py).

Shell-script mit Ende _MLClassifiers.py_ starten:
`
./start_pipelines.sh MLClassifiers 
`
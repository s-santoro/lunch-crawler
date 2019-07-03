# Start production pipeline
The production pipeline reads all webpage files from folder "./input" into memory.
Then does preprocessing of specified content according to config file.
The final task is to classify each file and move it either to folder "./output/menu" or "./output/no_menu".

To start the production pipeline execute the bash-script "start_pipeline.sh" with following command:
`./start_pipeline.sh`

_IMPORTANT:_ Before starting pipeline, make sure to download pickle-files from dropbox and place them in "./pickled_files/".
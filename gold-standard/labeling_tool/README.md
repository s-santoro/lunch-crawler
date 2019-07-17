# testdata_tool
Tool to improve manual labelling of test data.  
The tool reads json-files inside `./files` and shows their respective HTML content.  
After pressing the correct label key, the file is copied into the corresponding folder:
- Key "a" => `./files/pos_menu`
- Key "space" => `./files/pos_daily_menu`
- Key "d" => `.files/neg`


In order to use the tool, npm is needed.

Install all dependencies inside package.json with `npm install`.  
Start the app with `npm start`.

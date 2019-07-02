// Imports
const fs = require('fs');

// Read OSM JSON
var osmData = require('./OSM_Data_raw.json')
console.log(settings)

// Read LunchCard CSV

var fileContent;

new Promise(function(resolve) {
    fileContent = fs.readFileSync(path, {encoding: 'utf8'});
    resolve(fileContent);
});

console.log(fileContent);


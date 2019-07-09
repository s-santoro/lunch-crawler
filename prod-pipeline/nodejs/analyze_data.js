// Imports
const fs = require('fs');
const path = require('path');
const csv = require("csvjson");

// Data Import
let standardizedData = require('./standardized_data.json');
let osmData = require('./OSM_Data_raw.json');
let lcData = csv.toObject(fs.readFileSync(path.join(__dirname, './lc-card-data.csv'), { encoding : 'utf8'}));
let classifiedData = readClassifiedData();

let menuData = analyzeStandardizedDataForMappedURL(standardizedData);
writeToOutput(writeDatawithGeolocationAndURL(standardizedData))

console.log("Amount of Openstreetmap Data with Geolocation and Website:         "+analyzeOSMData(osmData));
console.log("Amount of Lunch Check Data with Website:                           "+analyzeLCData(lcData));
console.log("Amount of merged Data (OSM and Lunch Check):                       "+standardizedData.length);
console.log("Amount of Restaurants with Geolocation and mapped Menü-Webpage:    "+analyzeStandardizedData(standardizedData));
console.log("Amount of Restaurants with 1 mapped Menü-Webpage:                  "+ menuData[0]);
console.log("Amount of Restaurants with 2-5 mapped Menü-Webpage:                "+ menuData[1]);
console.log("Amount of Restaurants with 5-9 mapped Menü-Webpage:                "+ menuData[2]);
console.log("Amount of Restaurants with 10 or more mapped Menü-Webpage:         "+ menuData[3]);
console.log("Amount of classified Menü-Webpages:                                "+classifiedData.length);



// Read multiple JSON files from Subfolder and write them to Array
function readClassifiedData(){
    let data = [];
    const directoryPath = path.join(__dirname, 'menu');
    let files = fs.readdirSync(directoryPath);
    files.forEach( function (filename) {
        file = JSON.parse(fs.readFileSync(path.join(directoryPath, filename), { encoding : 'utf8'}))
        let obj = {
            "url": file.url,
            "text": file.text
        }
        data.push(obj); 
    });
    return data;
}

function analyzeOSMData(osmData){
    let counter = 0;
    for(i in osmData){
        if(osmData[i].tags!=undefined && osmData[i].tags.website!=undefined && osmData[i].lat!=undefined && osmData[i].lon!=undefined){
            counter++;
        }
    }
    return counter
}

function analyzeLCData(lcData){
    let counter = 0;
    for(i in lcData){
        if(lcData[i].Website!=""){
            counter++;
        }
    }
    return counter
}

function analyzeStandardizedData(data){
    let counter = 0;
    for(i in data){
        if(data[i].lat!=null&&data[i].menuURL.length!=0){
            counter++;
        }
    }
    return counter;
}
function writeDatawithGeolocationAndURL(data){
    let outputdata = []
    for(i in data){
        if(data[i].lat!=null&&data[i].menuURL.length!=0){
            outputdata.push(data[i]);
        }
    }
    return outputdata
}

function analyzeStandardizedDataForMappedURL(data){
    let oneCounter  = 0;
    let twoCounter  = 0;
    let fifeCounter = 0;
    let tenCounter  = 0;
    for(i in data){
        if(data[i].lat!=null&&data[i].menuURL.length!=0){
            if(data[i].menuURL.length>=10){
                tenCounter++;
            }
            else if(data[i].menuURL.length>=5){
                fifeCounter++;
            }
            else if(data[i].menuURL.length>=2){
                twoCounter++;
            }
            else if(data[i].menuURL.length>=1){
                oneCounter++;
            }
        }
    }
    return [oneCounter, twoCounter, fifeCounter, tenCounter];
}

// Writes Array to JSON File
function writeToOutput(data){
    fs.writeFile('./relevant_only.json', JSON.stringify(data), (err)=>{
        if (err) throw err;
        console.log("DATA WRITTEN TO FILE");
    })
}
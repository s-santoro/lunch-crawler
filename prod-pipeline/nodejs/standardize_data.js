// Imports
const fs = require('fs');
const csv = require("csvjson");
const path = require('path');
const psl = require('psl');
const request = require('sync-request');

// Data Import
// OSM Data:        Same Folder as Script, Name: "OSM_Data_raw.json"
// LC Data:         Same Folder as Script, Name: "lc-card-data.csv"
// Classified Data: Files in Subfolder called "menu"
let osmData = require('./OSM_Data_raw.json');
let lcData = csv.toObject(fs.readFileSync(path.join(__dirname, './lc-card-data.csv'), { encoding : 'utf8'}));
let classifiedData = readClassifiedData();

// Data Cleanup
let cleanOSMData = clearOSMData(osmData);
let cleanlcData = clearLCData(lcData, cleanOSMData);
let mergedData = cleanOSMData.concat(cleanlcData);
let finalData = matchData(classifiedData, mergedData);

writeToOutput(finalData);


// Match URL of classiefied Data to Homepage-URL of Data from OSM & Lunch Check
function matchData(classifiedData, mergedData){
    for(var i in classifiedData){
        for(var j in mergedData){
            if(psl.get(extractHostname(classifiedData[i].url)) == mergedData[j].homepage){
                mergedData[j].menuURL.push(classifiedData[i].url);
                mergedData[j].text.push(classifiedData[i].text);
                break;
            }
        }
    }
    return mergedData;
}

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

// Read OSM Data and rewrite them in standardized way to an array
function clearOSMData(osmData){
    let data = [];
    for(let i = 0; i < osmData.length; i++) {
        let osmObj = osmData[i];
        // Only write Objects with Website 
        if(osmObj.tags!=undefined && osmObj.tags.website!=undefined && osmObj.lat!=undefined && osmObj.lon!=undefined){
            let obj = {
                "name": osmObj.tags.name,
                "homepage": psl.get(extractHostname(osmObj.tags.website)),
                "lat": osmObj.lat,
                "lon": osmObj.lon,
                "address": "",
                "city": "",
                "menuURL": [],
                "text": []
            };
            data.push(obj);
        }
    }
    return data;
}

// Read Lunch Check Data, get the Geolocation and rewrite them in standardized way to an array
function clearLCData(lcData, osmData){
    let data = []
    for(let i = 0; i < lcData.length; i++) {
        let lcObj = lcData[i];
        // Check if Data already exist from OSM
        let objChecker = osmData.find(obj => obj.homepage == psl.get(extractHostname(lcObj.Website)));    
        if(objChecker==undefined){
            // No empty URL
            if(lcObj.Website!=""){
                let geodata;
                if(lcObj.Adresse!=undefined && lcObj.Ort!=undefined){
                    geodata = syncGetLocation(lcObj.Adresse, lcObj.Ort);
                }
                if(geodata==null){
                    geodata = [null, null];
                }
                //console.log(geodata)
                let obj = {
                    "name": lcObj.Restaurant,
                    "homepage": psl.get(extractHostname(lcObj.Website)),
                    "lat": parseFloat(geodata[0]),
                    "lon": parseFloat(geodata[1]),
                    "address": lcObj.Adresse,
                    "city": lcObj.Ort,
                    "menuURL": [],
                    "text": []
                }
                data.push(obj);
            }
        }    
    }
    return data;
}

// Extracts Hostname out of URL
function extractHostname(url) {
    var hostname;
    //find & remove protocol (http, ftp, etc.) and get hostname
    if(url!=null){
        if (url.indexOf("//") > -1) {
                hostname = url.split('/')[2];
            }
            else {
                hostname = url.split('/')[0];
            }
            //find & remove port number
            hostname = hostname.split(':')[0];
            //find & remove "?"
            hostname = hostname.split('?')[0];
            return hostname;
    }else{
        return null;
    }
    
}

// Writes Array to JSON File
function writeToOutput(data){
    fs.writeFile('./output.json', JSON.stringify(data), (err)=>{
        if (err) throw err;
        console.log("DATA WRITTEN TO FILE");
    })
}

// Requests Geolocation from local version of "Nominatim" 
function syncGetLocation(address, city){
    let url = "http://localhost:7070/search?street="+ address +"&city="+ city +"&format=json"
    url = encodeURI(url);
    let res = request('GET', url, {
    headers: {
        'user-agent': 'der Don'
    },
    });
    let object = JSON.parse(res.getBody('utf8'))
    if(object[0]!=undefined){
        if(object[0].lat!=undefined && object[0].lon!=undefined){
            return [object[0].lat, object[0].lon]
        }
        else{
            return null
        }
    }
    else{
        return null
    }
}


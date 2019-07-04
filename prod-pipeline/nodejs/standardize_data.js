// Imports
const fs = require('fs');
const csv = require("csvjson");
const path = require('path');
const psl = require('psl');
const fetch = require("node-fetch");

// Data Import and Cleanup
let osmData = require('./OSM_Data_raw.json');
let lsData = csv.toObject(fs.readFileSync(path.join(__dirname, 'lc-card-data.csv'), { encoding : 'utf8'}));
let cleanOSMData = clearOSMData(osmData);
let cleanlcData = clearLCData(lsData, cleanOSMData);
let mergedData = cleanOSMData.concat(cleanlcData);
writeToOutput(mergedData);

// Add OSM Data with URL to shared array
function clearOSMData(osmData){
    let data = [];
    for(let i = 0; i < osmData.length; i++) {
        let osmObj = osmData[i];
        if(osmObj.tags!=undefined && osmObj.tags.website!=undefined){
            let obj = {
                "name": osmObj.tags.name,
                "homepage": psl.get(extractHostname(osmObj.tags.website)),
                "lat": osmObj.lat,
                "lon": osmObj.lon,
                "Adress": "",
                "City": "",
                "menuURL": "",
                "text": ""
            };
            data.push(obj);
        }
    }
    return data;
}

function clearLCData(lcData, osmData){
    let data = []
    for(let i = 0; i < lcData.length; i++) {
        let lcObj = lcData[i];
        // Check if Data already exist from OSM
        let exists = false;
        for(let j = 0; j < osmData.length; j++){
            if(psl.get(extractHostname(lcObj.Website)) == psl.get(extractHostname(osmData[j].homepage)) && !undefined){
                exists = true;
            }
        }    
        if(!exists){
            // No empty URL
            if(lcObj.Website!=""){
                for(key in lcObj){
                    //console.log(lcObj[key]);
                    //console.log(typeof(key));     
                }
                //console.log(Object.keys(lcObj));
                //console.log(lcObj)
                let obj = {
                    "name": lcObj.Restaurant,
                    "homepage": lcObj.Website,
                    "lat": "",
                    "lon": "",
                    "Adress": lcObj.Adresse,
                    "City": lcObj.Ort,
                    "menuURL": "",
                    "text": ""
                }
                console.log(obj)
                data.push(obj);
            }
        }    
    }
    return data;
}

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

function writeToOutput(data){
    fs.writeFile('./output.json', JSON.stringify(data), (err)=>{
        if (err) throw err;
        console.log("DATA WRITTEN TO FILE");
    })
}

async function getGeolocation(address, city){
    let url = "https://eu1.locationiq.com/v1/search.php?key=e4dcb73bab907f&state=Switzerland&city="+ city +"&street="+ address +"&format=json"
    fetch(url)
    .then(function(response) {
        return response.json();
    })
    .then(function(myJson) {
        var string = JSON.stringify(myJson);
        var objectValue = JSON.parse(string);
        //console.log([objectValue[0].lat, objectValue[0].lon]);
        return [objectValue[0].lat, objectValue[0].lon];
    }).catch(error => console.error('Error:', error));
}


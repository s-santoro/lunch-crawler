const fs = require("fs");
// log all files in ./files/
let files = [];
let fileCounter = 0;
if (files.length === 0) {
  fs.readdir(`${__dirname}/files/`, {}, (err, filesTemp) => {
    if (err) throw err;
    files = filesTemp;

    if (`${__dirname}/files/${files[fileCounter]}`.includes("DS_Store")) {
      console.log("DS_STORE");
      fileCounter++;
    }
    fs.readFile(
      `${__dirname}/files/${files[fileCounter]}`,
      "utf-8",
      (err, data) => {
        if (err) throw err;
        console.log(`${files[fileCounter]}`);
        let json = JSON.parse(data);
        let html = json.content;
        let frame = document.getElementById("frame").contentWindow.document;
        frame.open();
        frame.write(html);
        frame.close();
        document.getElementById("text").innerText = json.text;
        document.getElementById("title").innerText = json.url;
      }
    );
    fs.mkdir(`${__dirname}/files/pos_menu`, err => {
      if (err) throw err;
    });
    fs.mkdir(`${__dirname}/files/neg`, err => {
      if (err) throw err;
    });
    fs.mkdir(`${__dirname}/files/pos_daily_menu`, err => {
      if (err) throw err;
    });
  });
}

//const yes_menu = document.getElementById('yes');
//const no = document.getElementById('no');
//const yes_daily_menu = document.getElementById('link');

document.addEventListener(
  "keydown",
  event => {
    const keyName = event.key;

    if (keyName === "a") {
      console.log("pos_menu");
      pos_menu();
    }
    if (keyName === "d") {
      console.log("neg");
      neg();
    }
    if (keyName === " ") {
      console.log("pos_daily_menu");
      pos_daily_menu();
    }
  },
  false
);

function pos_menu() {
  // copy file to pos-folder
  fs.rename(
    `${__dirname}/files/${files[fileCounter]}`,
    `${__dirname}/files/pos_menu/${files[fileCounter]}`,
    err => {
      if (err) throw err;
      console.log("copied to pos_menu");
    }
  );
  if (fileCounter < files.length) {
    fileCounter++;
    // load next file
    fs.readFile(
      `${__dirname}/files/${files[fileCounter]}`,
      "utf-8",
      (err, data) => {
        if (err) throw err;
        let json = JSON.parse(data);
        let html = json.content;
        let doc = document.getElementById("frame").contentWindow.document;
        doc.open();
        doc.write(html);
        doc.close();
        document.getElementById("text").innerText = json.text;
        document.getElementById("title").innerText = json.url;
      }
    );
  } else {
    alert("all files checked");
  }
}

function neg() {
  // copy file to neg-folder
  fs.rename(
    `${__dirname}/files/${files[fileCounter]}`,
    `${__dirname}/files/neg/${files[fileCounter]}`,
    err => {
      if (err) throw err;
      console.log("copied to neg");
    }
  );
  if (fileCounter < files.length) {
    fileCounter++;
    // load next file
    fs.readFile(
      `${__dirname}/files/${files[fileCounter]}`,
      "utf-8",
      (err, data) => {
        if (err) throw err;
        let json = JSON.parse(data);
        let html = json.content;
        let doc = document.getElementById("frame").contentWindow.document;
        doc.open();
        doc.write(html);
        doc.close();
        document.getElementById("text").innerText = json.text;
        document.getElementById("title").innerText = json.url;
      }
    );
  } else {
    alert("all files checked");
  }
}

function pos_daily_menu() {
  // copy file to neg-folder
  fs.rename(
    `${__dirname}/files/${files[fileCounter]}`,
    `${__dirname}/files/pos_daily_menu/${files[fileCounter]}`,
    err => {
      if (err) throw err;
      console.log("copied to pos_daily_menu");
    }
  );
  if (fileCounter < files.length) {
    fileCounter++;
    // load next file
    fs.readFile(
      `${__dirname}/files/${files[fileCounter]}`,
      "utf-8",
      (err, data) => {
        if (err) throw err;
        let json = JSON.parse(data);
        let html = json.content;
        let doc = document.getElementById("frame").contentWindow.document;
        doc.open();
        doc.write(html);
        doc.close();
        document.getElementById("text").innerText = json.text;
        document.getElementById("title").innerText = json.url;
      }
    );
  } else {
    alert("all files checked");
  }
}

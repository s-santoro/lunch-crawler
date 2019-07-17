const electron = require('electron');
const url = require('url');
const path = require('path');

const {app, BrowserWindow, Menu, dialog} = electron;
let mainWindow;

// listen for app to be ready
app.on('ready', () => {
    // create new window
    mainWindow = new BrowserWindow({});

    // open dev tools
    mainWindow.webContents.openDevTools();
    // load html into window
    mainWindow.loadURL(url.format({
        pathname: path.join(__dirname, 'mainWindow.html'),
        protocol: 'file',
        slashes: true
    }));

    // build menu from template
    const mainMenu = Menu.buildFromTemplate(template);
    // insert menu
    Menu.setApplicationMenu(mainMenu);
})

// create menu template
const template = [];
  
  if (process.platform === 'darwin') {
    template.unshift({
      label: app.getName(),
      submenu: [
        { role: 'about' },
        { type: 'separator' },
        { role: 'services' },
        { type: 'separator' },
        { role: 'hide' },
        { role: 'hideothers' },
        { role: 'unhide' },
        { type: 'separator' },
        { role: 'quit' }
      ]
    })
}

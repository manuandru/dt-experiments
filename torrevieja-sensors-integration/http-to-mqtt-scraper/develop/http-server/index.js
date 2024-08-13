const express = require('express');
const path = require('path');

const app = express();

const endpoints = ["buoy", "counter_indoor", "depth", "satellite", "sonometer", "weather"];

for (let endpoint of endpoints) {
    app.get(`/${endpoint}`, (_, res) => {
        const filePath = path.join(__dirname, `example-sensors-data/${endpoint}.json`);
        res.sendFile(filePath);
    });
}

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});

process.on('SIGTERM', () => {
    process.exit(0);
});

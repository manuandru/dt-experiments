const express = require('express');
const axios = require('axios');
const https = require('https');

const app = express();
const port = 3000;

app.use(express.json());

const honoUrl = process.env.HONO_URL || 'https://localhost:8443/telemetry';

app.post('/telemetry', (req, res) => {

    console.log('Data: ', req.body);

    axios.post(honoUrl, req.body, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': req.headers.authorization
        },
        httpsAgent: new https.Agent({
            rejectUnauthorized: false
        }),
    })
    .then((response) => {
        console.log(`statusCode: ${response.status}`);
        res.status(response.status).send(response.data);
    })
    .catch((error) => {
        console.error(error);
        res.status(500).send(error);
    });

});

app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});

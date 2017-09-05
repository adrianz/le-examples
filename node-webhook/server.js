const express = require('express');
const app = express();
const bodyParser = require('body-parser');

app.use(bodyParser.json());

var counter = 0;

app.post('/webhook/analytics', function (req, res) {
    var reqId = req.get('X-Request-ID');
    var typeHeader = req.get('type');
    // Manager ID of a manager associated with the API key
    // used to initiate a webhook
    const manId = 'yourManagerIDGoesHere';
    
    // First case is responsible for negotiating a webhook
    if (typeHeader === 'SUBSCRIPTION_CONFIRMATION' ) {
        console.log(counter + '. Request ID: ' + reqId);
        res.json({
            managerId: manId,
            requestId: reqId
        });
    // Second case handles actual Presence data
    } else if (typeHeader === 'DATA') {
        // Response for Presence data requests has to
        // use status code 202
        res.status(202).end();
        // In this sample we just count a number of Presence
        // objects but in actual solutions the data from req.body
        // is processed and analysed
        console.log(counter + '. Presence objects count: ' + req.body.length);
    }
    
    counter++;
});

app.listen(3000, function () {
    console.log('Webhook handler listening on local port 3000!');
});
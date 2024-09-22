const { app } = require('@azure/functions');

// Import your functions
const uploadFileToBlob = require('./uploadFileToBlob');
const httpTest = require('../../HttpTest/index');

// Register your functions
app.http('uploadFileToBlob', {
    methods: ['POST'],
    authLevel: 'function',
    handler: uploadFileToBlob
});

app.http('HttpTest', {
    methods: ['GET', 'POST'],
    authLevel: 'anonymous',
    handler: httpTest
});

module.exports = app;

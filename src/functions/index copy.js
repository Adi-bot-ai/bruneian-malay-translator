const { app } = require('@azure/functions');

const httpTrigger = require('./functions/HttpExample');
const uploadFileToBlob = require('./functions/uploadFileToBlob');

module.exports = app;

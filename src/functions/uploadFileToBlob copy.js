const { BlobServiceClient } = require('@azure/storage-blob');
const { exec } = require('child_process'); // To call Python script

module.exports = async function (context, req) {
    context.log(`Processing request for URL "${req.url}"`);

    const AZURE_STORAGE_CONNECTION_STRING = process.env.AZURE_STORAGE_CONNECTION_STRING;

    if (!AZURE_STORAGE_CONNECTION_STRING) {
        context.res = {
            status: 500,
            body: "Azure Storage connection string is missing."
        };
        return;
    }

    // Check if a file is uploaded
    if (!req.body || !req.headers['content-type']) {
        context.res = {
            status: 400,
            body: "No file uploaded."
        };
        return;
    }

    // Parse the file and upload it to Azure Blob Storage
    const blobServiceClient = BlobServiceClient.fromConnectionString(AZURE_STORAGE_CONNECTION_STRING);
    const containerClient = blobServiceClient.getContainerClient('fileuploads');
    const blockBlobClient = containerClient.getBlockBlobClient('uploaded-file.pdf');

    try {
        // Upload the file to Azure Blob Storage
        await blockBlobClient.upload(req.body, req.body.length);

        // Call Python script for PDF extraction and translation using Docling
        exec('python docling_integration.py', (error, stdout, stderr) => {
            if (error) {
                context.res = {
                    status: 500,
                    body: `File processing failed: ${error.message}`
                };
                return;
            }

            context.res = {
                status: 200,
                body: `File uploaded and processed successfully. Output: ${stdout}`
            };
        });
    } catch (error) {
        context.res = {
            status: 500,
            body: `File upload failed: ${error.message}`
        };
    }
};

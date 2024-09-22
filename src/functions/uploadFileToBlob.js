const { BlobServiceClient } = require('@azure/storage-blob');
const multipart = require('parse-multipart');

module.exports = async function (request, context) {
    context.log(`Processing request for URL "${request.url}"`);

    const connectionString = process.env.AZURE_STORAGE_CONNECTION_STRING;

    if (!connectionString) {
        return { status: 500, body: "Azure Storage connection string is missing." };
    }

    // Check if a file is uploaded
    if (!request.body || !request.headers.get('content-type')) {
        return { status: 400, body: "No file uploaded." };
    }

    // Parse the multipart form data
    const boundary = multipart.getBoundary(request.headers.get('content-type'));
    const parts = multipart.Parse(Buffer.from(await request.arrayBuffer()), boundary);

    if (parts.length === 0) {
        return { status: 400, body: "No file found in the request." };
    }

    const file = parts[0];
    const fileName = file.filename || 'uploaded-file.pdf';

    // Create BlobServiceClient
    const blobServiceClient = BlobServiceClient.fromConnectionString(connectionString);
    const containerClient = blobServiceClient.getContainerClient('fileuploads');
    const blockBlobClient = containerClient.getBlockBlobClient(fileName);

    try {
        // Upload the file to Azure Blob Storage
        await blockBlobClient.upload(file.data, file.data.length);

        // For now, let's skip the Python script execution and just return a success message
        return {
            status: 200,
            body: `File ${fileName} uploaded successfully.`
        };
    } catch (error) {
        context.log(`Error uploading file: ${error.message}`);
        return { status: 500, body: `File upload failed: ${error.message}` };
    }
};
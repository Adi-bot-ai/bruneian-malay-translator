module.exports = async function (request, context) {
    context.log('JavaScript HTTP trigger function processed a request.');

    const name = request.query.get('name') || await request.text() || 'world';
    return { body: `Hello, ${name}!` };
};
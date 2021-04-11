const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {

    let backendURI = 'http://localhost:8800'

    app.use(
        '/api/*',
        createProxyMiddleware({
            target: backendURI,
            changeOrigin: true,
        })
    );
};

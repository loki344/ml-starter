const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
    app.use(
        '/api/*',
        createProxyMiddleware({
            target: 'http://ml-starter-backend:8800',
            changeOrigin: true,
        })
    );
};

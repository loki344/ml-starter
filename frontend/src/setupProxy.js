const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {

    let backendURI = ''
    if ("IS_IN_DOCKER" in process.env){
        backendURI = 'http://ml-starter-backend:8800'
    }else {
        backendURI = 'http://localhost:8800'
    }

    app.use(
        '/api/*',
        createProxyMiddleware({
            target: backendURI,
            changeOrigin: true,
        })
    );
};

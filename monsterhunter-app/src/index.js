// src/index.js
const express = require('express');
const session = require('express-session');
const { Issuer, generators } = require('openid-client');
//const path = require('path');

const app = express();

// Initialize OpenID Client
async function initializeClient() {
    const issuer = await Issuer.discover('https://cognito-idp.us-east-1.amazonaws.com/us-east-1_myLnMHDr4');
    client = new issuer.Client({
        client_id: '7idtfj8i7ftvr8q9n0pha6ql2j',
        client_secret: '<client secret>',
        redirect_uris: ['https://44.201.124.232'],
        response_types: ['code']
    });
};
initializeClient().catch(console.error);

app.use(session({
    secret: 'some secret',
    resave: false,
    saveUninitialized: false
}));

const checkAuth = (req, res, next) => {
    if (!req.session.userInfo) {
        req.isAuthenticated = false;
    } else {
        req.isAuthenticated = true;
    }
    next();
};

app.get('/', checkAuth, (req, res) => {
    res.render('home', {
        isAuthenticated: req.isAuthenticated,
        userInfo: req.session.userInfo
    });
});

app.get('/login', (req, res) => {
    const nonce = generators.nonce();
    const state = generators.state();

    req.session.nonce = nonce;
    req.session.state = state;

    const authUrl = client.authorizationUrl({
        scope: 'email openid phone',
        state: state,
        nonce: nonce,
    });

    res.redirect(authUrl);
});

// Helper function to get the path from the URL. Example: "http://localhost/hello" returns "/hello"
function getPathFromURL(urlString) {
    try {
        const url = new URL(urlString);
        return url.pathname;
    } catch (error) {
        console.error('Invalid URL:', error);
        return null;
    }
}

app.get(getPathFromURL('https://44.201.124.232'), async (req, res) => {
    try {
        const params = client.callbackParams(req);
        const tokenSet = await client.callback(
            'https://44.201.124.232',
            params,
            {
                nonce: req.session.nonce,
                state: req.session.state
            }
        );

        const userInfo = await client.userinfo(tokenSet.access_token);
        req.session.userInfo = userInfo;

        res.redirect('/');
    } catch (err) {
        console.error('Callback error:', err);
        res.redirect('/');
    }
});

// Logout route
app.get('/logout', (req, res) => {
    req.session.destroy();
    const logoutUrl = `https://us-east-1mylnmhdr4.auth.us-east-1.amazoncognito.com/logout?client_id=7idtfj8i7ftvr8q9n0pha6ql2j&logout_uri=<logout uri>`;
    res.redirect(logoutUrl);
});

app.set('view engine', 'ejs');

//const PORT = process.env.PORT || 3000;

// Serve static files from the public directory
//app.use(express.static(path.join(__dirname, '../public'))); // Adjusted to point to the public directory

// Serve the index.html file
//app.get('/', (req, res) => {
//    res.sendFile(path.join(__dirname, '../public', 'index.html'));
//});

// Start the server
//app.listen(PORT, () => {
//    console.log(`Node.js server is running on http://localhost:${PORT}`);
//});
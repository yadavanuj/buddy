const jwt = require('jsonwebtoken');
const User = require('../models/User'); // Import the User model
require('dotenv').config(); // Load environment variables

// Middleware for authentication
function verifyToken(req, res, next) {
    const token = req.headers['authorization'];
    if (!token) return res.status(403).send('A token is required for authentication');

    try {
        const decoded = jwt.verify(token, process.env.JWT_SECRET); // Use loaded JWT_SECRET
        User.findById(decoded.id).then(user => {
            if (!user) {
                return res.status(401).send('User not found');
            }
            req.user = user; // Attach user info to request
            next(); // Proceed to the next middleware or route handler
        });
    } catch (err) {
        return res.status(401).send('Invalid Token');
    }
}

module.exports = {
    verifyToken
};

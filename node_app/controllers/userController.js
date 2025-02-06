const User = require('../models/User');
const jwt = require('jsonwebtoken'); // Import JWT

// Controller logic for users
function registerUser(req, res) {
    const { email, password } = req.body;
    User.create(email, password)
        .then(newUser => {
            const token = jwt.sign({ id: newUser.id }, process.env.JWT_SECRET, { expiresIn: '1h' }); // Create token
            res.status(201).json({ message: 'User registered successfully', user: newUser, token }); // Return token
        })
        .catch(error => res.status(500).json({ message: 'Error registering user' }));
}

function signIn(req, res) {
    const { email, password } = req.body;
    User.findByEmail(email)
        .then(user => {
            if (!user || user.password !== password) {
                return res.status(401).json({ message: 'Invalid email or password' });
            }
            const token = jwt.sign({ id: user.id }, process.env.JWT_SECRET, { expiresIn: '1h' }); // Create token
            res.status(200).json({ message: 'User signed in successfully', token }); // Return token
        })
        .catch(error => res.status(500).json({ message: 'Error signing in' }));
}

function getUserProfile(req, res) {
    const userId = req.params.id;
    User.findById(userId)
        .then(user => {
            if (!user) {
                return res.status(404).json({ message: 'User not found' });
            }
            res.status(200).json(user);
        })
        .catch(error => res.status(500).json({ message: 'Error retrieving user profile' }));
}

function getAllUsers(req, res) {
    User.findAll()
        .then(users => res.status(200).json(users))
        .catch(error => res.status(500).json({ message: 'Error retrieving users' }));
}

function deleteUser(req, res) {
    const userId = req.params.id;
    User.deleteById(userId)
        .then(() => res.status(200).json({ message: 'User deleted successfully' }))
        .catch(error => res.status(500).json({ message: 'Error deleting user' }));
}

module.exports = {
    registerUser,
    signIn,
    getUserProfile,
    getAllUsers,
    deleteUser
};

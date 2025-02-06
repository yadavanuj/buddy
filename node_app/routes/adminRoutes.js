const express = require('express');
const router = express.Router();
const adminController = require('../controllers/adminController');
const { verifyToken } = require('../middleware/authMiddleware'); // Import the middleware

// Admin actions
router.get('/users', verifyToken, adminController.getAllUsers);
router.delete('/user/:id', verifyToken, adminController.deleteUser);

module.exports = router;

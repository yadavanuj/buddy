const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');

// User registration and actions
router.post('/register', userController.registerUser);
router.post('/signin', userController.signIn); // Add sign-in route
router.get('/:id', userController.getUserProfile);
router.get('/', userController.getAllUsers);
router.delete('/:id', userController.deleteUser);

module.exports = router;

const User = require('../models/User');

// Controller logic for admin actions
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
    getAllUsers,
    deleteUser
};

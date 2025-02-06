const db = require('../db');

// User model functions
const User = {
    create: function(email, password) {
        return new Promise((resolve, reject) => {
            const sql = 'INSERT INTO users (email, password) VALUES (?, ?)';
            db.run(sql, [email, password], function(err) {
                if (err) {
                    reject(err);
                } else {
                    resolve({ id: this.lastID, email });
                }
            });
        });
    },

    findById: function(id) {
        return new Promise((resolve, reject) => {
            const sql = 'SELECT * FROM users WHERE id = ?';
            db.get(sql, [id], (err, row) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(row);
                }
            });
        });
    },

    findAll: function() {
        return new Promise((resolve, reject) => {
            const sql = 'SELECT * FROM users';
            db.all(sql, [], (err, rows) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(rows);
                }
            });
        });
    },

    deleteById: function(id) {
        return new Promise((resolve, reject) => {
            const sql = 'DELETE FROM users WHERE id = ?';
            db.run(sql, [id], function(err) {
                if (err) {
                    reject(err);
                } else {
                    resolve({ message: 'User deleted successfully' });
                }
            });
        });
    }
};

module.exports = User;

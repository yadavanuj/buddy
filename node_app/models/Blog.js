const db = require('../db');

// Blog model functions
const Blog = {
    create: function(title, content) {
        return new Promise((resolve, reject) => {
            const sql = 'INSERT INTO blogs (title, content) VALUES (?, ?)';
            db.run(sql, [title, content], function(err) {
                if (err) {
                    reject(err);
                } else {
                    resolve({ id: this.lastID, title, content });
                }
            });
        });
    },

    findById: function(id) {
        return new Promise((resolve, reject) => {
            const sql = 'SELECT * FROM blogs WHERE id = ?';
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
            const sql = 'SELECT * FROM blogs';
            db.all(sql, [], (err, rows) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(rows);
                }
            });
        });
    },

    updateById: function(id, title, content) {
        return new Promise((resolve, reject) => {
            const sql = 'UPDATE blogs SET title = ?, content = ? WHERE id = ?';
            db.run(sql, [title, content, id], function(err) {
                if (err) {
                    reject(err);
                } else {
                    resolve({ message: 'Blog updated successfully' });
                }
            });
        });
    },

    deleteById: function(id) {
        return new Promise((resolve, reject) => {
            const sql = 'DELETE FROM blogs WHERE id = ?';
            db.run(sql, [id], function(err) {
                if (err) {
                    reject(err);
                } else {
                    resolve({ message: 'Blog deleted successfully' });
                }
            });
        });
    }
};

module.exports = Blog;

const Cache = require('./cache');
const db = require('./db'); // Import the database connection

// Initialize the cache
const userCache = new Cache('cache', { collectionName: "userCollection", expirationTime: 60000, sizeCap: 1000 });
const sessionCache = new Cache('cache', { collectionName: "sessionCollection", expirationTime: 60000, sizeCap: 1000 });
const blogCache = new Cache('cache', { collectionName: "blogCollection", expirationTime: 60000, sizeCap: 1000 });

// Attach the cache instance to the global context
global.userCache = userCache;
global.sessionCache = sessionCache;
global.blogCache = blogCache;

// Call the function to create tables
db.serialize(() => {
    db.run(`CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    );`);

    db.run(`CREATE TABLE IF NOT EXISTS blogs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL
    );`);
});

console.log('Cache initialized and attached to global context.');

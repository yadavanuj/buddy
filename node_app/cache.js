const ForerunnerDB = require('forerunnerdb');

class Cache {
    constructor(dbName, options = {}) {
        this.fdb = new ForerunnerDB();
        this.db = this.fdb.db(dbName);
        this.sizeCap = options.sizeCap || 1000; // Default size cap
        this.expirationTime = options.expirationTime || 60000; // Default expiration time in milliseconds
        this.collectionName = options.collectionName || 'cacheCollection'; // Default collection name
        this.cache = this.db.collection(this.collectionName, { primaryKey: "key", capped: true, size: this.sizeCap });
    }

    set(key, value) {
        const entry = {
            value: value,
            createdAt: new Date() // Set createdAt timestamp
        };
        this.cache.insert({ key, entry });
    }

    get(key) {
        const cachedEntry = this.cache.find({
            key: {
                $eq: key,
            },
        });
        if (cachedEntry) {
            // Check if the entry has expired
            if (new Date() - cachedEntry.entry.createdAt > this.expirationTime) {
                this.cache.remove({ key }); // Remove expired entry
                return null;
            }
            return cachedEntry.entry.value; // Return the valid cached value
        }
        return null;
    }

    delete(key) {
        this.cache.remove({
            key: {
                $eq: key,
            },
        });
    }
}

module.exports = Cache;

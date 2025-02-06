const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(bodyParser.urlencoded({
    extended: false
}));
 
app.use(bodyParser.json());

// Require the bootstrap file to initialize cache
require('./bootstrap');

// Import routes
const blogRoutes = require('./routes/blogRoutes');
const userRoutes = require('./routes/userRoutes');
const adminRoutes = require('./routes/adminRoutes'); // Ensure admin routes are imported

// Use routes
app.use('/api/blogs', blogRoutes);
app.use('/api/users', userRoutes);
app.use('/api/admin', adminRoutes); // Register admin routes

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

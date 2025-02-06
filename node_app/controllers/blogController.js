const Blog = require('../models/Blog');

// Controller logic for blogs
function createBlog(req, res) {
    const { title, content } = req.body;
    Blog.create(title, content)
        .then(newBlog => res.status(201).json({ message: 'Blog created successfully', blog: newBlog }))
        .catch(error => res.status(500).json({ message: 'Error creating blog' }));
}

function getAllBlogs(req, res) {
    Blog.findAll()
        .then(blogs => res.status(200).json(blogs))
        .catch(error => res.status(500).json({ message: 'Error retrieving blogs' }));
}

function getBlogById(req, res) {
    const blogId = req.params.id;
    Blog.findById(blogId)
        .then(blog => {
            if (!blog) {
                return res.status(404).json({ message: 'Blog not found' });
            }
            res.status(200).json(blog);
        })
        .catch(error => res.status(500).json({ message: 'Error retrieving blog' }));
}

function updateBlog(req, res) {
    const blogId = req.params.id;
    const { title, content } = req.body;
    Blog.updateById(blogId, title, content)
        .then(() => res.status(200).json({ message: 'Blog updated successfully' }))
        .catch(error => res.status(500).json({ message: 'Error updating blog' }));
}

function deleteBlog(req, res) {
    const blogId = req.params.id;
    Blog.deleteById(blogId)
        .then(() => res.status(200).json({ message: 'Blog deleted successfully' }))
        .catch(error => res.status(500).json({ message: 'Error deleting blog' }));
}

module.exports = {
    createBlog,
    getAllBlogs,
    getBlogById,
    updateBlog,
    deleteBlog
};

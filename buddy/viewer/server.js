const express = require('express');
const fs = require('fs');
const path = require('path');
const { marked } = require('marked');
const hljs = require('highlight.js');

const app = express();
const port = 3000;

// Serve static HTML files
app.use(express.static(path.join(__dirname, 'public')));

// Serve a static JSON file
app.get('/graph', (req, res) => {
	res.sendFile(path.join(__dirname, 'output', 'graphData.json'));
});

// Configure marked to use highlight.js
marked.setOptions({
	highlight: function (code, lang) {
		return hljs.highlightAuto(code, [lang]).value;
	},
});

app.get('/plan', (req, res) => {
	const filePath = path.join(__dirname, 'output', 'plan.md');
	fs.readFile(filePath, 'utf8', (err, data) => {
		if (err) {
			res.status(500).send('Error reading the file');
			return;
		}
		console.log(data);
		const htmlContent = marked(data);
		res.send(`
      <!DOCTYPE html>
      <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Markdown Viewer</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.0/styles/default.min.css">
      </head>
      <body>
      ${htmlContent}
       <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.0/highlight.min.js"></script>
        <script>hljs.highlightAll();</script>
      </body>
      </html>
    `);
	});
});

app.listen(port, () => {
	console.log(`Server is running at http://localhost:${port}`);
});

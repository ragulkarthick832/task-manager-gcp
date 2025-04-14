const express = require('express');
const path = require('path');
const mysql = require('mysql2/promise');
const app = express();
const port = 3000;

app.use(express.json());
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
  });
// Update with your Cloud SQL config
const dbConfig = {
  host: '34.58.81.11', 
  user: 'ragul',
  password: '12345',
  database: 'taskdb'
};

app.get('/tasks', async (req, res) => {
  const conn = await mysql.createConnection(dbConfig);
  const [rows] = await conn.execute('SELECT * FROM tasks');
  res.json(rows);
});

app.post('/tasks', async (req, res) => {
  const { description, status } = req.body;
  const conn = await mysql.createConnection(dbConfig);
  await conn.execute('INSERT INTO tasks (description, status) VALUES (?, ?)', [description, status]);
  res.send('Task created');
});

app.put('/tasks/:id', async (req, res) => {
  const { id } = req.params;
  const { status } = req.body;
  const conn = await mysql.createConnection(dbConfig);
  await conn.execute('UPDATE tasks SET status = ? WHERE id = ?', [status, id]);
  res.send('Task updated');
});

app.delete('/tasks/:id', async (req, res) => {
  const { id } = req.params;
  const conn = await mysql.createConnection(dbConfig);
  await conn.execute('DELETE FROM tasks WHERE id = ?', [id]);
  res.send('Task deleted');
});

// app.listen(port, () => {
//   console.log(`Server running on port ${port}`);
// });
async function startServer() {
    try {
      const conn = await mysql.createConnection(dbConfig);
      await conn.ping(); // Quick way to test connection
      console.log('✅ Successfully connected to the database.');
      conn.end();
  
      app.listen(port,'0.0.0.0', () => {
        console.log(`🚀 Server running on port ${port}`);
      });
    } catch (err) {
      console.error('❌ Failed to connect to the database:', err.message);
      process.exit(1); // Exit the process with error code
    }
  }
  
startServer();

const express = require('express');
const { Client } = require('ssh2');
const { exec } = require('child_process');
const cors = require('cors');
const app = express();
const port = 3000;

// Enable CORS
app.use(cors());

// Middleware to parse JSON bodies
app.use(express.json({ limit: '50mb' }));

let sshConnection = null; // Variable to store the SSH session

// SSH connection route
app.post('/connect-ssh', (req, res) => {
  const { host, user, keyBase64 } = req.body;

  if (!host || !user || !keyBase64) {
    return res.status(400).json({ success: false, message: 'Missing required fields' });
  }

  const privateKey = Buffer.from(keyBase64, 'base64');

  const conn = new Client();

  conn.on('ready', () => {
    console.log('SSH connection established');
    sshConnection = conn; // Store the connection in the variable
    res.json({ success: true, message: 'SSH connection established', host, user });
  }).on('error', (err) => {
    console.error('SSH connection error: ', err);
    res.json({ success: false, message: err.message });
  }).connect({
    host: host,
    port: 22,
    username: user,
    privateKey: privateKey,
  });
});

// Command execution route
app.post('/execute-command', (req, res) => {
  const command = req.body.command;

  if (!command) {
    return res.status(400).json({ success: false, message: 'No command provided' });
  }

  if (!sshConnection) {
    return res.status(400).json({ success: false, message: 'No active SSH session' });
  }

  sshConnection.exec(command, (err, stream) => {
    if (err) {
      return res.status(500).json({ success: false, message: 'Error executing command: ' + err.message });
    }

    let output = '';
    let error = '';

    stream.on('data', (data) => {
      output += data.toString();
    });

    stream.on('stderr', (data) => {
      error += data.toString();
    });

    stream.on('close', (code, signal) => {
      if (code === 0) {
        res.json({ success: true, output });
      } else {
        res.json({ success: false, error });
      }
    });
  });
});

app.post('/disconnect-ssh', (req, res) => {
  if (sshConnection) {
    sshConnection.end();
    sshConnection = null; // Reset the session
    res.json({ success: true, message: 'SSH session disconnected' });
  } else {
    res.status(400).send('No active SSH session to disconnect');
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});

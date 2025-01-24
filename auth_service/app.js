const express = require('express');
const bodyParser = require('body-parser');
const dotenv = require('dotenv');
const authRoutes = require('./routes/auth');

dotenv.config(); 

const app = express();
const PORT = process.env.PORT || 5000;

app.use(bodyParser.json());

app.use('/auth', authRoutes);

app.listen(PORT, () => {
  console.log(`Auth service is running on http://localhost:${PORT}`);
});

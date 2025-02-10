const express = require("express");
const bodyParser = require("body-parser");
const dotenv = require("dotenv");
const admin = require("firebase-admin");
const jwt = require("jsonwebtoken");
const { OAuth2Client } = require("google-auth-library");
const rateLimit = require("express-rate-limit");
const axios = require("axios");

dotenv.config();

const serviceAccount = require("./serviceAccountKey.json");
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
});

const googleClient = new OAuth2Client(process.env.GOOGLE_CLIENT_ID);

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(bodyParser.json());

// Secret key for JWT
const JWT_SECRET = process.env.JWT_SECRET || "your_jwt_secret_key";

const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: {
    error: "Too many requests, please try again later.",
  },
});

// Apply rate limiting to all routes
app.use(apiLimiter);

const verifyGoogleToken = async (idToken) => {
  try {
    const ticket = await googleClient.verifyIdToken({
      idToken,
      audience: process.env.GOOGLE_CLIENT_ID,
    });

    const payload = ticket.getPayload();
    const uid = payload.sub;

    let user;
    try {
      user = await admin.auth().getUser(uid);
    } catch (error) {
      user = await admin.auth().createUser({ uid, email: payload.email });
    }

    return { uid, email: payload.email };
  } catch (error) {
    throw new Error("Invalid Google ID token");
  }
};

app.post("/validate-token", async (req, res) => {
  const { token } = req.body;

  if (!token) {
    return res.status(400).json({ error: "Token is required" });
  }

  try {
    const decoded = verifyJWT(token);
    res.status(200).json({ valid: true, userId: decoded.uid });
  } catch (error) {
    res.status(401).json({ error: error.message });
  }
});

app.post("/validate-google-token", async (req, res) => {
  const { idToken } = req.body;

  if (!idToken) {
    return res.status(400).json({ error: "Google ID token is required" });
  }

  try {
    const { uid, email } = await verifyGoogleToken(idToken);
    res.status(200).json({ valid: true, userId: uid, email });
  } catch (error) {
    res.status(401).json({ error: error.message });
  }
});

const verifyJWT = (token) => {
  try {
    return jwt.verify(token, JWT_SECRET);
  } catch (error) {
    throw new Error("Invalid or expired token");
  }
};

app.post("/upload/:email", async (req, res) => {
  const email = req.params.email;
  const token = req.headers.authorization?.split(" ")[1]; // Extract token from Authorization header

  if (!token) {
    return res.status(401).json({ error: "Authorization token is required" });
  }

  try {
    const decoded = verifyJWT(token);

    if (!email || !req.body.file) {
      return res.status(400).json({ error: "Email and file data are required" });
    }

    const flaskBackendUrl = process.env.FLASK_BACKEND_URL || "http://127.0.0.1:5000/upload";
    const response = await axios.post(`${flaskBackendUrl}/${email}`, req.body, {
      headers: { "Content-Type": "application/json" },
    });

    res.status(response.status).json(response.data);
  } catch (error) {
    res.status(401).json({ error: error.message });
  }
});


// Start the server
app.listen(PORT, () => {
  console.log(`API Gateway running on http://localhost:${PORT}`);
});

const { createUser, authenticateUser, verifyGoogleToken, verifyFirebaseToken } = require("../services/firebaseService");

exports.signUp = async (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).json({ error: "Email and password are required" });
  }

  try {
    const user = await createUser(email, password);
    res.status(201).json({ message: "User created successfully", userId: user.uid });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};

exports.signIn = async (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).json({ error: "Email and password are required" });
  }

  try {
    const token = await authenticateUser(email, password);
    res.status(200).json({ token });
  } catch (error) {
    res.status(401).json({ error: error.message });
  }
};

exports.googleSignIn = async (req, res) => {
  const { idToken } = req.body;

  if (!idToken) {
    return res.status(400).json({ error: "Google ID token is required" });
  }

  try {
    const { uid, customToken } = await verifyGoogleToken(idToken);
    res.status(200).json({ userId: uid, token: customToken });
  } catch (error) {
    res.status(401).json({ error: error.message });
  }
};

exports.validateToken = async (req, res) => {
  const { token } = req.body;

  if (!token) {
    return res.status(400).json({ error: 'Token is required' });
  }

  try {
    const decodedToken = await verifyFirebaseToken(token);
    res.status(200).json({ valid: true, userId: decodedToken.uid });
  } catch (error) {
    res.status(401).json({ valid: false, error: error.message });
  }
};
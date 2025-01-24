const admin = require("firebase-admin");
const { OAuth2Client } = require("google-auth-library");

const serviceAccount = require("../serviceAccountKey.json");
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
});

const googleClient = new OAuth2Client(process.env.GOOGLE_CLIENT_ID);

exports.createUser = async (email, password) => {
  try {
    return await admin.auth().createUser({ email, password });
  } catch (error) {
    throw new Error(error.message);
  }
};

exports.authenticateUser = async (email, password) => {
  try {
    const user = await admin.auth().getUserByEmail(email);
    return admin.auth().createCustomToken(user.uid);
  } catch (error) {
    throw new Error("Invalid email or password");
  }
};

exports.verifyGoogleToken = async (idToken) => {
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

    const customToken = await admin.auth().createCustomToken(uid);
    return { uid, customToken };
  } catch (error) {
    throw new Error("Invalid Google ID token");
  }
};

exports.verifyFirebaseToken = async (token) => {
  try {
    const decodedToken = await admin.auth().verifyIdToken(token);
    return decodedToken;  // Return the decoded token if valid
  } catch (error) {
    throw new Error('Invalid or expired Firebase token');
  }
};
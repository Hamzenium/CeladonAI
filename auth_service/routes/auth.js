const express = require("express");
const { signUp, signIn, googleSignIn, validateToken } = require("../controllers/authController");

const router = express.Router();

router.post("/signup", signUp); // Email/Password Sign-Up
router.post("/signin", signIn); // Email/Password Sign-In
router.post("/google-signin", googleSignIn); // Google Sign-In
router.post("/validate-token", validateToken); // Token Validation

module.exports = router;

import { useState } from 'react';
import styles from '/styles/Auth.module.css';
import Head from 'next/head';
import firebase_app from "/utils/firebaseconfig.js";
import { createUserWithEmailAndPassword, getAuth, GoogleAuthProvider, signInWithPopup } from "firebase/auth";
import axios from 'axios';

const auth = getAuth(firebase_app);
const provider = new GoogleAuthProvider();

export default function Auth() {
	const [username, setUsername] = useState('');
	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');
	const [error, setError] = useState('');
	const [loading, setLoading] = useState(false);	

	const handleGoogleLogin = () => {
		setLoading(true);
		signInWithPopup(auth, provider)
			.then((result) => {
				axios.post('https://celadon-ai-flask-1194b43609af.herokuapp.com/create/user', {
					name: username,
					email: email
				}).then((response) => {
					window.location = "/";
					setLoading(false);
				}).catch(e => {
					console.log(e);
					setLoading(false);
				});
				window.location = "/";
			}).catch((error) => {
				const errorMessage = error.message;
				setError(errorMessage.replace("Firebase: ", ""));
				setLoading(false);
			});
	}

	const handleSignup = async () => {
		let result = null,
			error = null;
		try {
			result = await createUserWithEmailAndPassword(auth, email, password);
			axios.post('https://celadon-ai-flask-1194b43609af.herokuapp.com/create/user', {
				name: username,
				email: email
			}).then((response) => {
				window.location = "/";
			}).catch(e => {
				console.log(e);
			});
		} catch (e) {
			error = e;
			const errorMessage = error.message;
			setError(errorMessage.replace("Firebase: ", ""));
		}
	};

	return (
		<div className={styles.Auth}>
			<Head>
				<title>Sign Up | Personalised ChatGPT for your brand</title>
				<meta name="viewport" content="width=device-width, initial-scale=1" />
			</Head>

			<div className={styles.wrapper}>
				<strong>Welcome to Celadon AI</strong>
				<button onClick={handleGoogleLogin} className={`${styles.button} ${styles.btnGoogle}`}><img width={18} src={"/google-icon.svg"} /> Continue with Google</button>
				<p style={{ textAlign: "center" }}>or</p>
				<input
					type="name"
					placeholder="Username"
					value={username}
					onChange={(e) => setUsername(e.target.value)}
					className={styles.input}
				/>
				<input
					type="email"
					placeholder="Email"
					value={email}
					onChange={(e) => setEmail(e.target.value)}
					className={styles.input}
				/>
				<input
					type="password"
					placeholder="Password"
					value={password}
					onChange={(e) => setPassword(e.target.value)}
					className={styles.input}
				/>
				<button disabled={loading} onClick={handleSignup} className={styles.button}>
					{loading ? "Loading..." : "Create account"}
				</button>
				<p style={{ color: "red" }}>{error}</p>
				<p>Already have an account? <a href='/auth/login'>Log in</a> instead</p>
			</div>
		</div>
	);
}
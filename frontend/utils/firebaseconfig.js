// Import the functions you need from the SDKs you need
import { initializeApp, getApps } from "firebase/app";

const firebaseConfig = {
    apiKey: "AIzaSyAOSj9M-TuSbgvX5hXdQHRslX8e0v8FbnU",
    authDomain: "celadonai-69915.firebaseapp.com",
    projectId: "celadonai-69915",
    storageBucket: "celadonai-69915.appspot.com",
    messagingSenderId: "940884304741",
    appId: "1:940884304741:web:e448eb35588eb1a30af78c",
    measurementId: "G-NV4BDG6FXP"
};

// Initialize Firebase
let firebase_app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApps()[0];

export default firebase_app;
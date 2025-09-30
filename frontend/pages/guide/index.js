import React from 'react'
import styles from '@/styles/Home.module.css'
import Head from 'next/head';
import Navbar from '@/components/Navbar';

export default function index() {
    return (
        <div style={{backgroundColor: "rgb(245, 245, 245)", minHeight: "100vh", paddingBottom: 100, width: "100%"}}>
            <Head>
                <title>Guide | Personalised ChatGPT for your brand</title>
                <meta name="viewport" content="width=device-width, initial-scale=1" />
            </Head>

            <Navbar />

            <div className={styles.wrapper}>
                <h1>How to Guide: Train and Leverage Custom Chatbots to Boost Productivity</h1>

                <h2>Table of Contents</h2>
                <ol>
                    <li><a style={{ color: "black" }} href="#introduction">Introduction to Celadon AI</a></li>
                    <li><a style={{ color: "black" }} href="#documents">Uploading Documents</a></li>
                    <li><a style={{ color: "black" }} href="#training">Training the Chatbot</a></li>
                    <li><a style={{ color: "black" }} href="#using">Using the Chatbot</a></li>
                    <li><a style={{ color: "black" }} href="#tools">Other Tools</a></li>
                </ol>

                <h2 id="introduction">1. Introduction</h2>
                <p>Our flow works in a simple manner: You start by uploading a document using our form. We then create a special bot that learns from your document. This bot can answer questions and do other helpful things for you based on what it learned from the document.</p>

                <h2 id="documents">2. Uploading Documents</h2>
                <p>To upload your document, just go to the homepage and use the form provided. You can upload presentations and PDFs. Accepted file types are: ppt, pptx, doc, docx, and pdf.</p>

                <h2 id="training">3. Training the Chatbot</h2>
                <p>Once you've uploaded a file, we'll work behind the scenes to train the bot. This means we'll go through the content and use external GPT tools to create models that fit what you need. </p>

                <h2 id="using">4. Using the Chatbot</h2>
                <p>Using the generated Chatbot, you can now ask it any questions within the scope of the content in the file it is dedicated to. Example uses: Improving your presentation, enhancing your resume/CV, explaining a concept from your class notes, ect. </p>

                <h2 id="tools">5. Other Tools</h2>
                <p>The possibilities are endless when it comes to utilizing custom Chatbots. Additional tools that are to be added includes: embedding your Chatbots within your own website, automating email replies and inquiries, automatically summarizing subscribed content and much more.</p>

            </div>
        </div>
    )
}

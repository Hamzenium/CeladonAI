import React, { useState, useEffect } from 'react';
import styles from '@/styles/Chat.module.css'
import Head from 'next/head';
import Link from 'next/link';
import { useAuthContext } from "/utils/AuthContext";
import axios from 'axios';

export default function Chat({ query }) {
    const { user } = useAuthContext();
    const [name, setName] = useState(null);
    const [documentID, setDocumentID] = useState(null);
    const [loading, setLoading] = useState(false);
    const [inputList, setInputList] = useState([]);
    const [outputList, setOutputList] = useState(["Hello! Ask me a question."]);
    const [inputValue, setInputValue] = useState('');
    const [para, setPara] = useState('');

    useEffect(() => {
        if (user) {
            if (query) {
                setName(query.name);
                setDocumentID(query.id);
            }
        } else {
            window.location = "/auth/login";
        }
    }, []);

    const arrayMerge = (array1, array2) => {
        const mergedArray = [];

        for (let i = 0; i < Math.max(array1.length, array2.length); i++) {
            if (array1[i] !== undefined) {
                mergedArray.push(array1[i]);
            }

            if (array2[i] !== undefined) {
                mergedArray.push(array2[i]);
            }
        }

        return mergedArray;
    }

    const handleInputChange = (event) => {
        setInputValue(event.target.value);
    }

    const handleFormSubmit = (event) => {
        event.preventDefault();
        setLoading(true);

        if (inputValue.trim() !== '') {
            setInputList([...inputList, inputValue]);
            setInputValue('');

            axios.post(`https://celadon-ai-flask-1194b43609af.herokuapp.com/query`, {
                question: inputValue,
                document_id: documentID
            }).then(doc => {
                console.log(doc.data);
                setOutputList([...outputList, doc.data.answer]);
                setPara(doc.data.para);
                setLoading(false);
            }).catch(e => {
                console.log(e);
                setLoading(false);
            });
        }
    }

    return (
        <div>
            <Head>
                <title>Chat | Personalised ChatGPT for your brand</title>
                <meta name="viewport" content="width=device-width, initial-scale=1" />
            </Head>

            <div className={styles.Chat}>
                {name ?
                    <>
                        <div className={styles.top}>
                            <h3><Link href="/chatbots"><button className={styles.back}>Go Back</button></Link> {name}</h3>
                        </div>
                        <div className={styles.messageContainer}>
                            {para !== '' ? <div className={styles.para}><span style={{color: "orange"}}>Reference: </span>{para}</div> : null}
                            <div className={styles.messages}>
                                {arrayMerge(outputList, inputList).map((message, index) => (
                                    <div className={styles.message} key={index}>
                                        {message}
                                    </div>
                                ))}
                            </div>
                            {/* <div className={styles.alertMessage}>
                                Note: We are currently experiencing downtime with our chat responses. We will be back soon.
                            </div> */}
                            <form className={styles.form} onSubmit={handleFormSubmit}>
                               <input
                                    type="text"
                                    autoFocus={true}
                                    value={inputValue}
                                    onChange={handleInputChange}
                                    placeholder="Type your message..."
                                    className={styles.input}
                                />
                                <button disabled={loading} className={loading ? styles.disabled : styles.button} type="submit">{loading ? "Processing" : "Send"}</button>
                            </form>
                        </div>
                    </>
                    :
                    <div style={{
                        width: "100%",
                        height: "100vh"
                    }}>
                        <img style={{
                            display: "block",
                            margin: "auto",
                            paddingTop: "25vh"
                        }} src="https://i.pinimg.com/originals/49/23/29/492329d446c422b0483677d0318ab4fa.gif" width={150} />
                    </div>
                }
            </div>
        </div>
    );
}

Chat.getInitialProps = async ({ query }) => {
    return { query };
}
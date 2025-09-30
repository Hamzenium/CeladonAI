import React, { useEffect, useState } from 'react';
import styles from '../../styles/Dashboard.module.css';
import Head from 'next/head';
import Link from 'next/link';
import Navbar from '@/components/Navbar';
import { useAuthContext } from "/utils/AuthContext";

import axios from 'axios';

const Dashboard = () => {
    const { user } = useAuthContext();
    const [loading, setLoading] = useState(false);
    const [bots, setBots] = useState([]);
    const [edit, setEdit] = useState(null);
    const [confirm, setConfirm] = useState(null)


    const fetchBots = async () => {
        axios.post(`https://celadon-ai-flask-1194b43609af.herokuapp.com/dashboard`, {
            email: user.email
        }).then(doc => {
            setBots(doc.data.student_info.files);
            console.log(doc.data);
            setLoading(false);
        }).catch(e => {
            console.log(e);
            setLoading(false);
        });
    }

    const changeName = (document_id, name) => {
        if (edit) {
            console.log(document_id, name);
            axios.put(`https://celadon-ai-flask-1194b43609af.herokuapp.com/update/${document_id}`, { "document_name": `${name}` }).then(doc => {
                setEdit(null)
            }).catch(e => {
                console.log(e);
                setLoading(false);
            });
        }
        else {
            setEdit(document_id)
        }
    }
    const handleEditChange = (id, newName) => {
        console.log(newName)
        const updatedBots = bots.map(bot =>
            bot.document_id === id ? { ...bot, name: newName } : bot
        );
        setBots(updatedBots);
    }
    const handleDelete = (document_id) => {
        axios.delete(`https://celadon-ai-flask-1194b43609af.herokuapp.com/delete/${document_id}`).then(doc => {
            console.log(doc.data);
            fetchBots()
        }).catch(e => {
            console.log(e);
            setLoading(false);
        });
    }
    useEffect(() => {
        setLoading(true);

        if (user) {
            fetchBots();
        } else {
            window.location = "/auth/login";
        }
    }, []);

    return (

        <div style={{ backgroundColor: "rgb(245, 245, 245)", minHeight: "100vh", width: "100%" }}>

            <Head>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"></link>
                <title>Dashboard | Personalised ChatGPT for your brand</title>
                <meta name="viewport" content="width=device-width, initial-scale=1" />
            </Head>

            <Navbar />
            <div className={styles.dashboard}>
                {
                    loading ?
                        <div style={{
                            width: "100%",
                            height: "100vh"
                        }}>
                            <img style={{
                                display: "block",
                                margin: "auto",
                                marginTop: "25vh"
                            }} src="https://i.pinimg.com/originals/49/23/29/492329d446c422b0483677d0318ab4fa.gif" width={150} />
                        </div>
                        :
                        <div className={styles.container}>
                            <h3>Your Chat Bots <Link href="/"><button className={styles.button}>Add new</button></Link></h3>
                            <br />
                            {bots.length == 0 ? 
                            <div>
                                <h3 style={{color: "grey"}}>No chatbots available. Click on the button above to add a new chatbot</h3>
                            </div>
                            : bots.map((bot, index) => {
                                return (
                                    <div key={index}>
                                        {confirm == bot.document_id ?
                                            <div className={styles.divContainer}>
                                                <h3>Are you sure?</h3>
                                                <div style={{ display: "flex" }}>
                                                    <button className={styles.button} onClick={() => { handleDelete(bot.document_id) }}>Yes</button>
                                                    <button className={styles.button} onClick={() => { setConfirm(null) }}>No</button>
                                                </div>
                                            </div>
                                            :
                                            <div className={styles.divContainer}>
                                                <div id="chatLink">
                                                    {edit == bot.document_id ? <input onChange={(e) => handleEditChange(bot.document_id, e.target.value)} className={styles.editInput} value={bots[index].name} />
                                                        : <Link href={
                                                            {
                                                                pathname: '/chat',
                                                                query: { id: bot.document_id, name: bot.document_name }
                                                            }
                                                        } id={1} style={{ textDecoration: "none", color: "black" }}>
                                                            <h3>{bot.document_name}</h3>
                                                        </Link>
                                                    }
                                                </div>

                                                <div className={styles.icons}>
                                                    <h3>
                                                        <i id={bot.document_id} class="fa fa-pencil" onClick={(e) => { changeName(bot.document_id, bots[index].name) }}></i>
                                                    </h3>
                                                    <h3>
                                                        <i class="fa fa-trash" onClick={(e) => { setConfirm(bot.document_id) }}></i>
                                                    </h3>
                                                </div>
                                            </div>
                                        }
                                    </div>
                                )
                            })}
                        </div>
                }
            </div>
        </div>
    );
};

export default Dashboard;
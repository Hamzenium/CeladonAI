import React from 'react'
import styles from '@/styles/Home.module.css'
import JSZip from 'jszip';
import { useEffect, useState } from 'react';
import { useAuthContext } from "/utils/AuthContext";



export default function UploadForm() {
    const { user } = useAuthContext()
    const [selectedFile, setSelectedFile] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleFileUpload =  async (event) => {
        const file = event.target.files[0];
        
        // //convert pptx to xml to extract # of slides
        // const zip = new JSZip();
        // await zip.loadAsync(file);

        // if (zip.files['ppt/presentation.xml']) {
        //     const presentationXML = await zip.files['ppt/presentation.xml'].async('text');
        //     const slideMatches = presentationXML.match(/p:sldId id=/g);
        //     if (slideMatches.length < 100){
        //         setSelectedFile(file);
        //     }
        //     else{
        //         alert("Choose files with less than 100 slides")
        //     }
        // }

        setSelectedFile(file);
    };

    const handleSubmit = async event => {
        event.preventDefault();
        setLoading(true);
        
        if (user) {
            if (selectedFile) {
                const formData = new FormData();
                formData.append("file", selectedFile);
                await fetch(`https://celadon-ai-flask-1194b43609af.herokuapp.com/upload/${user.email}`, {
                    method: 'POST',
                    body: formData
                }).then(doc => {
                    setLoading(false);
                    console.log(doc);
                    window.location = "/chatbots";
                }).catch(e => {
                    console.log(e);
                });
            } else {
                alert('Please select a file.');
                setLoading(false);
            }
        } else {
            window.location = "/auth/login";
        }
    }

    return (
        <div className={styles.inner}>
            <form onSubmit={handleSubmit} className={styles.uploadForm}>
                <input type="file" onChange={handleFileUpload} className={styles.fileInput} accept=".ppt, .pptx, .pdf" />
                <button type="submit" disabled={loading} className={loading ? styles.disabled : styles.uploadButton}>{loading ?  "Processing..." : "Upload"}</button>
            </form>
        </div>
    )
}
import Head from 'next/head'
import styles from '@/styles/Home.module.css'
import UploadForm from '@/components/UploadForm';
import { Noto_Sans } from 'next/font/google'
import Navbar from '@/components/Navbar';

// If loading a variable font, you don't need to specify the font weight
const opensans = Noto_Sans({
    weight: ['400', '700'],
    style: ['normal', 'italic'],
    subsets: ['latin'],
    display: 'swap',
})

export default function Home() {
    return (
        <div>
            <div className={styles.home}>
                <Head>
                    <title>Celadon AI | Personalised ChatGPT for your brand</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1" />
                </Head>

                <Navbar/>
                
                <div className={styles.container}>
                    <div className={styles.hero}>
                        <div className={styles.landingContent}>
                            <h1 className={opensans.className}><span className={styles.highlighted}>Train and leverage</span> custom chatbots to boost productivity</h1>
                        </div> 
                        <div className={styles.formWrapper}>
                            {/* <p style={{
                                padding: 12,
                                backgroundColor: "white",
                                borderRadius: 6,
                                color: "rgb(221, 46, 46)",
                                fontWeight: "bold"
                            }}>The project is currently not functional due to recent upgrades in OpenAI models and is currently under development. Please come back later :(</p>  */}
                            <p>Start by uploading a <strong>document</strong> file to train your chatbot</p>
                            <UploadForm />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
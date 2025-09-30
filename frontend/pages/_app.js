import Layout from '../components/Layout'
import Head from "next/head";

// add bootstrap css 
// import 'bootstrap/dist/css/bootstrap.css'
import '@/styles/globals.css'

export default function App({ Component, pageProps }) {
  return (
    <Layout>
      <Head>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>
      <Component {...pageProps} />
    </Layout>
  )
}
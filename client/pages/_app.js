import Head from 'next/head';
import { AuthProvider } from '../hooks/useAuth';
import Layout from '../components/Layout/Layout';
import '../styles/globals.css';
import '../styles/colors.css';

export default function App({ Component, pageProps }) {
  return (
    <AuthProvider>
      <Head>
        <link rel="icon" href="/logo.png" />
      </Head>
      <Layout>
        <Component {...pageProps} />
      </Layout>
    </AuthProvider>
  );
}

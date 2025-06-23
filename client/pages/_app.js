import Head from 'next/head';
import getConfig from 'next/config';
import { AuthProvider } from '../hooks/useAuth';
import Layout from '../components/Layout/Layout';
import '../styles/globals.css';
import '../styles/colors.css';

const { publicRuntimeConfig } = getConfig();
const basePath = publicRuntimeConfig.basePath || '';

export default function App({ Component, pageProps }) {
  return (
    <AuthProvider>
      <Head>
        <link rel="icon" href={`${basePath}/favicon.ico`} type="image/x-icon" />
        <link rel="shortcut icon" href={`${basePath}/favicon.ico`} type="image/x-icon" />
      </Head>
      <Layout>
        <Component {...pageProps} />
      </Layout>
    </AuthProvider>
  );
}

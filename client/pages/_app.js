import { AuthProvider } from '../hooks/useAuth';
import Layout from '../components/Layout/Layout';
import '../styles/globals.css';
import '../styles/colors.css';

export default function App({ Component, pageProps }) {
  return (
    <AuthProvider>
      <Layout>
        <Component {...pageProps} />
      </Layout>
    </AuthProvider>
  );
}
import { useState } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import Link from 'next/link';
import { useAuth } from '../../hooks/useAuth';
import LoginForm from '../../components/Auth/LoginForm';
import styles from '../../styles/Auth.module.css';

export default function Login() {
  const router = useRouter();
  const { login, isAuthenticated } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  if (isAuthenticated) {
    router.push('/');
    return null;
  }

  const handleSubmit = async (formData) => {
    try {
      setLoading(true);
      setError(null);
      await login(formData);
      router.push('/');
    } catch (error) {
      console.error('Login failed:', error);
      setError(error.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>Login</title>
        <meta name="description" content="Login to your account" />
      </Head>

      <div className={styles.container}>
        <div className={styles.card}>
          <div className={styles.header}>
            <h1 className={styles.title}>Login</h1>
            <p className={styles.subtitle}>
              Welcome back!
            </p>
          </div>

          {error && (
            <div className={styles.error}>
              <p>{error}</p>
            </div>
          )}

          <LoginForm onSubmit={handleSubmit} loading={loading} />

          <div className={styles.footer}>
            <p>
              Don't have an account?{' '}
              <Link href="/auth/register" className={styles.link}>
                Register here
              </Link>
            </p>
          </div>
        </div>
      </div>
    </>
  );
}
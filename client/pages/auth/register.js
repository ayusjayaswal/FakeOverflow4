import { useState } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import Link from 'next/link';
import { useAuth } from '../../hooks/useAuth';
import RegisterForm from '../../components/Auth/RegisterForm';
import styles from '../../styles/Auth.module.css';

export default function Register() {
  const router = useRouter();
  const { register, isAuthenticated } = useAuth();
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
      await register(formData);
      router.push('/');
    } catch (error) {
      console.error('Registration failed:', error);
      setError(error.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>Register</title>
        <meta name="description" content="Create a new account" />
      </Head>

      <div className={styles.container}>
        <div className={styles.card}>
          <div className={styles.header}>
            <h1 className={styles.title}>Register</h1>
            <p className={styles.subtitle}>
              Create your account :D
            </p>
          </div>

          {error && (
            <div className={styles.error}>
              <p>{error}</p>
            </div>
          )}

          <RegisterForm onSubmit={handleSubmit} loading={loading} />

          <div className={styles.footer}>
            <p>
              Already have an account?{' '}
              <Link href="/auth/login" className={styles.link}>
                Login here
              </Link>
            </p>
          </div>
        </div>
      </div>
    </>
  );
}

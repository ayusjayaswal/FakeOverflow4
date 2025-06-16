import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import { useAuth } from '../../hooks/useAuth';
import { apiClient } from '../../lib/api';
import DiscussionForm from '../../components/Discussion/DiscussionForm';
import styles from '../../styles/NewDiscussion.module.css';

export default function NewDiscussion() {
  const router = useRouter();
  const { user, isAuthenticated } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/auth/login');
    }
  }, [isAuthenticated, router]);

  if (!isAuthenticated) {
    return null;
  }

  const handleSubmit = async (discussionData) => {
    try {
      setLoading(true);
      setError(null);
      const discussion = await apiClient.createDiscussion(discussionData);
      router.push(`/discussions/${discussion.id}`);
    } catch (error) {
      console.error('Failed to create discussion:', error);
      setError(error.message || 'Failed to create discussion');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>New Discussion</title>
        <meta name="description" content="Start a new discussion" />
      </Head>

      <div className={styles.container}>
        <div className={styles.form}>
        <div className={styles.header}>
          <h1 className={styles.title}>Start a New Discussion</h1>
        </div>

        {error && (
          <div className={styles.error}>
            <p>{error}</p>
          </div>
        )}

        
          <DiscussionForm onSubmit={handleSubmit} loading={loading} />
        </div>
      </div>
    </>
  );
}
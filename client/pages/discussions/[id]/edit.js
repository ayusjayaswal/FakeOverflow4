import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import { useAuth } from '../../../hooks/useAuth';
import { apiClient } from '../../../lib/api';
import DiscussionForm from '../../../components/Discussion/DiscussionForm';
import styles from '../../../styles/EditDiscussion.module.css';

export default function EditDiscussion() {
  const router = useRouter();
  const { id } = router.query;
  const { user, isAuthenticated } = useAuth();
  
  const [discussion, setDiscussion] = useState(null);
  const [loading, setLoading] = useState(false);
  const [pageLoading, setPageLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (id && isAuthenticated) {
      loadDiscussion();
    } else if (!isAuthenticated) {
      router.push('/auth/login');
    }
  }, [id, isAuthenticated]);

  const loadDiscussion = async () => {
    try {
      const data = await apiClient.getDiscussion(id);
      
      // Check if user owns this discussion
      if (data.user_id !== user.id) {
        router.push(`/discussions/${id}`);
        return;
      }
      
      setDiscussion(data);
    } catch (error) {
      console.error('Failed to load discussion:', error);
      setError('Failed to load discussion');
    } finally {
      setPageLoading(false);
    }
  };

  const handleSubmit = async (discussionData) => {
    try {
      setLoading(true);
      setError(null);
      await apiClient.updateDiscussion(id, discussionData);
      router.push(`/discussions/${id}`);
    } catch (error) {
      console.error('Failed to update discussion:', error);
      setError(error.message || 'Failed to update discussion');
    } finally {
      setLoading(false);
    }
  };

  if (pageLoading) {
    return (
      <div className={styles.loading}>
        <div className={styles.spinner}></div>
        <p>Loading discussion...</p>
      </div>
    );
  }

  if (error || !discussion) {
    return (
      <div className={styles.error}>
        <h1>Error</h1>
        <p>{error || 'Discussion not found or you do not have permission to edit it.'}</p>
      </div>
    );
  }

  return (
    <>
      <Head>
        <title>{discussion.title}</title>
        <meta name="description" content="Edit your discussion" />
      </Head>

      <div className={styles.container}>
        <div className={styles.header}>
          <h1 className={styles.title}>Edit Discussion</h1>
        </div>

        {error && (
          <div className={styles.error}>
            <p>{error}</p>
          </div>
        )}

        <div className={styles.form}>
          <DiscussionForm
            initialData={discussion}
            onSubmit={handleSubmit}
            loading={loading}
          />
        </div>
      </div>
    </>
  );
}
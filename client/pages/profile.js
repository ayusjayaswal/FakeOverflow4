import { useState, useEffect } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { useAuth } from '../hooks/useAuth';
import { apiClient } from '../lib/api';
import DiscussionList from '../components/Discussion/DiscussionList';
import { formatDate } from '../utils/dateUtils';
import styles from '../styles/Profile.module.css';

export default function Profile() {
  const { user, isAuthenticated } = useAuth();
  const [userDiscussions, setUserDiscussions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (isAuthenticated && user) {
      loadUserDiscussions();
    }
  }, [isAuthenticated, user]);

  const loadUserDiscussions = async () => {
    try {
      const discussions = await apiClient.getUserDiscussions(user.id);
      setUserDiscussions(discussions);
    } catch (error) {
      console.error('Failed to load user discussions:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated) {
    return (
      <div className={styles.container}>
        <div className={styles.notAuthenticated}>
          <h1>Please Login</h1>
          <p>You need to be logged in to view your profile.</p>
          <Link href="/auth/login" className={styles.loginBtn}>
            Login
          </Link>
        </div>
      </div>
    );
  }

  return (
    <>
      <Head>
        <title>{user?.username}</title>
        <meta name="description" content="Your profile and discussions" />
      </Head>

      <div className={styles.container}>
        <div className={styles.profileHeader}>
          <h1 className={styles.username}>{user?.username}</h1>
          <div className={styles.userInfo}>
            <p className={styles.email}>{user?.email}</p>
            <p className={styles.joinDate}>
              Joined {formatDate(user?.created_at)}
            </p>
          </div>
          
          <div className={styles.stats}>
            <div className={styles.stat}>
              <span className={styles.statNumber}>{user?.discussion_count || 0}</span>
              <span className={styles.statLabel}>Discussions</span>
            </div>
            <div className={styles.stat}>
              <span className={styles.statNumber}>{user?.comment_count || 0}</span>
              <span className={styles.statLabel}>Comments</span>
            </div>
          </div>
        </div>

        <section className={styles.userDiscussions}>
          <h2 className={styles.sectionTitle}>{user?.username}'s Discussions</h2>
          <DiscussionList discussions={userDiscussions} loading={loading} />
        </section>
      </div>
    </>
  );
}
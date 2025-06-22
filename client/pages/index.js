import { useState, useEffect } from 'react';
import Head from 'next/head';
import SearchBox from '../components/Search/SearchBox';
import DiscussionList from '../components/Discussion/DiscussionList';
import { apiClient } from '../lib/api';
import styles from '../styles/Home.module.css';

export default function Home() {
  const [discussions, setDiscussions] = useState([]);
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searching, setSearching] = useState(false);
  const [isSearchMode, setIsSearchMode] = useState(false);

  useEffect(() => {
    loadDiscussions();
  }, []);

  const loadDiscussions = async () => {
    try {
      setLoading(true);
      const data = await apiClient.getDiscussions({ limit: 50 });
      setDiscussions(data);
    } catch (error) {
      console.error('Failed to load discussions:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchResults = (results) => {
    setSearchResults(results);
    setIsSearchMode(results.length > 0);
  };

  const handleSearchLoading = (isLoading) => {
    setSearching(isLoading);
  };

  const displayedDiscussions = isSearchMode ? searchResults : discussions;
  const displayLoading = isSearchMode ? searching : loading;

  return (
    <>
      <Head>
        <title>tangerines</title>
        <meta name="description" content="Join the conversation on our discussion platform" />
      </Head>

      <div className={styles.container}>
        <div className={styles.hero}>
          <h1 className={styles.title}>Welcome to tangerines</h1>
          <p className={styles.subtitle}>
            a place for fake opinions of fake people...
          </p>
        </div>

        <SearchBox 
          onResults={handleSearchResults} 
          onLoading={handleSearchLoading}
        />

        <div className={styles.content}>             
          <DiscussionList 
            discussions={displayedDiscussions} 
            loading={displayLoading} 
          />
        </div>
      </div>
    </>
  );
}
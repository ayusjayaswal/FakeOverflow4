import { useState, useEffect } from 'react';
import { useDebounce } from '../../hooks/useDebounce';
import { apiClient } from '../../lib/api';
import styles from './SearchBox.module.css';

export default function SearchBox({ onResults, onLoading }) {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const debouncedQuery = useDebounce(query, 300);

  useEffect(() => {
    if (debouncedQuery.trim()) {
      handleSearch(debouncedQuery);
      fetchSuggestions(debouncedQuery);
    } else {
      onResults([]);
      setSuggestions([]);
    }
  }, [debouncedQuery]);

  const handleSearch = async (searchQuery) => {
    try {
      onLoading(true);
      const results = await apiClient.search(searchQuery);
      onResults(results.results || []);
    } catch (error) {
      console.error('Search failed:', error);
      onResults([]);
    } finally {
      onLoading(false);
    }
  };

  const fetchSuggestions = async (searchQuery) => {
    try {
      const suggestions = await apiClient.getSearchSuggestions(searchQuery);
      setSuggestions(suggestions);
    } catch (error) {
      console.error('Failed to fetch suggestions:', error);
    }
  };

  const handleInputChange = (e) => {
    setQuery(e.target.value);
    setShowSuggestions(true);
  };

  const handleSuggestionClick = (suggestion) => {
    setQuery(suggestion);
    setShowSuggestions(false);
  };

  return (
    <div className={styles.searchContainer}>
      <div className={styles.searchBox}>
        <input
          type="text"
          value={query}
          onChange={handleInputChange}
          onFocus={() => setShowSuggestions(true)}
          onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
          placeholder="Search Active Discussions..."
          className={styles.searchInput}
        />
        
        {showSuggestions && suggestions.length > 0 && (
          <div className={styles.suggestions}>
            {suggestions.map((suggestion, index) => (
              <div key={index} className={styles.suggestion} onClick={() => handleSuggestionClick(suggestion)} >
                {suggestion}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

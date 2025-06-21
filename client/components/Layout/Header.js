import Link from 'next/link';
import { useAuth } from '../../hooks/useAuth';
import styles from './Header.module.css';
import { useState, useEffect } from 'react';

export default function Header() {
  const { user, logout, isAuthenticated } = useAuth();
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    const initialTheme = savedTheme || systemTheme;
    setTheme(initialTheme);
    document.documentElement.setAttribute('data-theme', initialTheme);
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
  };

  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <Link href="/" className={styles.logo}>torikai</Link>
        
        <nav className={styles.nav}>
          {isAuthenticated ? (
            <>
              <Link href="/discussions/new" className={styles.navLink}>
                New Discussion
              </Link>
              <Link href="/profile" className={styles.navLink}>
                {user?.username}
              </Link>
              <button onClick={logout} className={styles.logoutBtn}>
                Logout
              </button>
            </>
          ) : (
            <>
              <Link href="/auth/login" className={styles.navLink}>
                Login
              </Link>
              <Link href="/auth/register" className={styles.navLink}>
                Register
              </Link>
            </>
          )}
          <button onClick={toggleTheme} className={styles.themeBtn}>
            {theme === 'light' ? '🌙' : '☀️'}
          </button>
        </nav>
      </div>
    </header>
  );
}
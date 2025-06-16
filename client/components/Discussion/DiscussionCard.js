import Link from 'next/link';
import { formatDate } from '../../utils/dateUtils';
import styles from './DiscussionCard.module.css';

export default function DiscussionCard({ discussion }) {
  const truncatedContent = discussion.content.length > 50 
    ? discussion.content.substring(0, 50) + '...' 
    : discussion.content;

  return (
    <div className={styles.card}>
      <Link href={`/discussions/${discussion.id}`} className={styles.cardLink}>
        <h3 className={styles.title}>{discussion.title}</h3>
        <p className={styles.content}>{truncatedContent}</p>
        
        <div className={styles.meta}>
          <span className={styles.author}>By {discussion.author?.username}</span>
          <span className={styles.date}>{formatDate(discussion.created_at)}</span>
          <span className={styles.comments}>{discussion.comment_count || 0} comments</span>
        </div>
        
        {discussion.tags && discussion.tags.length > 0 && (
          <div className={styles.tags}>
            {discussion.tags.map((tag, index) => (
              <span key={index} className={styles.tag}>
                {tag}
              </span>
            ))}
          </div>
        )}
      </Link>
    </div>
  );
}
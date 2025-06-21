import DiscussionCard from './DiscussionCard';
import styles from './DiscussionList.module.css';

export default function DiscussionList({ discussions, loading }) {
  if (loading) {
    return (
      <div className={styles.loading}>
        <div className={styles.spinner}></div>
        <p>Loading discussions...</p>
      </div>
    );
  }

  if (!discussions || discussions.length === 0) {
    return (
      <div className={styles.empty}>
        <p>No active toiwas found.</p>
      </div>
    );
  }

  return (
    <div className={styles.discussionList}>
      {discussions.map((discussion) => (
        <DiscussionCard key={discussion.id} discussion={discussion} />
      ))}
    </div>
  );
}

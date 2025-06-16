import { useState } from 'react';
import styles from './CommentForm.module.css';

export default function CommentForm({ 
  initialData, 
  onSubmit, 
  onCancel, 
  submitText = 'Post Comment',
  loading 
}) {
  const [content, setContent] = useState(initialData?.content || '');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (content.trim()) {
      onSubmit({ content: content.trim() });
      if (!initialData) {
        setContent('');
      }
    }
  };

  return (
    <form onSubmit={handleSubmit} className={styles.form}>
      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Write your comment..."
        required
        rows={4}
        className={styles.textarea}
      />
      
      <div className={styles.actions}>
        <button type="submit" disabled={loading || !content.trim()} className={styles.submitBtn} >
          {loading ? 'Posting...' : submitText}
        </button>
        {onCancel && (
          <button type="button" onClick={onCancel} className={styles.cancelBtn} >
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}
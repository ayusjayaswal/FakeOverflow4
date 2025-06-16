import { useState } from 'react';
import styles from './DiscussionForm.module.css';

export default function DiscussionForm({ initialData, onSubmit, loading }) {
  const [formData, setFormData] = useState({
    title: initialData?.title || '',
    content: initialData?.content || '',
    tags: initialData?.tags?.join(', ') || '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const tags = formData.tags
      .split(',')
      .map(tag => tag.trim())
      .filter(tag => tag.length > 0);
    
    onSubmit({
      title: formData.title,
      content: formData.content,
      tags,
    });
  };

  return (
    <form onSubmit={handleSubmit} className={styles.form}>
      <div className={styles.field}>
        <label htmlFor="title" className={styles.label}>
          Title
        </label>
        <input
          type="text"
          id="title"
          name="title"
          value={formData.title}
          onChange={handleChange}
          required
          className={styles.input}
        />
      </div>

      <div className={styles.field}>
        <label htmlFor="content" className={styles.label}>
          Content
        </label>
        <textarea
          id="content"
          name="content"
          value={formData.content}
          onChange={handleChange}
          required
          rows={10}
          className={styles.textarea}
        />
      </div>

      <div className={styles.field}>
        <label htmlFor="tags" className={styles.label}>
          Tags (comma-separated)
        </label>
        <input
          type="text"
          id="tags"
          name="tags"
          value={formData.tags}
          onChange={handleChange}
          placeholder="technology, programming, discussion"
          className={styles.input}
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className={styles.submitBtn}
      >
        {loading ? 'Submitting...' : (initialData ? 'Update Discussion' : 'Create Discussion')}
      </button>
    </form>
  );
}

import { useState, useEffect } from 'react';
import { Edit, Shredder } from 'lucide-react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import Link from 'next/link';
import { useAuth } from '../../hooks/useAuth';
import { apiClient } from '../../lib/api';
import CommentList from '../../components/Comment/CommentList';
import CommentForm from '../../components/Comment/CommentForm';
import { formatDate } from '../../utils/dateUtils';
import styles from '../../styles/DiscussionDetail.module.css';

export default function DiscussionDetail() {
  const router = useRouter();
  const { id } = router.query;
  const { user, isAuthenticated } = useAuth();
  
  const [discussion, setDiscussion] = useState(null);
  const [comments, setComments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [commentLoading, setCommentLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (id) {
      loadDiscussion();
      loadComments();
    }
  }, [id]);

  const loadDiscussion = async () => {
    try {
      const data = await apiClient.getDiscussion(id);
      setDiscussion(data);
    } catch (error) {
      console.error('Failed to load discussion:', error);
      setError('Failed to load discussion');
    }
  };

  const loadComments = async () => {
    try {
      const data = await apiClient.getDiscussionComments(id, { tree: true });
      setComments(data);
    } catch (error) {
      console.error('Failed to load comments:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleNewComment = async (commentData) => {
    try {
      setCommentLoading(true);
      await apiClient.createComment({
        ...commentData,
        discussion_id: parseInt(id),
      });
      await loadComments();
    } catch (error) {
      console.error('Failed to create comment:', error);
      alert('Failed to create comment');
    } finally {
      setCommentLoading(false);
    }
  };

  const handleEditComment = async (commentId, commentData) => {
    try {
      await apiClient.updateComment(commentId, commentData);
      await loadComments();
    } catch (error) {
      console.error('Failed to update comment:', error);
      alert('Failed to update comment');
    }
  };

  const handleDeleteComment = async (commentId) => {
    if (confirm('Are you sure you want to delete this comment?')) {
      try {
        await apiClient.deleteComment(commentId);
        await loadComments();
      } catch (error) {
        console.error('Failed to delete comment:', error);
        alert('Failed to delete comment');
      }
    }
  };

  const handleDeleteDiscussion = async () => {
    if (confirm('Are you sure you want to delete this discussion?')) {
      try {
        await apiClient.deleteDiscussion(id);
        router.push('/');
      } catch (error) {
        console.error('Failed to delete discussion:', error);
        alert('Failed to delete discussion');
      }
    }
  };

  if (loading) {
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
        <h1>Discussion Not Found</h1>
        <p>{error || 'The discussion you are looking for does not exist.'}</p>
        <Link href="/" className={styles.backLink}>
          ← Back to Home
        </Link>
      </div>
    );
  }

  const isOwner = user && user.id === discussion.user_id;

  return (
    <>
      <Head>
        <title>{discussion.title}</title>
        <meta name="description" content={discussion.content.substring(0, 160)} />
      </Head>

      <div className={styles.container}>
      
        <article className={styles.discussion}>
          <header className={styles.header}>
            <h1 className={styles.title}>{discussion.title}</h1>
            
            <div className={styles.meta}>
              <span className={styles.author}>
                By {discussion.author?.username}
              </span>
              <span className={styles.date}>
                {formatDate(discussion.created_at)}
              </span>
              {discussion.updated_at !== discussion.created_at && (
                <span className={styles.updated}>
                  (edited {formatDate(discussion.updated_at)})
                </span>
              )}
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



          </header>

          <div className={styles.content}>
            <p>{discussion.content}</p>
          </div>
          {isOwner && (
  <div className={styles.actions}>
    <button onClick={handleDeleteDiscussion} className={styles.iconBtn} aria-label="Delete discussion" >
      ❌
    </button>
    <Link href={`/discussions/${id}/edit`} className={styles.iconBtn} aria-label="Edit discussion" >
      🖋️
    </Link>
  </div>
)}
        </article>
        <section className={styles.commentsSection}>
          <h2 className={styles.commentsTitle}>
            Comments ({comments.length})
          </h2>

          {isAuthenticated ? (
            <div className={styles.newComment}>
              <h3>Add a Comment</h3>
              <CommentForm
                onSubmit={handleNewComment}
                loading={commentLoading}
              />
            </div>
          ) : (
            <div className={styles.loginPrompt}>
              <p>
                <Link href="/auth/login" className={styles.loginLink}>
                  Login
                </Link>{' '}
                or{' '}
                <Link href="/auth/register" className={styles.loginLink}>
                  register
                </Link>{' '}
                to comment
              </p>
            </div>
          )}

          <CommentList
            comments={comments}
            onReply={handleNewComment}
            onEdit={handleEditComment}
            onDelete={handleDeleteComment}
            currentUserId={user?.id}
          />
        </section>
      </div>
    </>
  );
}

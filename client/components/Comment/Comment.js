import { useState } from 'react';
import { formatDate } from '../../utils/dateUtils';
import CommentForm from './CommentForm';
import styles from './Comment.module.css';

export default function Comment({ comment, onReply, onEdit, onDelete, currentUserId }) {
  const [showReplyForm, setShowReplyForm] = useState(false);
  const [showEditForm, setShowEditForm] = useState(false);
  const [isExpanded, setIsExpanded] = useState(true);

  const handleReply = (replyData) => {
    onReply({
      ...replyData,
      parent_comment_id: comment.id,
    });
    setShowReplyForm(false);
  };

  const handleEdit = (editData) => {
    onEdit(comment.id, editData);
    setShowEditForm(false);
  };

  const isOwner = currentUserId === comment.user_id;

  return (
    <div className={styles.comment}>
      <div className={styles.commentHeader}>
        <span className={styles.author}>{comment.author?.username}</span>
        <span className={styles.date}>{formatDate(comment.created_at)}</span>
        
        {comment.replies && comment.replies.length > 0 && (
          <button onClick={() => setIsExpanded(!isExpanded)} className={styles.toggleBtn} >
            {isExpanded ? 'Collapse' : `Expand (${comment.replies.length})`}
          </button>
        )}
      </div>

      {showEditForm ? (
        <CommentForm
          initialData={{ content: comment.content }}
          onSubmit={handleEdit}
          onCancel={() => setShowEditForm(false)}
          submitText="Update Comment"
        />
      ) : (
        <div className={styles.content}>{comment.content}</div>
      )}

      <div className={styles.actions}>
        <button onClick={() => setShowReplyForm(!showReplyForm)} className={styles.actionBtn} >
          Reply
        </button>
        
        {isOwner && (
          <>
            <button onClick={() => setShowEditForm(!showEditForm)} className={styles.actionBtn} >
              Edit
            </button>
            <button onClick={() => onDelete(comment.id)} className={`${styles.actionBtn} ${styles.deleteBtn}`} >
              Delete
            </button>
          </>
        )}
      </div>

      {showReplyForm && (
        <div className={styles.replyForm}>
          <CommentForm
            onSubmit={handleReply}
            onCancel={() => setShowReplyForm(false)}
            submitText="Post Reply"
          />
        </div>
      )}

      {isExpanded && comment.replies && comment.replies.length > 0 && (
        <div className={styles.replies}>
          {comment.replies.map((reply) => (
            <Comment
              key={reply.id}
              comment={reply}
              onReply={onReply}
              onEdit={onEdit}
              onDelete={onDelete}
              currentUserId={currentUserId}
            />
          ))}
        </div>
      )}
    </div>
  );
}
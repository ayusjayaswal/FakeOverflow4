import Comment from './Comment';
import styles from './CommentList.module.css';

export default function CommentList({ comments, onReply, onEdit, onDelete, currentUserId }) {
  if (!comments || comments.length === 0) {
    return (
      <div className={styles.empty}>
        <p>No comments yet. Be the first to comment!</p>
      </div>
    );
  }

  return (
    <div className={styles.commentList}>
      {comments.map((comment) => (
        <Comment
          key={comment.id}
          comment={comment}
          onReply={onReply}
          onEdit={onEdit}
          onDelete={onDelete}
          currentUserId={currentUserId}
        />
      ))}
    </div>
  );
}
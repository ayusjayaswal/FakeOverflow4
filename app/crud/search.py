from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc, or_, text 
from app.models.discussion import Discussion
from app.models.comment import Comment
from typing import List, Optional, Tuple
import time
import logging

logger = logging.getLogger(__name__)

def search_discussions_with_comments(
    db: Session,
    query: str,
    limit: int = 20,
    offset: int = 0,
    similarity_threshold: float = 0.1
) -> Tuple[List[dict], int, float]:
    start_time = time.time()   
    if not query or not query.strip():
        return [], 0, 0
    clean_query = query.strip()
    db.execute(text(f"SELECT set_limit({similarity_threshold})"))
    search_sql = text("""
        WITH discussion_matches AS (
            -- Search in discussion titles and content
            SELECT 
                d.id,
                d.title,
                d.content,
                d.created_at,
                d.updated_at,
                u.username,
                u.email,
                CASE 
                    -- Exact match gets highest score
                    WHEN LOWER(d.title) = LOWER(:query) THEN 100
                    -- Title similarity using pg_trgm
                    WHEN d.title % :query THEN 80 + (similarity(d.title, :query) * 20)
                    -- Content similarity using pg_trgm
                    WHEN d.content % :query THEN 60 + (similarity(d.content, :query) * 20)
                    -- Full-text search fallback
                    WHEN to_tsvector('english', d.title || ' ' || d.content) @@ plainto_tsquery('english', :query) 
                        THEN 40 + (ts_rank(to_tsvector('english', d.title || ' ' || d.content), plainto_tsquery('english', :query)) * 30)
                    ELSE 10
                END as relevance_score,
                similarity(d.title, :query) as title_similarity,
                similarity(d.content, :query) as content_similarity,
                'discussion' as match_type
            FROM discussions d
            JOIN users u ON d.user_id = u.id
            WHERE d.is_active = true
            AND (
                d.title % :query
                OR d.content % :query
                OR to_tsvector('english', d.title || ' ' || d.content) @@ plainto_tsquery('english', :query)
                OR d.title ILIKE :ilike_pattern
                OR d.content ILIKE :ilike_pattern
            )
        ),
        comment_matches AS (
            -- Search in comments
            SELECT 
                d.id,
                d.title,
                d.content,
                d.created_at,
                d.updated_at,
                u.username,
                u.email,
                CASE 
                    WHEN c.content % :query THEN 50 + (similarity(c.content, :query) * 20)
                    ELSE 25
                END as relevance_score,
                0 as title_similarity,
                similarity(c.content, :query) as content_similarity,
                'comment' as match_type
            FROM discussions d
            JOIN users u ON d.user_id = u.id
            JOIN comments c ON c.discussion_id = d.id
            WHERE d.is_active = true 
            AND c.is_active = true
            AND (
                c.content % :query
                OR c.content ILIKE :ilike_pattern
            )
        ),
        all_matches AS (
            SELECT * FROM discussion_matches
            UNION ALL
            SELECT * FROM comment_matches
        ),
        grouped_results AS (
            SELECT 
                id,
                title,
                content,
                created_at,
                updated_at,
                username,
                email,
                MAX(relevance_score) as max_relevance,
                MAX(title_similarity) as max_title_similarity,
                MAX(content_similarity) as max_content_similarity,
                array_agg(DISTINCT match_type) as match_types
            FROM all_matches
            GROUP BY id, title, content, created_at, updated_at, username, email
        )
        SELECT 
            gr.*,
            COUNT(*) OVER() as total_count,
            (SELECT COUNT(*) FROM comments WHERE discussion_id = gr.id AND is_active = true) as comment_count
        FROM grouped_results gr
        ORDER BY gr.max_relevance DESC, gr.created_at DESC
        LIMIT :limit OFFSET :offset
    """)
    try:
        result = db.execute(search_sql, {
            'query': clean_query,
            'ilike_pattern': f'%{clean_query}%',
            'limit': limit,
            'offset': offset
        }).fetchall()
        
        search_time = (time.time() - start_time) * 1000
        
        if not result:
            return [], 0, search_time
        
        total_count = result[0].total_count if result else 0
        processed_results = []
        for row in result:
            matched_in = []
            if 'discussion' in row.match_types:
                if row.max_title_similarity > similarity_threshold:
                    matched_in.append("title")
                if row.max_content_similarity > similarity_threshold:
                    matched_in.append("content")
                if not matched_in:
                    if clean_query.lower() in row.title.lower():
                        matched_in.append("title")
                    if clean_query.lower() in row.content.lower():
                        matched_in.append("content")
            if 'comment' in row.match_types:
                matched_in.append("comments")
            snippet = _generate_snippet_with_highlight(row.title, row.content, clean_query, max_length=200)
            
            processed_results.append({
                'id': row.id,
                'title': row.title,
                'content': row.content,
                'created_at': row.created_at,
                'updated_at': row.updated_at,
                'author': {
                    'username': row.username,
                    'email': row.email
                },
                'comment_count': row.comment_count,
                'relevance_score': float(row.max_relevance),
                'title_similarity': float(row.max_title_similarity) if row.max_title_similarity else 0.0,
                'content_similarity': float(row.max_content_similarity) if row.max_content_similarity else 0.0,
                'matched_in': matched_in,
                'snippet': snippet
            })
        
        return processed_results, total_count, search_time
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        return _fallback_search(db, clean_query, limit, offset, start_time)

def _fallback_search(db: Session, query: str, limit: int, offset: int, start_time: float) -> Tuple[List[dict], int, float]:
    """Fallback search using SQLAlchemy ORM with ILIKE"""
    from app.crud.discussion import get_discussion_comment_count
    
    search_pattern = f"%{query}%"
    
    try:
        discussions_query = db.query(Discussion).options(
            joinedload(Discussion.author)
        ).filter(
            Discussion.is_active == True,
            or_(
                Discussion.title.ilike(search_pattern),
                Discussion.content.ilike(search_pattern)
            )
        )
        total_count = discussions_query.count()
        discussions = discussions_query.order_by(
            desc(Discussion.created_at)
        ).offset(offset).limit(limit).all()
        
        search_time = (time.time() - start_time) * 1000
        
        processed_results = []
        for discussion in discussions:
            matched_in = []
            if query.lower() in discussion.title.lower():
                matched_in.append("title")
            if query.lower() in discussion.content.lower():
                matched_in.append("content")
            relevance_score = 10
            if discussion.title.lower() == query.lower():
                relevance_score = 100
            elif discussion.title.lower().startswith(query.lower()):
                relevance_score = 50
            elif query.lower() in discussion.title.lower():
                relevance_score = 30
            snippet = _generate_snippet_with_highlight(discussion.title, discussion.content, query, max_length=200)
            comment_count = get_discussion_comment_count(db, discussion.id)
            
            processed_results.append({
                'id': discussion.id,
                'title': discussion.title,
                'content': discussion.content,
                'created_at': discussion.created_at,
                'updated_at': discussion.updated_at,
                'author': {
                    'username': discussion.author.username,
                    'email': discussion.author.email
                },
                'comment_count': comment_count,
                'relevance_score': float(relevance_score),
                'title_similarity': 0.0,
                'content_similarity': 0.0,
                'matched_in': matched_in,
                'snippet': snippet
            })
        
        return processed_results, total_count, search_time
        
    except Exception as e:
        logger.error(f"Fallback search error: {e}")
        return [], 0, (time.time() - start_time) * 1000

def _generate_snippet_with_highlight(title: str, content: str, query: str, max_length: int = 200) -> str:
    query_lower = query.lower()
    
    if query_lower in title.lower():
        snippet = title[:max_length]
        if len(title) > max_length:
            snippet += "..."
        return snippet
    
    content_lower = content.lower()
    query_pos = content_lower.find(query_lower)
    
    if query_pos == -1:
        snippet = content[:max_length]
        if len(content) > max_length:
            snippet += "..."
        return snippet
    context_length = max_length // 3
    start_pos = max(0, query_pos - context_length)
    end_pos = min(len(content), query_pos + len(query) + context_length)
    
    if end_pos - start_pos > max_length:
        end_pos = start_pos + max_length
    
    snippet = content[start_pos:end_pos]
    if start_pos > 0:
        snippet = "..." + snippet
    if end_pos < len(content):
        snippet = snippet + "..."
    
    return snippet

def get_search_suggestions(db: Session, partial_query: str, limit: int = 10) -> List[str]:
    if len(partial_query) < 2:
        return []
    
    try:
        suggestions_sql = text("""
            WITH title_words AS (
                SELECT DISTINCT unnest(string_to_array(title, ' ')) as word
                FROM discussions 
                WHERE is_active = true
                AND title % :query
            ),
            content_words AS (
                SELECT DISTINCT unnest(string_to_array(content, ' ')) as word
                FROM discussions 
                WHERE is_active = true
                AND content % :query
                AND LENGTH(content) < 1000  -- Don't extract from very long content
            ),
            all_words AS (
                SELECT word, similarity(word, :query) as sim
                FROM (
                    SELECT word FROM title_words
                    UNION
                    SELECT word FROM content_words
                ) words
                WHERE LENGTH(word) > 2 
                AND word % :query
            )
            SELECT word
            FROM all_words
            ORDER BY sim DESC, word
            LIMIT :limit
        """)
        
        result = db.execute(suggestions_sql, {
            'query': partial_query,
            'limit': limit
        }).fetchall()
        
        return [row.word for row in result]
        
    except Exception as e:
        logger.error(f"Suggestions error: {e}")
        try:
            discussions = db.query(Discussion.title).filter(
                Discussion.is_active == True,
                Discussion.title.ilike(f'%{partial_query}%')
            ).limit(limit * 2).all()
            
            suggestions = set()
            for discussion in discussions:
                words = discussion.title.split()
                for word in words:
                    if len(word) > 2 and partial_query.lower() in word.lower():
                        suggestions.add(word)
                        if len(suggestions) >= limit:
                            break
                if len(suggestions) >= limit:
                    break
            
            return sorted(list(suggestions))[:limit]
            
        except Exception as fallback_error:
            logger.error(f"Suggestions fallback error: {fallback_error}")
            return []

def get_popular_discussions(db: Session, days: int = 7, limit: int = 10) -> List[dict]:
    try:
        popular_sql = text("""
            SELECT 
                d.id,
                d.title,
                d.content,
                d.created_at,
                u.username,
                COUNT(c.id) as comment_count,
                COUNT(DISTINCT c.user_id) as unique_commenters
            FROM discussions d
            JOIN users u ON d.user_id = u.id
            LEFT JOIN comments c ON c.discussion_id = d.id 
                AND c.is_active = true
                AND c.created_at >= NOW() - INTERVAL ':days days'
            WHERE d.is_active = true
            AND d.created_at >= NOW() - INTERVAL ':days days'
            GROUP BY d.id, d.title, d.content, d.created_at, u.username
            ORDER BY comment_count DESC, unique_commenters DESC, d.created_at DESC
            LIMIT :limit
        """)
        
        result = db.execute(popular_sql, {
            'days': days,
            'limit': limit
        }).fetchall()
        
        return [
            {
                'id': row.id,
                'title': row.title,
                'content': row.content[:200] + ("..." if len(row.content) > 200 else ""),
                'created_at': row.created_at,
                'author_username': row.username,
                'comment_count': row.comment_count,
                'unique_commenters': row.unique_commenters
            }
            for row in result
        ]
        
    except Exception as e:
        logger.error(f"Popular discussions error: {e}")
        return []
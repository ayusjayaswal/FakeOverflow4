from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.search import search_discussions_with_comments, get_search_suggestions
from app.schemas.discussion import DiscussionSearchResult, SearchResponse
from typing import List

router = APIRouter()

@router.get("/", response_model=SearchResponse)
def search_discussions(
    q: str = Query(..., description="Search query", min_length=1, max_length=100),
    limit: int = Query(20, description="Maximum number of results", ge=1, le=100),
    offset: int = Query(0, description="Offset for pagination", ge=0),
    db: Session = Depends(get_db)
):
    try:
        results, total_count, search_time = search_discussions_with_comments(
            db=db,
            query=q,
            limit=limit,
            offset=offset
        )
        
        return SearchResponse(
            results=results,
            total_count=total_count,
            query=q,
            search_time_ms=search_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@router.get("/suggestions", response_model=List[str])
def get_search_suggestions_endpoint(
    q: str = Query(..., description="Partial search query", min_length=1, max_length=50),
    limit: int = Query(10, description="Maximum number of suggestions", ge=1, le=20),
    db: Session = Depends(get_db)
):
    try:
        suggestions = get_search_suggestions(
            db=db,
            partial_query=q,
            limit=limit
        )
        return suggestions
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get suggestions: {str(e)}")
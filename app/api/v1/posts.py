from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from app.db.database import get_db
from app.models.schemas.posts import LikeUpdate, PostOut
from app.models.post import Post
from app.models.comment import Comment
from app.models.schemas.comments import CommentIn, CommentOut

router = APIRouter(
    prefix="/api/v1/posts",
    tags=["Posts"]
)

# Get all posts
@router.get("/", response_model=list[PostOut])
async def get_posts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Post).options(selectinload(Post.comments))
    )
    posts = result.scalars().all()
    return posts

# Get single post by ID
@router.get("/{post_id}", response_model=PostOut)
async def get_post(post_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    anon_id = request.headers.get("X-Anonymous-Id")
    if not anon_id:
        raise HTTPException(status_code=400, detail="Missing anonymous ID")
    
    stmt = select(Post).options(selectinload(Post.comments)).filter(Post.id == post_id)
    
    result = await db.execute(stmt)
    post = result.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if anon_id not in post.viewed_users:
        post.views += 1
        post.viewed_users = post.viewed_users + [anon_id]
    
    db.add(post)
    await db.commit()
    await db.refresh(post)

    return post

@router.patch("/{post_id}", response_model=PostOut)
async def update_post_likes(post_id: int, likes: LikeUpdate, request: Request, db: AsyncSession = Depends(get_db)):
    anon_id = request.headers.get("X-Anonymous-Id")
    if not anon_id:
        raise HTTPException(status_code=400, detail="Missing anonymous ID")
    
    result = await db.execute(
        select(Post).options(selectinload(Post.comments)).where(Post.id == post_id)
    )
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Update the like count
    if anon_id not in post.liked_users:
        post.likes = likes.likes
        post.liked_users = post.liked_users + [anon_id]
    else:
        raise HTTPException(status_code=400, detail="You have already liked this post")
    
    db.add(post)
    await db.commit()
    await db.refresh(post)

    return post


# Comment on a post
@router.post("/{post_id}/comments", response_model=CommentOut)
async def create_comment(post_id: int, comment: CommentIn, db: AsyncSession = Depends(get_db)):
    post = await db.execute(select(Post).where(Post.id == post_id))
    post = post.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db_comment = Comment(post_id=post_id, **comment.dict())
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)

    return db_comment
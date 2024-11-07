import asyncio

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, User, Profile, Post

async def create_user(session:AsyncSession, username:str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    user: User | None = await session.scalar(stmt)
    return user


async def create_user_profile(
        session: AsyncSession,
        user_id: int,
        first_name: str | None =None,
        last_name: str | None = None
) -> Profile:

    profile = Profile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name
    )
    session.add(profile)
    await session.commit()
    return profile


async def show_user_with_profile(session: AsyncSession):
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        print(user.profile.first_name)


async def create_posts(session: AsyncSession, user_id: int, *posts_title: str) -> list[Post]:
    posts = [
        Post(title=title, user_id=user_id)
        for title in posts_title
    ]
    session.add_all(posts)
    await session.commit()
    return list(posts)


async def get_user_with_posts_and_profiles(session: AsyncSession):
    stmt = select(User).options(joinedload(User.profile), selectinload(User.posts)).order_by(User.id)
    users = await session.scalars(stmt)

    for user in users:  # type: User
        print(user, user.profile and user.profile.first_name)
        for post in user.posts:
            print(post)


async def get_user_with_posts(session: AsyncSession):
    stmt = select(User).options(selectinload(User.posts)).order_by(User.id)
    users = await session.scalars(stmt)

    for user in users:  # type: User
        print(user)
        for post in user.posts:
            print(post)


async def get_posts_with_author(session: AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)

    for post in posts: #type: Post
        print(post)
        print(post.user)


async def get_profiles_with_users_and_users_with_posts(session: AsyncSession):
    stmt = (
        select(Profile)
        .join(Profile.user)
        .options(
            joinedload(Profile.user).selectinload(User.posts),
        )
        .order_by(Profile.id)
    )

    profiles = await session.scalars(stmt)

    for profile in profiles:
        print(profile.first_name, profile.user)
        print(profile.user.posts)


async def main_relations(session: AsyncSession):
    await create_user(session=session, username="john")
    await create_user(session=session, username="sam")
    await create_user(session=session, username="alice")
    user_john = await get_user_by_username(session=session, username="john")
    user_sam = await get_user_by_username(session=session, username="sam")
    user_alice = await get_user_by_username(session=session, username="alice")
    await create_user_profile(
        session=session,
        user_id=user_john.id,
        first_name="John",
    )
    await create_user_profile(
        session=session,
        user_id=user_sam.id,
        first_name="Sam",
    )
    await create_user_profile(
        session=session,
        user_id=user_alice.id,
        first_name="Alice",
    )
    await show_user_with_profile(session=session)
    await create_posts(
        session,
        user_john.id,
        "SQLA 2.0",
        "SQLA Joins"
    )
    await create_posts(
        session,
        user_sam.id,
        "FastAPi Intro",
        "FastAPi Advanced",
        "FastAPi more"
    )
    await get_user_with_posts(session=session)
    await get_posts_with_author(session=session)
    await get_profiles_with_users_and_users_with_posts(session=session)
    await get_user_with_posts_and_profiles(session=session)
    await get_user_with_posts(session=session)


async def demo_m2m(session: AsyncSession):
    pass


async def main():
    async with db_helper.session_factory() as session:
        # await main_relations(session=session)
        await demo_m2m(session=session)

if __name__ == '__main__':
    asyncio.run(main())
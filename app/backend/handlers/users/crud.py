from datetime import datetime
from typing import List
from typing import Optional
from typing import Sequence

from sqlalchemy import RowMapping
from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import text
from sqlalchemy import update

from app.backend.db.base_crud import BaseCRUD
from app.backend.handlers.users.models import User
from app.backend.handlers.users.models import UsersActivity


class UserCRUD(BaseCRUD[User]):
    async def create(self, vk_id: int) -> User:
        user = User(vk_id=vk_id)  # noqa
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get(self, vk_id: int) -> User:
        stmt = select(User).where(User.vk_id == vk_id)
        query = await self.session.execute(stmt)
        return query.scalar_one_or_none()

    async def user_exists(self, vk_id: int):
        user = await self.get(vk_id)
        return user is None

    async def update_group(self, vk_id: int, group_number: int) -> User:
        stmt = update(User).where(User.vk_id == vk_id).values(group_index=group_number)
        await self.session.execute(stmt)
        await self.session.commit()

        return await self.get(vk_id=vk_id)

    async def mark_last_activity(self, vk_id: str):
        sql = update(User).where(User.vk_id == vk_id).values(last_activity=datetime.now())
        await self.session.execute(sql)
        await self.session.commit()

    async def get_daily_users(self) -> int:
        sql = text("SELECT count(*) FROM users WHERE last_activity >= NOW() - INTERVAL '1 day'")
        query = await self.session.execute(sql)
        return query.scalar_one_or_none()

    async def get_usercount_by_grade(self) -> RowMapping:
        first_grade = (
            select(func.count())
            .select_from(User)
            .where(and_(User.group_index > 100, User.group_index < 200))
            .label("Первый курс")
        )
        second_grade = (
            select(func.count())
            .select_from(User)
            .where(and_(User.group_index > 200, User.group_index < 300))
            .label("Второй курс")
        )
        third_grade = (
            select(func.count())
            .select_from(User)
            .where(and_(User.group_index > 300, User.group_index < 400))
            .label("Третий курс")
        )
        fourth_grade = (
            select(func.count())
            .select_from(User)
            .where(and_(User.group_index > 400, User.group_index < 500))
            .label("Четвёртый курс")
        )
        fifth_grade = (
            select(func.count())
            .select_from(User)
            .where(and_(User.group_index > 500, User.group_index < 600))
            .label("Пятый курс")
        )

        stmt = select(first_grade, second_grade, third_grade, fourth_grade, fifth_grade)
        query = await self.session.execute(stmt)
        return query.mappings().first()

    async def get_usercount_by_groups(self) -> Sequence[RowMapping]:
        stmt = text(
            "select u.group_index, count(*) from users u "
            "group by u.group_index order by u.group_index"
        )

        query = await self.session.execute(stmt)
        return query.mappings().all()

    async def get_daily_users_by_day(self) -> List[UsersActivity]:
        sql = select(UsersActivity)
        query = await self.session.execute(sql)
        return list(query.scalars())

    async def record_daily_users(self):
        count = await self.get_daily_users()
        self.session.add(UsersActivity(user_count=count))
        await self.session.commit()

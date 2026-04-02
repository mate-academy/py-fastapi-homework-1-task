from fastapi import Request
from sqlalchemy import func, select, Select
from sqlalchemy.ext.asyncio import AsyncSession


class Paginator:
    def __init__(
            self,
            query: Select,
            page: int,
            per_page: int,
            request: Request,
            db: AsyncSession
    ):
        self.db = db
        self.query = query
        self.page = page
        self.per_page = per_page
        self.request = request
        self.total_pages = 0

    def _get_total_pages(self, count: int) -> int:
        rest = count % self.per_page
        quotient = count // self.per_page
        return quotient if not rest else quotient + 1

    async def _get_total_items(self) -> int:
        count = await self.db.scalar(select(func.count()).select_from(self.query.subquery()))
        self.total_pages = self._get_total_pages(count)
        return count

    async def _get_items(self):
        paginated_items = self.query.offset((self.page - 1) * self.per_page).limit(self.per_page)
        result = await self.db.execute(paginated_items)
        return result.scalars().all()

    def get_next_page(self) -> str | None:
        if self.page >= self.total_pages:
            return None
        next_page = self.request.url.include_query_params(page=self.page + 1)
        return str(next_page)

    def get_previous_page(self) -> str | None:
        if self.page == 1 or self.page > self.total_pages + 1:
            return None
        prev_page = self.request.url.include_query_params(page=self.page - 1)
        return str(prev_page)

    async def get_response(self) -> dict:
        total_items = await self._get_total_items()
        items = await self._get_items()
        return {
            "items": items,
            "total_items": total_items,
            "prev_page": self.get_previous_page(),
            "next_page": self.get_next_page(),
            "total_pages": self.total_pages,
        }


async def paginate(*args, **kwargs):
    paginator = Paginator(*args, **kwargs)
    return await paginator.get_response()

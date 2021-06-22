
from aiounittest import AsyncTestCase
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from viewsdocs import dals, models

class TestPageDal(AsyncTestCase):
    async def create_metadata(self,engine):
        async with engine.begin() as con:
            await con.run_sync(models.Base.metadata.create_all)

    async def test_async_basic(self):
        engine = create_async_engine("sqlite+aiosqlite:///:memory:")
        await self.create_metadata(engine)
        async with sessionmaker(engine, class_ = AsyncSession)() as session:
            pages = dals.PageDal(session)

            await pages.add("alpha","beta","gamma")
            await session.commit()

            page_list = await pages.list()
            self.assertEqual(len(page_list), 1)

            content = await pages.content("alpha","beta")
            self.assertEqual(content, "gamma")

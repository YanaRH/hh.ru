from src.database import Database
import asyncio


class DBManager:
    def __init__(self):
        self.db = Database()

    async def init(self):
        await self.db.init_pool()

    async def get_companies_and_vacancies_count(self) -> list:
        async with self.db.pool.acquire() as conn:
            return await conn.fetch("""
                SELECT 
                    c.name as company,
                    COUNT(v.id) as vacancies_count
                FROM companies c
                LEFT JOIN vacancies v ON c.id = v.company_id
                GROUP BY c.id, c.name
                ORDER BY vacancies_count DESC
            """)

    async def get_all_vacancies(self) -> list:
        async with self.db.pool.acquire() as conn:
            return await conn.fetch("""
                SELECT 
                    c.name as company,
                    v.name as vacancy,
                    v.salary,
                    v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.id
                ORDER BY v.created_at DESC
            """)

    async def get_avg_salary(self) -> float:
        async with self.db.pool.acquire() as conn:
            result = await conn.fetchrow("SELECT AVG(salary) as avg FROM vacancies WHERE salary IS NOT NULL")
            return result['avg'] or 0

    async def get_vacancies_with_higher_salary(self) -> list:
        async with self.db.pool.acquire() as conn:
            avg = await self.get_avg_salary()
            return await conn.fetch("""
                SELECT 
                    c.name as company,
                    v.name as vacancy,
                    v.salary,
                    v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.id
                WHERE v.salary > $1
                ORDER BY v.salary DESC
            """, avg)

    async def get_vacancies_with_keyword(self, keyword: str) -> list:
        async with self.db.pool.acquire() as conn:
            return await conn.fetch("""
                SELECT 
                    c.name as company,
                    v.name as vacancy,
                    v.salary,
                    v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.id
                WHERE LOWER(v.name) LIKE $1 OR LOWER(v.description) LIKE $1
            """, f'%{keyword.lower()}%')

    async def close(self):
        await self.db.close()
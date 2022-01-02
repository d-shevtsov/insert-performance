from datetime import datetime

from asyncpg import Pool


class Storage:
    connection_pool: Pool

    def __init__(self, connection_pool: Pool):
        self.connection_pool = connection_pool

    async def create_task_data(self, record_id: int, step_id: int, data: str):
        async with self.connection_pool.acquire() as connection:
            # async with connection.transaction():
            await connection.execute(
                '''
                INSERT INTO task_data(
                    record_id,
                    step_id,
                    data)
                VALUES ($1, $2, $3)
                ''',
                record_id,
                step_id,
                data
            )

    async def create_1000_tasks_data(self, tasks: []):
        async with self.connection_pool.acquire() as connection:
            # async with connection.transaction():
            await connection.executemany(
                '''
                INSERT INTO task_data(
                    record_id,
                    step_id,
                    data)
                VALUES ($1, $2, $3)
                ''',
                tasks
            )

    async def initialize(self):
        async with self.connection_pool.acquire() as connection:
            await connection.execute('''
            CREATE TABLE IF NOT EXISTS task_data(
                id SERIAL PRIMARY KEY,
                record_id bigint,
                step_id bigint,
                data text
                )
            ''')


        async with self.connection_pool.acquire() as connection:
            await connection.execute("CREATE INDEX IF NOT EXISTS task_data_index on task_data(id)")
            #
            # await connection.execute(
            #     "CREATE INDEX IF NOT EXISTS farmer_update_history_launcher_id_idx on farmer_update_history(launcher_id)")
            #
            # await connection.execute("CREATE INDEX IF NOT EXISTS partial_launcher_id_idx on partial(launcher_id)")
            # await connection.execute("CREATE INDEX IF NOT EXISTS partial_timestamp_idx on partial(timestamp)")
            # await connection.execute(
            #     "CREATE UNIQUE INDEX IF NOT EXISTS partial_unique_proof_of_space_idx on partial(challenge, plot_public_key, proof)")
            #
            # await connection.execute("CREATE INDEX IF NOT EXISTS partial_error_launcher_id_idx on partial_error(launcher_id)")
            # await connection.execute("CREATE INDEX IF NOT EXISTS partial_error_timestamp_idx on partial_error(timestamp)")

start: pipenv run uvicorn app.main:app --reload

alembic: https://alembic.sqlalchemy.org/en/latest/tutorial.html#the-migration-environment

redis-queue: https://python-rq.org/

redis: https://redis.io/topics/quickstart

run rq: nohup pipenv run rq worker </dev/null &>/dev/null &
from sqlalchemy.orm import Session

from app.logger import AppLog
from app.services import users as users_service


def check_point(db: Session, user: any):
    check_result = users_service.check_user_rank(db, user)
    if ~check_result:
        # write log
        AppLog('users').error(f'User {user.username} can not be checked to update rank')
    return

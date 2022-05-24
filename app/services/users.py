from sqlalchemy.orm import Session

from app.constants import USER_RANK_POINT


def check_user_rank(db: Session, current_user: any):
    try:
        current_point = current_user.accumulated_points
        current_rank = current_user.rank

        if 0 <= current_point <= USER_RANK_POINT.get("Đồng"):  # 0 - 1000
            if current_rank != "Đồng":
                current_user.rank = "Đồng"
                db.commit()

        elif USER_RANK_POINT.get("Đồng") + 1 <= current_point <= USER_RANK_POINT.get("Bạc"):  # 1001 - 5000
            if current_rank != "Bạc":
                current_user.rank = "Bạc"
                db.commit()

        elif USER_RANK_POINT.get("Bạc") + 1 <= current_point <= USER_RANK_POINT.get("Vàng"):  # 5001 - 10000
            if current_rank != "Vàng":
                current_user.rank = "Vàng"
                db.commit()

        elif current_point > USER_RANK_POINT.get("Vàng"):  # > 10000
            if current_rank != "Kim Cương":
                current_user.rank = "Kim Cương"
                db.commit()

        return True

    except Exception as e:
        return False

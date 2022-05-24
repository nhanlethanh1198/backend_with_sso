from datetime import datetime
from functools import partial

from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app import models

from app.schemas import staff_schemas


def get_staff_info(db: Session, staff_id: int):
    result = db.query(models.Staff).filter(models.Staff.id == staff_id).first()
    return result


def staff_login(db: Session, phone: str, hash_password: str):
    staff = db.query(models.Staff).filter(models.Staff.phone ==
                                          phone, models.Staff.hash_password == hash_password).first()
    return staff


def get_staff_list(db: Session):
    list = db.query(models.Staff).order_by(
        desc(models.Staff.join_from_date)).all()
    return list


def user_get_staff_list(db: Session, limit: int):
    db_staff_list = db.query(
        models.Staff.id,
        models.Staff.fullname,
        models.Staff.phone,
        models.Staff.address,
        models.Staff.avatar_img,
        models.Staff.join_from_date,
        models.Staff.working_count,
        models.Staff.vote_count,
        models.Staff.vote_average_score
    ).filter(
        models.Staff.is_active == True,
        models.Staff.role == 'staff'
    ).order_by(
        models.Staff.join_from_date.asc(),
        models.Staff.working_count.desc()
    ).limit(limit).all()
    return db_staff_list


def add_staff(db: Session, data: dict):
    data.pop('password', None)

    db_staff = models.Staff(
        **data,
        status=1,
        is_active=True,
        join_from_date=datetime.now(),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff


def update_staff_info(db: Session, staff_id: int, data: dict):
    if 'password' in data:
        data.pop('password', None)

    db_staff = db.query(models.Staff).filter(models.Staff.id == staff_id).first()

    for key, value in data.items():
        if value is not None:
            setattr(db_staff, key, value)

    db.commit()
    db.refresh(db_staff)
    return db_staff

    db.commit()
    db.refresh(db_staff)
    return db_staff


def get_staff_by_phone(db: Session, phone: str):
    staff = db.query(models.Staff).filter_by(phone=phone).first()
    return staff


def add_staff_vote(db: Session, staff_id: int, user_id: int, vote: staff_schemas.VoteStaff):
    # Update Vote to Staff Table
    vote_score = vote.vote_score
    tags = vote.tags

    current_staff = db.query(models.Staff).filter_by(id=staff_id).first()

    current_staff.vote_count += 1

    for tag in tags:
        if (tag == 'good_skill'):
            current_staff.skill_score_count += 1
            current_staff.skill_average_score = (
                                                        current_staff.skill_score_count // current_staff.vote_count) * 10
        if (tag == 'good_attitude'):
            current_staff.attitude_score_count += 1
            current_staff.attitude_average_score = (
                                                           current_staff.attitude_score_count // current_staff.vote_count) * 10
        if (tag == 'good_job'):
            current_staff.contentment_score_count += 1
            current_staff.contentment_average_score = (
                                                              current_staff.contentment_score_count // current_staff.vote_count) * 10

    def update_vote_one_star():
        current_staff.vote_one_star_count += 1
        return True

    def update_vote_two_star():
        current_staff.vote_two_star_count += 1
        return True

    def update_vote_three_star():
        current_staff.vote_three_star_count += 1
        return True

    def update_vote_four_star():
        current_staff.vote_four_star_count += 1
        return True

    def update_vote_five_star():
        current_staff.vote_five_star_count += 1
        return True

    def update_vote_count_case(score):
        # switch case
        switcher = {
            1: update_vote_one_star,
            2: update_vote_two_star,
            3: update_vote_three_star,
            4: update_vote_four_star,
            5: update_vote_five_star
        }

        # chay switch case voi score truyen vao
        func = switcher.get(score, False)
        return func()

    # Tinh so sao trung binh
    def calculate_average_vote_score():
        average_vote_score = (
                                     current_staff.vote_one_star_count * 1 +
                                     current_staff.vote_two_star_count * 2 +
                                     current_staff.vote_three_star_count * 3 +
                                     current_staff.vote_four_star_count * 4 +
                                     current_staff.vote_five_star_count * 5) / current_staff.vote_count
        return "{:.1f}".format(average_vote_score)

    def update_vote_in_staff(score):
        result = update_vote_count_case(score)
        if result:
            current_staff.vote_average_score = float(
                calculate_average_vote_score())
            current_staff.updated_at = datetime.now()
            db.commit()
            db.refresh(current_staff)
            return True
        else:
            return False

    updated_staff = update_vote_in_staff(vote_score)

    # Update Vote to User Table SuccessFully
    if (updated_staff):
        vote_data = vote.dict()
        # Add new Vote to Star_Staff Table
        db_staff_vote = models.StarStaff(
            staff_id=staff_id,
            user_id=user_id,
            **vote_data,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(db_staff_vote)
        db.commit()
        db.refresh(db_staff_vote)

        return db_staff_vote

    return False


def get_list_vote_of_staff(db: Session, staff_id: int):
    try:
        current_staff = jsonable_encoder(db.query(
            models.Staff.id,
            models.Staff.fullname,
            models.Staff.avatar_img,
            models.Staff.working_count,
            models.Staff.vote_count,
            models.Staff.skill_average_score,
            models.Staff.attitude_average_score,
            models.Staff.contentment_average_score,
            models.Staff.vote_average_score,
            models.Staff.vote_one_star_count,
            models.Staff.vote_two_star_count,
            models.Staff.vote_three_star_count,
            models.Staff.vote_four_star_count,
            models.Staff.vote_five_star_count,
        ).filter_by(id=staff_id).first())

        current_staff_vote_list = jsonable_encoder(db.query(
            models.StarStaff.id,
            models.User.fullname,
            models.StarStaff.vote_score,
            models.StarStaff.comment,
            models.StarStaff.tags,
            models.StarStaff.created_at,
            models.StarStaff.updated_at,
        ).outerjoin(models.User).filter(models.StarStaff.staff_id == staff_id).all())

    except Exception as e:
        print(e)
        return False

    return {
        **current_staff,
        'vote_list': current_staff_vote_list
    }


def get_vote_info_by_id(db: Session, vote_id: int):
    vote_info = db.query(
        models.StarStaff.id,
        models.User.fullname,
        models.StarStaff.vote_score,
        models.StarStaff.comment,
        models.StarStaff.tags,
        models.StarStaff.created_at,
        models.StarStaff.updated_at,
    ).outerjoin(models.User).filter(models.StarStaff.id == vote_id).first()
    return vote_info


def update_vote_info(db: Session, vote_id: int, user_id: int, vote: any):
    try:
        vote_score = vote.vote_score
        db_vote_info = db.query(models.StarStaff).get(vote_id)

        if (db_vote_info.user_id != user_id):
            return False

        previos_vote_score = db_vote_info.vote_score

        # Update Vote to User Table

        def update_score_in_product(vote_score, previous_vote_score):
            try:
                current_staff = db.query(models.Staff).get(
                    db_vote_info.staff_id)

                def update_vote_one_star(type: str):
                    if (type == 'add'):
                        current_staff.vote_one_star_count += 1
                    elif (type == 'sub'):
                        current_staff.vote_one_star_count -= 1
                    return True

                def update_vote_two_star(type: str):
                    if (type == 'add'):
                        current_staff.vote_two_star_count += 1
                    elif (type == 'sub'):
                        current_staff.vote_two_star_count -= 1
                    return True

                def update_vote_three_star(type: str):
                    if (type == 'add'):
                        current_staff.vote_three_star_count += 1
                    elif (type == 'sub'):
                        current_staff.vote_three_star_count -= 1
                    return True

                def update_vote_four_star(type: str):
                    if (type == 'add'):
                        current_staff.vote_four_star_count += 1
                    elif (type == 'sub'):
                        current_staff.vote_four_star_count -= 1
                    return True

                def update_vote_five_star(type: str):
                    if (type == 'add'):
                        current_staff.vote_five_star_count += 1
                    elif (type == 'sub'):
                        current_staff.vote_five_star_count -= 1
                    return True

                def update_vote_count_case(score: int, type: str):
                    # switch case
                    switcher = {
                        1: partial(update_vote_one_star, type),
                        2: partial(update_vote_two_star, type),
                        3: partial(update_vote_three_star, type),
                        4: partial(update_vote_four_star, type),
                        5: partial(update_vote_five_star, type)
                    }

                    # chay switch case voi score truyen vao
                    func = switcher.get(score, False)
                    return func()

                # Check vote_score and previous_vote_score is different
                # If different, update score in product

                if (vote_score != previous_vote_score):
                    try:
                        # Không chạy được switch case chỗ này
                        checkUpvote = update_vote_count_case(
                            score=vote_score, type='add')
                        checkDownVote = update_vote_count_case(
                            score=previous_vote_score, type='sub')

                        if (checkUpvote == True and checkDownVote == True):
                            # Tinh lai diem trung binh
                            average_vote_score = (
                                                         current_staff.vote_one_star_count * 1 +
                                                         current_staff.vote_two_star_count * 2 +
                                                         current_staff.vote_three_star_count * 3 +
                                                         current_staff.vote_four_star_count * 4 +
                                                         current_staff.vote_five_star_count * 5) / current_staff.vote_count
                            current_staff.vote_average_score = float(
                                "{:.1f}".format(average_vote_score))
                            db.commit()
                            db.refresh(current_staff)
                            return True

                        current_staff.vote_count_updated_at = datetime.now()

                        db.commit()
                        db.refresh(current_staff)
                    except Exception as e:
                        print(str(e))
                        return False
                return True

            except Exception as e:
                print(e)
                return False

        updated_staff = update_score_in_product(vote_score, previos_vote_score)

        if updated_staff:
            db_vote_info.vote_score = vote_score
            db_vote_info.comment = vote.comment
            db_vote_info.updated_at = datetime.now()
            db.commit()
            db.refresh(db_vote_info)

            return db_vote_info
    except Exception as e:
        print(e)
        return False


def staff_get_locations(db: Session, staff_id: int):
    return db.query(models.StaffLocation).filter_by(staff_id=staff_id).order_by(models.StaffLocation.updated_at).all()


def get_list_staff_with_high_star(db: Session, limit: int = 30):
    list_staff = db.query(models.Staff.id).order_by(models.Staff.vote_average_score.desc()).limit(limit).all()
    return list(map(lambda x: x['id'], list_staff))


def get_list_staff_by_list_id(db: Session, list_staff_id: List[int]):
    return db.query(models.Staff).filter(models.Staff.id.in_(list_staff_id)).all()

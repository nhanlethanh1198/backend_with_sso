from typing import Optional

from fastapi import APIRouter, Depends, Form
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import response_models
from app.database import get_db
from app.dependencies import random_number
from app.get_current_staff import get_current_staff, CurrentStaff
from app.get_current_user import get_current_user, CurrentUser
from app.repositories import combo
from app.schemas import combo_schemas
from app.upload_file_to_s3 import S3

router = APIRouter(
    prefix='/combo',
    tags=['Combo'],
    responses={404: {'description': 'Not Found'}}
)


@router.get('/user-get-combo-list', summary='User get list combo is_activating',
            response_model=response_models.ComboListResponse)
async def get_combo_list(limit: Optional[int] = 20, page: Optional[int] = 1, location: Optional[int] = None,
                         db: Session = Depends(get_db)):
    count_combo_list = combo.get_count_combo_list(db=db, location=location)

    total_page = count_combo_list // limit if count_combo_list % limit == 0 else count_combo_list // limit + 1
    offset = (page - 1) * limit
    results = combo.get_combo_list(db=db, limit=limit, offset=offset, location=location, is_active=True)

    return {
        "detail": "success",
        "data": results
    }


@router.get('/user-get-combo-by-id/{combo_id}', summary="User get combo by id",
            response_model=response_models.ComboDetailResponse)
async def get_combo_by_id(combo_id: int, db: Session = Depends(get_db)):
    current_combo = combo.get_combo_by_id(db=db, combo_id=combo_id)
    if not current_combo:
        return {
            "detail": "success",
            "data": current_combo
        }
    return {
        "detail": "error",
        "data": "Not Found combo with combo_id={}".format(combo_id),
    }


@router.get('/get-combo-list', summary='Staff get list all combo', response_model=response_models.ComboListResponse)
async def get_combo_list(db: Session = Depends(get_db), current_staff: CurrentStaff = Depends(get_current_staff)):
    results = combo.get_combo_list(db=db, limit=50)
    return {
        "detail": "success",
        "data": results
    }


@router.get('/get-combo-by-id/{combo_id}', response_model=response_models.ComboDetailResponse)
async def get_combo_by_id(combo_id: int, db: Session = Depends(get_db),
                          current_staff: CurrentStaff = Depends(get_current_staff)):
    current_combo = combo.get_combo_by_id(db=db, combo_id=combo_id)

    if current_combo is not None:
        return {
            "detail": "success",
            "data": current_combo
        }
    else:
        return {
            "detail": "error",
            "data": "Not Found combo with combo_id={}".format(combo_id),
        }


@router.post('/create-combo', response_model=response_models.HandleComboResponse)
async def create_combo(form: combo_schemas.ComboCreate = Depends(combo_schemas.ComboCreate.as_form),
                       db: Session = Depends(get_db),
                       current_staff: CurrentStaff = Depends(get_current_staff)):
    if len(form.products) == 0:
        return {
            'detail': 'error',
            'message': 'Bạn chưa thêm sản phẩm vào combo'
        }

    # handle file upload
    s3 = S3()
    url_img = None
    if form.image is not None:
        path_file = 'combos/images/{}'.format(form.image.filename)
        url_img = s3.upload_file_to_s3(form.image, path_file)

    data = {
        **form.dict(),
        'code': await random_number(6),
        'image': url_img,
    }

    new_combo = combo.create_combo(db=db, data=data)

    return {
        "detail": "success",
        "data": new_combo,
    }


@router.put('/update-combo-by-id/{combo_id}', response_model=response_models.HandleComboResponse)
async def update_combo(combo_id: int, form: combo_schemas.ComboUpdate = Depends(combo_schemas.ComboUpdate.as_form),
                       db: Session = Depends(get_db), current_staff: CurrentStaff = Depends(get_current_staff)):
    data = {
        **form.dict(),
    }
    # Handle file upload
    if form.image is not None:
        s3 = S3()
        path_file = 'combos/images/{}'.format(form.image.filename)
        url_img = s3.upload_file_to_s3(form.image, path_file)

        data = {
            **form.dict(),
            'image': url_img,
        }

    return {
        "detail": "success",
        "data": combo.update_combo_by_id(db=db, combo_id=combo_id, data=data)
    }


@router.put('/active-combo/{combo_id}')
async def active_combo_by_id(combo_id: int, is_active: bool = Form(...), db: Session = Depends(get_db),
                             current_staff: CurrentStaff = Depends(get_current_staff)):
    current_combo = combo.active_combo_by_id(
        db=db, combo_id=combo_id, is_active=is_active)
    return {
        "detail": "success",
        "data": current_combo
    }


# Gợi ý combo
@router.get('/get-suggest-combo/{combo_id}', summary="Gợi ý combo", response_model=response_models.ComboListResponse,
            description='Lọc combo bằng cách tìm kiếm combo khác combo_id gửi lên')
async def get_suggest_combo(combo_id: int, db: Session = Depends(get_db)):
    suggest_combo_list = combo.get_suggest_combo(db=db, combo_id=combo_id)
    return {
        'detail': 'success',
        'data': suggest_combo_list
    }


# Vote

# Add new Vote


@router.post('/vote/{combo_id}', tags=['Combo Vote'], response_model=response_models.HandleVoteResponse)
async def add_vote_to_combo(combo_id: int, vote: combo_schemas.AddVoteCombo, db: Session = Depends(get_db),
                            current_user: CurrentUser = Depends(get_current_user)):
    try:
        data = jsonable_encoder(vote)
        user_id = current_user.user_id

        results = combo.add_combo_vote(combo_id=combo_id, user_id=user_id, data=data, db=db)
        return {"detail": "success"} if results else {"detail": "false"}
    except Exception as e:
        print(e)
        return {
            "detail": "error",
            "error": str(e)
        }


# Update Vote by Vote Id


@router.put('/vote/id/{vote_id}', tags=['Combo Vote'], summary="Update Vote in Combo By Combo_Id",
            response_model=response_models.HandleVoteResponse)
async def update_vote_to_combo(vote_id: int, vote: combo_schemas.AddVoteCombo, db: Session = Depends(get_db),
                               current_user: CurrentUser = Depends(get_current_user)):
    user_id = current_user.user_id
    updated_combo = combo.update_combo_vote(vote_id=vote_id, user_id=user_id, data=vote, db=db)
    return {"detail": "success"} if updated_combo else {"detail": "false"}


# Get Vote List by Combo ID
@router.get('/vote/{combo_id}', tags=['Combo Vote'], summary="Get Vote List in Combo By Combo_Id",
            response_model=response_models.VoteListInComboResponse)
async def get_list_vote_in_combo(combo_id: int, db: Session = Depends(get_db)):
    results = combo.get_list_vote_in_combo(combo_id=combo_id, db=db)
    return {
        "detail": "success",
        "data": results
    }


# Get Vote Info by Vote ID


@router.get('/vote/id/{vote_id}', tags=['Combo Vote'], summary="Get Vote Info in Combo By Vote_Id",
            response_model=response_models.VoteInfoByVoteIdResponse)
async def get_vote_info_by_vote_id(vote_id: int, db: Session = Depends(get_db)):
    results = combo.get_vote_info_by_vote_id(vote_id=vote_id, db=db)
    return {
        "detail": "success",
        "data": results
    }

from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from models import TokenData, PassInfo, NotFoundException, PassFileCreationReq
from auth import get_token_info
from rsuty_pstore_service import get_names, get_pass_info, add_pass, init_pass_file

pass_store_router = APIRouter(
    prefix='/pass',
    tags=['pass']
)

@pass_store_router.put('/init')
async def init_client_pass(
    data: PassFileCreationReq, 
    authenticated_client: Annotated[TokenData, Depends(get_token_info)]
):
    print(f'{authenticated_client.client_id} creating new client pass file: {data.client_id}')
    try:
        success = init_pass_file(data.client_id, data.password)

        if success is True:
            return True
        
        raise RuntimeError(f'non success when creating client file for {data.client_id}. response {success}')
    except Exception as e:
        print(f"error creating pass file for {data.client_id}. {str(e)}")
        return HTTPException(
            status_code=500,
            detail='Internal Server Error'
        )

@pass_store_router.get('/names')
async def get_pass_names(authenticated_client: Annotated[TokenData, Depends(get_token_info)]):
    print(f'getting pass names for {authenticated_client.client_id}')
    return get_names(authenticated_client)

@pass_store_router.get('/{name}')
async def get_pass(name: str, authenticated_client: Annotated[TokenData, Depends(get_token_info)]):
    print(f'getting pass info {name} for {authenticated_client.client_id}')
    try:
        return get_pass_info(authenticated_client, name)
    except NotFoundException:
        return HTTPException(
            status_code=404,
            detail='Resource not found'
        )
    except Exception:
        return HTTPException(
            status_code=500,
            detail='Internal Server Error'
        )

@pass_store_router.post('')
async def put_pass_info(data: PassInfo, authenticated_client: Annotated[TokenData, Depends(get_token_info)]):
    name = data.name
    username = data.username
    password = data.password
    url = data.url

    print(f'adding password {name} for {authenticated_client.client_id}')
    try:
        return add_pass(authenticated_client, name, username, password, url)
    except Exception  as e:
        print(f'Error saving pass details {str(e)}')
        return HTTPException(
            status_code=500,
            detail='Internal Server Error'
        )
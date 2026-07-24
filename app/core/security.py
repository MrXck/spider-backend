from fastapi import HTTPException, status, Depends, Request, Response

from app.utils.jwt_utils import parse_payload, create_token


def get_current_user(request: Request, response: Response):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="缺少或无效的 Authorization Header"
        )

    data = parse_payload(token)

    if not data['status']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="登录过期"
        )

    user_id = data['data']['data']
    response.headers["Authorization"] = create_token(user_id)
    return {
        'user_id': user_id
    }


RequireLogin = Depends(get_current_user)

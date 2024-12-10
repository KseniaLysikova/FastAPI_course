from fastapi import HTTPException, status


def with_errors(*errors: HTTPException):
    errors_data = {}
    for err in errors:
        if err.status_code in errors_data:
            errors_data[err.status_code]["description"] += f"\n\n{err.detail}"
        else:
            errors_data[err.status_code] = {"description": err.detail}
    return errors_data


def invalid_credentials():
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Invalid credentials")


def token_validation_failed():
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Token validation failed")


def unauthorized():
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Unauthorized")


def token_expired():
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Token expired")


def invalid_token():
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                         detail="Invalid token")


def incorrect_password():
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                         detail="Incorrect password")


def project_not_found():
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail="Project not found")


def project_user_exists():
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                         detail="User is already an attendant in this project")


def invalid_project_user_id():
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                         detail="Invalid project_id or user_id")


def user_not_in_project():
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                         detail="User is not an attendant in this project")


def user_not_found():
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail="User not found")


def user_already_exists():
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                         detail="User already exists")


def email_format_error():
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                         detail="Email must contain @")


def request_not_found():
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail="Request not found")

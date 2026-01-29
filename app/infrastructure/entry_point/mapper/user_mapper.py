from app.domain.model.user import User
from app.infrastructure.entry_point.dto.user_dto import UserResponse


class UserDTOMapper:
    
    @staticmethod
    def to_response(user: User) -> UserResponse:
        return UserResponse(
            id=user.id,
            name=user.name,
            lastName=user.last_name,
            email=user.email,
            token=user.token
        )

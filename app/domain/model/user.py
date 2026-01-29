"""User domain model"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    
    id: str
    name: str
    last_name: str
    email: str
    password: str
    token: Optional[str] = None
    
    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("User ID (cedula) is required")
        if not self.email or "@" not in self.email:
            raise ValueError("Valid email is required")
        if not self.name:
            raise ValueError("Name is required")
        if not self.last_name:
            raise ValueError("Last name is required")
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "lastName": self.last_name,
            "email": self.email,
        }
    
    def to_dict_with_token(self) -> dict:
        data = self.to_dict()
        if self.token:
            data["token"] = self.token
        return data

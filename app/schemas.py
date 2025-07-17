from pydantic import BaseModel, EmailStr, create_model, validator
from typing import Any, Dict, List, Optional, Type
from fastapi import HTTPException


def build_model_from_schema(fields: List[Dict[str, Any]]) -> Type[BaseModel]:
    model_fields = {}

    for field in fields:
        field_name = field["name"]
        field_type = field["type"]
        required = field.get("required", False)

        # Map frontend type to Pydantic type
        if field_type == "email":
            pyd_type = EmailStr
        elif field_type == "number":
            pyd_type = Optional[int] if not required else int
        elif field_type == "text" or field_type == "password":
            pyd_type = Optional[str] if not required else str
        elif field_type == "dropdown":
            pyd_type = Optional[str] if not required else str
        else:
            pyd_type = Any  # fallback

        default = ... if required else None
        model_fields[field_name] = (pyd_type, default)

    # Create Pydantic model dynamically
    return create_model("DynamicForm", **model_fields)
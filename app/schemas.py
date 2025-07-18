from pydantic import BaseModel, EmailStr, create_model, validator
from typing import Any, Dict, List, Optional, Type
from fastapi import HTTPException


def build_model_from_schema(fields: List[Dict[str, Any]]) -> Type[BaseModel]:
    model_fields = {}

    for field in fields:
        name = field["name"]
        field_type = field["type"]

        if field_type == "email":
            model_fields[name] = (str, None)
        elif field_type == "number":
            model_fields[name] = (int, None)
        else:
            model_fields[name] = (str, None)

    return create_model("DynamicForm", **model_fields)

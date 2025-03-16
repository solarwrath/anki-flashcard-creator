from typing import Any

from pydantic import BaseModel


class ConfiguredPydanticBaseModel(BaseModel):
    model_config = {"arbitrary_types_allowed": True}  # Prevents automatic validation
    _validated: bool = False  # Flag to track validation

    def __init__(self, **data):
        """Bypass Pydantic validation at initialization."""
        object.__setattr__(self, "__dict__", data)  # Store raw, unvalidated data
        object.__setattr__(self, "_validated", False)  # Mark as unvalidated
        object.__setattr__(self, "__pydantic_extra__", None)  # Prevent attribute errors

    def validate(self):
        """Manually validates the model and updates attributes."""
        if object.__getattribute__(self, "_validated"):  # Prevent redundant validation
            return

        validated = self.model_validate(self.__dict__)  # Perform validation
        object.__setattr__(self, "__dict__", validated.__dict__)  # Replace raw data
        object.__setattr__(self, "_validated", True)  # Mark as validated

    def __getattribute__(self, name: str) -> Any:
        """Lazy validation: Trigger validation only on first attribute access."""
        if name not in {"_validated", "validate", "__dict__", "__class__", "__pydantic_extra__"}:
            if not object.__getattribute__(self, "_validated"):  # Safe access
                object.__setattr__(self, "_validated", True)  # Prevent recursion loop
                self.validate()

        return object.__getattribute__(self, name)
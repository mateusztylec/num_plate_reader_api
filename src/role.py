from .logs import logger

class SingleRole:
    def __init__(self, name: str, id: int, description: str):
        self.name = name
        self.id = id
        self.description = description


class Role:
    GUEST = SingleRole(name="GUEST", 
                       id="0", 
                       description="Guest account")
    USER = SingleRole(name="USER", 
                       id="1", 
                       description="Normal user account")
    ADMIN = SingleRole(name="ADMIN", 
                       id="2", 
                       description="Admin account")

    @classmethod
    def attributes(cls) -> list[SingleRole]:
        return [val for key, val in vars(cls).items() if not (key.startswith("__") or key == "attributes")]
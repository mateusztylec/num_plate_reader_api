class Role:
    GUEST = {
        "name": "GUEST",
        "description": "Guest account"
    }
    USER = {
        "name": "USER",
        "description": "Normal user account"
    }
    ADMIN = {
        "name": "ADMIN",
        "description": "Admin account"
    }

    def __getattr__(self, name):
        if name in self.GUEST:
            return self.GUEST[name]
        elif name in self.USER:
            return self.USER[name]
        elif name in self.ADMIN:
            return self.ADMIN[name]
        else:
            raise AttributeError(
                f"{self.__class__.__name__} object has no attribute '{name}'")

class MaskHandler:
    @staticmethod
    def mask_username(username: str) -> str:
        if len(username) <= 2:
            return '*' * len(username)
        return username[0] + '*' * (len(username) - 2) + username[-1]
class ValidationException(Exception):
    def __init__(self):
        super().__init__(f"The audit doesn't contain required section.")

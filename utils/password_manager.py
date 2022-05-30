from flask_bcrypt import generate_password_hash, check_password_hash

from re import match

from .constants import PASSWORD_REGEX, HASH_ROUNDS


class PasswordManager:
    class Meta:
        abstract = True

    def set_password(self, password: str) -> str:
        """
        Sets user password.
        :param password: string value, longer than 8 characters
        :return: boolean value
        """
        if not self._validate_password(password=password):
            return
        self.password = password
        self.__update__password__()
        return self.password

    def _validate_password(self, password: str) -> bool:
        """
        Checks if password is valid.
        :param password: string value, longer than 8 characters
        :return: boolean value
        """
        return match(PASSWORD_REGEX, password)

    def verify_password(self, password: str) -> bool:
        """
        Checks user password.
        :param password: string value, longer than 8 characters
        :return: boolean value
        """
        return self.__check_password_hash__(password=password)

    def serialize(self) -> dict:
        return {
            'full_name': self.full_name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }

    def __update__password__(self):
        """ Updates the password field of the user. """
        self.password = self.__generate_password_hash__()

    def __generate_password_hash__(self) -> str:
        return generate_password_hash(password=self.password, rounds=HASH_ROUNDS).decode('utf-8')

    # Use documentation from BCrypt for password hashing
    __generate_password_hash__.__doc__ = generate_password_hash.__doc__

    def __check_password_hash__(self, password: str) -> bool:
        return check_password_hash(pw_hash=self.password, password=password)
    # Use documentation from BCrypt for password hashing
    __check_password_hash__.__doc__ = check_password_hash.__doc__

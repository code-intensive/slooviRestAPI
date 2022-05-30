from mongoengine import (
    Document, EmailField,
    StringField
)

from utils.constants import EMAIL_REGEX
from utils.password_manager import PasswordManager


class User(Document, PasswordManager):
    """ MongoDB ODM for the User document"""
    user_id = StringField(required=True, max_length=50, min_length=24, unique=True)
    first_name = StringField(required=True, max_length=50, unique=False)
    last_name = StringField(required=True, max_length=50, unique=False)
    email = EmailField(required=True, unique=True,
                       max_length=50, regex=EMAIL_REGEX)
    password = StringField(required=True, max_length=128)
        
    @property
    def full_name(self) -> str:
        return F'{self.first_name} {self.last_name}'.title()
    
    def email_is_unique(self):
        return User.objects.filter(email=self.email).first() is None
    
    def save(self, *args, **kwargs):
        # Overwrite Document save method to generate password hash prior to saving
        self.__update__password__()
        super(User, self).save(*args, **kwargs)


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
	def create_user(self, email, name, number , password=None):
		if not email:
			raise ValueError('Email must be provided!')
		if not password:
			raise ValueError('Password can not be empty!')
		if not name:
			raise ValueError('Name can not be empty!')
		user = self.model(email=email,name=name,number=number)
		user.set_password(password)
		user.save(using=self._db)
		return user

class User(AbstractBaseUser):
	email = models.EmailField(max_length=255, unique=True, null=True)
	admin = models.BooleanField(default=False)
	staff = models.BooleanField(default=False)
	active = models.BooleanField(default=True)
	name = models.CharField(max_length=255,null=False)
	number = models.CharField(max_length=10,null=False)
	# print("email",email)
	objects = UserManager()

	USERNAME_FIELD = 'number'
	REQUIRED_FIELDS = []

	def __str__(self, *args, **kwargs):
		return self.email

	@property
	def is_active(self, *args, **kwargs):
		return self.active
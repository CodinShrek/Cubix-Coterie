from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager # Imports the standard Django classes # 
from django.core.validators import MinValueValidator, MaxValueValidator # Imports the validators to check student's grade #

class MyAccountManager(BaseUserManager):
    def create_user(self, username, firstname, lastname, grade, email, password=None):
            if not username: # This ensures that the username field is filled in #
                raise ValueError("Username is required to create an account")
            if not email: # This ensures that the student's email ID is filled in #
                raise ValueError("An Email Address is required to create an account")
            if not firstname: # This ensures that the student's first name is provided #
                raise ValueError("Name Details are required to create an account")
            if not lastname: # This ensures that the student's last name is provided #
                raise ValueError("Name Details are required to create an account")
            if not grade: # This ensures that the student's grade is provided #
                raise ValueError("User's Grade is required to create an account")
            
            user = self.model(
                email = self.normalize_email(email), # Normalize the email address (e.g., lowercase) #
                username=username,
                grade = grade,
                firstname = firstname,
                lastname = lastname
                )
            
            # Set the password for the user (hashed internally) #
            user.set_password(password)
            
            # Save the user object to the database using the defined database connection #
            user.save(using=self._db)
            return user
        
    def create_superuser(self, username, email, firstname, lastname, grade, password):
        user = self.create_user(
            email = self.normalize_email(email),
            password=password,
            username=username,
            grade = grade,
            firstname = firstname,
            lastname = lastname
        )
       
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
                


class Account(AbstractBaseUser):
    username                = models.CharField(verbose_name =("Username"), max_length=50, unique=True) # Ensures that no two usernames are the same #
    email                   = models.EmailField(verbose_name =("Email"), max_length=254, unique=True) # Ensures that email IDs are not re-used #
    date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin				= models.BooleanField(default=False) # Ensures that students who register do not gain admin access #
    is_active				= models.BooleanField(default=True)
    is_staff				= models.BooleanField(default=False)
    is_superuser			= models.BooleanField(default=False)
    firstname              = models.CharField(max_length=100)
    lastname               = models.CharField(max_length=100)
    grade                   = models.IntegerField(
        validators=[
            MinValueValidator(6), # Grades below 6 cannot register #
            MaxValueValidator(12) # Grade 12 is the highest grade that can register #
        ]
    )
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','firstname', 'lastname', 'grade']
    
    objects = MyAccountManager()
    
    def __str__(self):
        return self.username
        return self.email
        return self.firstname
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
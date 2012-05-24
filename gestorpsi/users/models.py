from django.contrib.auth.models import User
class Users(User):
    
    class Meta:
        permissions = (
            ("user_list", "Can list user"),
        )
        

# Create your models here.

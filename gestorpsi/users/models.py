from django.contrib.auth.models import User
class Users(User):
    
    class Meta:
        permissions = (
            ("user_add", "Can add users"),
            ("user_change", "Can change users"),
            ("user_list", "Can list users"),
            ("user_write", "Can write users"),
        )
        

# Create your models here.

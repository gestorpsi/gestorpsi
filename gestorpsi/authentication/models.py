from django.db import models
from gestorpsi.organization.models import Organization
from django.contrib.auth.models import User, UserManager

class CustomUser(User):
    organization = models.ForeignKey(Organization, null=True)
    try_login = models.IntegerField(null=True)
    
    # Use UserManager to get the create_user method, etc.
    objects = UserManager()

    
    
    
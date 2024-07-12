from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import *

def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)
        Customer.objects.create(
            user=instance,
            name=instance.username,
            email=instance.email,
        )
        
post_save.connect(customer_profile, sender=User)     



def update_user_from_customer(sender, instance, created, **kwargs):
    if not created:  
        user = instance.user 
        if user:
            user.username = instance.name  
            user.email = instance.email  
            user.save()


post_save.connect(update_user_from_customer, sender=Customer) 

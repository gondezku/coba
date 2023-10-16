from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

class member(models.Model):
    name = models.CharField(max_length=30)
    shift = models.IntegerField()
    status = models.IntegerField(default=0) 
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class site(models.Model):
    name = models.TextField(max_length=50)
    sub_name = models.TextField(max_length=50, default='')
    Other = 1
    PumpCashing = 2
    MotorCashing = 3
    JetPump = 4
    Rotor = 5
    Finishing_PC = 6
    Finishing_MC = 7
    Impeller = 8
    Stator = 9
    Assy = 10
    Final_Inspection = 11
    AIDA_DieCast = 12
      
    ROLE_CHOICES = (
          (Other, 'Others'),
          (PumpCashing, 'Pump Cashing'),
          (MotorCashing, 'Motor Cashing'),
          (JetPump, 'Jet Pump'),
          (Rotor, 'Rotor'),
          (Finishing_PC, 'Finishing_PC'),
          (Finishing_MC, 'Finishing_MC'),
          (Impeller, 'Impeller'),
          (Stator, 'Stator'),
          (Assy, 'Assy'),
          (Final_Inspection, 'Final Inspection'),
          (AIDA_DieCast, 'AIDA-DieCast'),
    )
    section = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True,default=1)
    
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Other = 1
    PumpCashing = 2
    MotorCashing = 3
    JetPump = 4
    Rotor = 5
    Finishing_PC = 6
    Finishing_MC = 7
    Impeller = 8
    Stator = 9
    Assy = 10
    Final_Inspection = 11
    AIDA_DieCast = 12
      
    ROLE_CHOICES = (
          (Other, 'Others'),
          (PumpCashing, 'Pump Cashing'),
          (MotorCashing, 'Motor Cashing'),
          (JetPump, 'Jet Pump'),
          (Rotor, 'Rotor'),
          (Finishing_PC, 'Finishing_PC'),
          (Finishing_MC, 'Finishing_MC'),
          (Impeller, 'Impeller'),
          (Stator, 'Stator'),
          (Assy, 'Assy'),
          (Final_Inspection, 'Final Inspection'),
          (AIDA_DieCast, 'AIDA-DieCast'),
    )
    section = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True,default=1)
    is_admin= models.BooleanField('Is_admin', default=False)
    is_lead = models.BooleanField('Is_lead', default=False)
    is_super = models.BooleanField('Is_super', default=False)
    is_tech = models.BooleanField('Is_tech', default=False) 
    is_active = models.BooleanField('Is_Active', default=False)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Open_ticket(models.Model):
    ticket_id = models.IntegerField(default=0)
    user_name = models.CharField(max_length=100)
    site_name = models.TextField(max_length=50)
    site_sub_name = models.TextField(max_length=50, default='')
    site_section = models.PositiveSmallIntegerField(default='')
    description = models.TextField(max_length=300, default='')
    time_issue = models.DateTimeField(default=timezone.now)
    status = models.TextField(max_length=50, default='')

    def __str__(self):
        return str(self.ticket_id)

class ticket_stat(models.Model):
    ticket_id = models.IntegerField(default=0)
    super_approve_time = models.DateTimeField(null=True,blank=True,default='')
    pe_approved_time = models.DateTimeField(null=True,blank=True,default='')
    pe_man_approved_time = models.DateTimeField(null=True,blank=True,default='')

    def __str__(self):
        return str(self.ticket_id)

class tech_action(models.Model):
    ticket_id = models.IntegerField(default=0)
    taken_by = models.TextField(null=True,blank=True,max_length=50)
    closed_by = models.TextField(null=True,blank=True,max_length=50)
    pe_start = models.DateTimeField(null=True,blank=True,default='')
    pe_finish = models.DateTimeField(null=True,blank=True,default='')
    closed = models.DateTimeField(null=True,blank=True,default='')
    action_taken = models.TextField(null=True,blank=True,max_length=200)
    sparepart = models.TextField(null=True,blank=True,max_length=100)

    def __str__(self):
        return str(self.ticket_id)

class Downtime(models.Model):
    ticket_id = models.IntegerField(null=True,blank=True,default=0)
    user_name = models.CharField(null=True,blank=True,max_length=100)
    site_name = models.TextField(null=True,blank=True,max_length=50)
    site_sub_name = models.TextField(null=True,blank=True,max_length=50, default='')
    site_section = models.PositiveSmallIntegerField(null=True,blank=True,default=0)
    description = models.TextField(null=True,blank=True,max_length=300, default='')
    analisis = models.TextField(null=True,blank=True,max_length=300, default='')
    spare_part = models.TextField(null=True,blank=True,max_length=300, default='')
    time_issue = models.DateTimeField(null=True,blank=True,default='')
    time_finish = models.DateTimeField(null=True,blank=True,default='')
    status = models.TextField(null=True,blank=True,max_length=50, default='')
    reasons = models.TextField(null=True,blank=True,max_length=50, default='')
    kyt_image = models.ImageField(null=True,blank=True,upload_to='uploads/')
    approved = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    taken = models.BooleanField(default=False)

    def __str__(self):
        return str(self.ticket_id)
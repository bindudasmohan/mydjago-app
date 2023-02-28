from django.db import models


# Create your models here.
class Userreg(models.Model):
    Name = models.CharField(max_length=50)
    Address = models.CharField(max_length=50)
    Contactno = models.BigIntegerField()
    Email_id = models.CharField(max_length=50)
    Aadhaarno = models.BigIntegerField()
    Village = models.CharField(max_length=50)
    User_id = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)

class Agriculture(models.Model):
    Area = models.CharField(max_length=50)
    Productname = models.CharField(max_length=50)
    Quantity = models.IntegerField()
    Status = models.CharField(max_length=50,null=True)
    Appno = models.ForeignKey(Userreg,on_delete=models.CASCADE)
    Agriphoto=models.CharField(max_length=100,null=True)
    Reason=models.CharField(max_length=255,null=True)

class Farm(models.Model):
    Farmno = models.IntegerField(primary_key=True,auto_created=True)
    Area = models.CharField(max_length=50)
    Animalname = models.CharField(max_length=50)
    Animalfood = models.CharField(max_length=50)
    Numofanimal = models.IntegerField()
    Status = models.CharField(max_length=50,null=True)
    Applicationno = models.ForeignKey(Userreg,on_delete=models.CASCADE)
    Farmphoto=models.CharField(max_length=100,null=True)
    Reason=models.CharField(max_length=255,null=True)

class House(models.Model):
    Houseno = models.CharField(max_length=50,primary_key=True)
    Area = models.CharField(max_length=50)
    Floor = models.CharField(max_length=50)
    Roof = models.CharField(max_length=50)
    Staircase = models.CharField(max_length=50)
    Diprecition = models.CharField(max_length=50)
    Status = models.CharField(max_length=50,null=True)
    Sqfeet = models.CharField(max_length=50)
    Applicationno = models.ForeignKey(Userreg,on_delete=models.CASCADE)
    Housephoto=models.CharField(max_length=100,null=True)
    Reason=models.CharField(max_length=255,null=True)


class Disaster_amount(models.Model):
    Affectedno = models.IntegerField()
    Applicationno =  models.IntegerField()
    Amount =  models.IntegerField()
    Depreciation =  models.IntegerField()
    Status = models.CharField(max_length=11,null=True)

class Disasterfloor(models.Model):
    Floor = models.CharField(max_length=50)
    Rate = models.DecimalField(max_digits=10,decimal_places=2)

class Disasterroof(models.Model):
    Roof = models.CharField(max_length=50)
    Rate = models.DecimalField(max_digits=10,decimal_places=2)

class Dismanagereg(models.Model):
    Name = models.CharField(max_length=50)
    Address = models.CharField(max_length=50)
    District = models.CharField(max_length=50)
    Mobno = models.BigIntegerField()
    Email_id = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50,primary_key=True)
    Password = models.CharField(max_length=50)

class Adminlog(models.Model):
    User_id =  models.CharField(max_length=50,primary_key=True)
    Password =  models.CharField(max_length=50)

class Animalnum(models.Model):
    Animalname =  models.CharField(max_length=50)
    Rate = models.DecimalField(max_digits=10,decimal_places=2)

class Event(models.Model):
    Eventname = models.CharField(max_length=50)
    Description = models.CharField(max_length=50)

class Feedback(models.Model):
    Name = models.CharField(max_length=50)
    Description = models.CharField(max_length=50)

class Productamount(models.Model):
    Productname = models.CharField(max_length=50)
    Rate = models.DecimalField(max_digits=10,decimal_places=2)
    
class Userpersonal(models.Model):
    Applicationno =  models.ForeignKey(Userreg,on_delete=models.CASCADE)
    # User_id = models.CharField(max_length=50)
    Taluk = models.CharField(max_length=50)
    Surveyno = models.IntegerField()
    Bankname = models.CharField(max_length=100)
    Bankbranch = models.CharField(max_length=50)
    Accno = models.BigIntegerField()

class villagereg(models.Model):
    Name = models.CharField(max_length=50)
    Address = models.CharField(max_length=50)
    Contactno = models.BigIntegerField()
    Village = models.CharField(max_length=50)
    Block = models.CharField(max_length=50)
    District = models.CharField(max_length=50)
    User_id = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)
    Officer_id = models.BigAutoField(primary_key=True)
    Email_id = models.CharField(max_length=50)













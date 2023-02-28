from django.shortcuts import render,redirect
from django.http import HttpResponse
from.models import *
from django.template import loader
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail,BadHeaderError
# Create your views here.


def index(request):
        return render(request, "dces/index.html")

#########################################
#victim Section
#victim Login
def victim(request):
    template = loader.get_template("dces/user/index.html")
    context = {}
    if request.method == "POST":
        try:
            username = request.POST.get("txtUserid")
            password = request.POST.get("txtpwd")
            login_obj = Userreg.objects.filter(User_id=username).exists()
            if login_obj:
                user_obj = Userreg.objects.get(User_id=username, Password=password)
                request.session['USERNAME'] = user_obj.User_id
                request.session['APPNO']=user_obj.id
                # template = loader.get_template("dces/user/home.html")
                uservictim = Userreg.objects.filter(User_id=username)
                userper = Userpersonal.objects.filter(Applicationno=user_obj.id)
                return render(request, "dces/user/uprofile.html", {'Profile': uservictim, 'Personal': userper})
                # return redirect('/uprofile/'+str(user_obj.id))
            else:

                context = {"error": "invalid user"}
                HttpResponse(template.render(context, request))
        except Exception as e:
            context = {"error": e}
            HttpResponse(template.render(context, request))
    return HttpResponse(template.render(context, request))

#victim registration
def userreg(request):
    template= loader.get_template('dces/user/userreg.html')
    context={}
    if request.method == "POST":
        
        name = request.POST["name"]
        address = request.POST["address"]
        contactno = request.POST["usecontact"]
        email_id = request.POST["useemail"]
        aadhaarno = request.POST["useadhar"]
        village = request.POST["usevillage"]
        user_id = request.POST["useuser"]
        password = request.POST["usepwd"]
        user_obj = Userreg.objects.filter(User_id=user_id).exists()
        if user_obj:
            context={'error':'Username is not available !..'}
        else:
            user = Userreg(Name=name,Address=address,Contactno=contactno,Email_id=email_id,Aadhaarno=aadhaarno,Village=village,User_id=user_id,Password=password)
            user.save()
            currentuser=Userreg.objects.latest('id')
            context={'APPNO':currentuser.id}
            template=loader.get_template('dces/user/vapp.html')
        
    return HttpResponse(template.render(context,request))

#victim personal details
def userpers(request):
    template = loader.get_template('dces/user/userpersonal.html')
    context = {}
    if request.method == "POST":
        hhuser=request.POST["huser"]
        appno = Userreg.objects.filter(User_id=hhuser)
        # affectedarea = request.POST["affectarea"]
        taluk = request.POST["taluk"]
        surveyno = request.POST["survey"]
        bankname = request.POST["bnkname"]
        bankbranch = request.POST["bnkbranch"]
        accno = request.POST["accno"]
        userpers = Userpersonal(Applicationno=appno[0], Taluk=taluk, Surveyno=surveyno,Bankname=bankname, Bankbranch=bankbranch, Accno=accno)
        userpers.save()
        uservictim = Userreg.objects.filter(User_id=hhuser)
        userper = Userpersonal.objects.filter(Applicationno=appno[0])
        return render(request, "dces/user/uprofile.html", {'Profile': uservictim, 'Personal': userper})
        # return redirect('/uprofile/'+str(appno[0]))
    return HttpResponse(template.render(context, request))

#victim change password
def userchgpwd(request):
    u=Userreg.objects.get(User_id=request.session['USERNAME'])
    context={'Profile':u}
    template = loader.get_template("dces/user/userchgpwd.html")
    if request.method == "POST":
        pwd=request.POST['Password']
        cpwd=request.POST['ConfirmPassword']
        if pwd == cpwd:
            u.Password=pwd
            u.save()
            context={'Profile':u,'Error':'Password changed Successfully.Logout your account and Login again !.'}
            template = loader.get_template("dces/user/userchgpwd.html")
        else:
            u=Userreg.objects.filter(User_id=request.session['USERNAME'])
            context={'Profile':u,'Error':'Password not matched'}
            template = loader.get_template("dces/user/userchgpwd.html")
    return HttpResponse(template.render(context,request))


#user profile
def uprofile(request,APPNO):
    U=Userreg.objects.filter(id=APPNO)
    P=Userpersonal.objects.filter(Applicationno_id=APPNO)
    context={'Profile':U,'Personal':P}
    return render(request,"dces/user/uprofile.html",context)

#common event list
def ueventlist(request):
    events=Event.objects.all()
    context={'events':events}
    template = loader.get_template("dces/user/events.html")
    return HttpResponse(template.render(context,request))

#victim house application
def house(request):
    template = loader.get_template('dces/user/house.html')
    context = {}
    if request.method == "POST":
        houseno = request.POST["houseno"]
        area = request.POST["housearea"]
        floor = request.POST["housefloor"]
        roof = request.POST["houseroof"]
        staircase = request.POST["housestair"]
        dipreciation= request.POST["housedepre"]
        sqfeet = request.POST["housesq"]
        hhuser = request.POST["huser"]
        photo=request.FILES['hphoto']
        fs=FileSystemStorage()
        filename='H'+photo.name
        fs.save(filename,photo)
        appno = Userreg.objects.filter(User_id=hhuser)
        house = House(Houseno = houseno,Area = area, Floor = floor,Roof = roof,Staircase = staircase,Diprecition = dipreciation, Sqfeet =sqfeet,Applicationno=appno[0],Housephoto=filename)
        house.save()
        H = House.objects.filter(Applicationno=appno[0])
        context={'house':H,'users':appno}
        template = loader.get_template('dces/user/victimhouse.html')
    return HttpResponse(template.render(context, request))

#victim view house status
def viewhouse(req,appno):
    # appno = Userreg.objects.filter(id=id)
    # amt = Disaster_amount.objects.raw("select * from dces_Disaster_amount where Status='Passed' and Applicationno=" + id + " and Affectedno=(select id from dces_house where Houseno_id="+id+")")
    H=House.objects.filter(Applicationno_id=appno)
    U=Userreg.objects.filter(id=appno)
    return render(req,"dces/user/victimhouse.html",{'house':H,'users':U})

#victim view house status
def vhouse(req,ano):
    # appno = Userreg.objects.filter(id=id)
    id=ano
    amt = Disaster_amount.objects.raw("select * from dces_Disaster_amount where Status='Passed' and Applicationno=" + id + " and Affectedno=(select Houseno from dces_house where Applicationno_id="+id+")")
    H=House.objects.filter(Applicationno=id)
    U=Userreg.objects.filter(id=id)
    return render(req,"dces/user/vhouse.html",{'house':H,'users':U,'Amount':amt})

#victim farm Application
def farm(request):
    template = loader.get_template('dces/user/farm.html')
    context = {}
    if request.method == "POST":
        farmno= request.POST["farmno"]
        area= request.POST["farmarea"]
        animalname= request.POST["farmanimal"]
        animalfood = request.POST["farmanimalfood"]
        animalno = request.POST["farmnum"]
        hhuser = request.POST["huser"]
        photo=request.FILES['fphoto']
        fs=FileSystemStorage()
        filename='F'+photo.name
        fs.save(filename,photo)
        appno = Userreg.objects.filter(User_id=hhuser)
        farm= Farm(Farmno=farmno,Area=area,Animalname=animalname,Animalfood=animalfood,Numofanimal=animalno,Applicationno=appno[0],Farmphoto=filename)
        farm.save()
        F = Farm.objects.filter(Applicationno=appno[0])
        context = {'farm': F, 'users': appno}
        template = loader.get_template('dces/user/victimfarm.html')
    return HttpResponse(template.render(context, request))

#victim view house 
def viewfarm(req,appno):
    F = Farm.objects.filter(Applicationno=appno)
    U=Userreg.objects.filter(id=appno)
    return render(req,"dces/user/victimfarm.html",{'farm':F,'users':U})

#victim view farm status
def vfarm(req,bno):
    id=bno
    amt = Disaster_amount.objects.raw("select * from dces_Disaster_amount where Status='Passed' and Applicationno=" + id + " and Affectedno=(select Farmno from dces_farm where Applicationno_id=" + id + ")")
    F = Farm.objects.filter(Applicationno=id)
    U = Userreg.objects.filter(id=id)
    return render(req,'dces/user/vfarm.html',{'farm':F,'users':U,'Amount':amt})


#victim agriculture application
def agriculture(request):
    template = loader.get_template('dces/user/agriculture.html')
    context = {}
    if request.method == "POST":
        area = request.POST["agrarea"]
        productname = request.POST["agrproname"]
        quantity = request.POST["agrquantity"]
        hhuser = request.POST["huser"]
        photo=request.FILES['aphoto']
        fs=FileSystemStorage()
        filename='A'+photo.name
        fs.save(filename,photo)
        appno = Userreg.objects.filter(User_id=hhuser)
        agriculture = Agriculture(Area=area,Productname=productname,Quantity=quantity,Appno=appno[0],Agriphoto=filename)
        agriculture.save()
        A = Farm.objects.filter(Applicationno=appno[0])
        context = {'farm': A, 'users': appno}
        template = loader.get_template('dces/user/victimagriculture.html')
    return HttpResponse(template.render(context, request))

#victim view agriculture 
def viewagriculture(req,appno):
    A = Agriculture.objects.filter(Appno_id=appno)
    U = Userreg.objects.filter(id=appno)
    return render(req, 'dces/user/victimagriculture.html', {'agriculture': A, 'users': U})


#victim view agriculture status
def vagriculture(req,cno):
    id = cno
    # amt=Disaster_amount.objects.filter(Applicationno=id)
    amt = Disaster_amount.objects.raw("select * from dces_Disaster_amount where Status='Passed' and Applicationno="+id+" and Affectedno=(select id from dces_agriculture where Appno_id="+id+")")
    A = Agriculture.objects.filter(Appno=id)
    U = Userreg.objects.filter(id=id)
    return render(req, 'dces/user/vagriculture.html', {'agriculture': A, 'users': U,'Amount':amt})

#victim logout
def victimlogout(request):
    del request.session['USERNAME']
    del request.session['APPNO']
    return render(request, 'dces/user/index.html')


# victim section end
########################################







#######################################
#Village officer section start

#village officer login
def vLogin(request):
    template = loader.get_template('dces/village/index.html')
    context = {}
    if request.method == "POST":
        try:
            officerid=request.POST.get('txtid')
            username = request.POST.get('txtUsername') 
            password = request.POST.get('txtPassword')  
            Login_obj = villagereg.objects.filter(Officer_id=officerid,User_id=username).exists()
            if Login_obj:
                user_obj = villagereg.objects.get(Officer_id=officerid,User_id=username,Password=password)
                request.session['VOFFICER_ID']=user_obj.Officer_id
                request.session['VUSERNAME'] = user_obj.User_id
                # template = loader.get_template('dces/village/vhome.html')
                # village=villagereg.object.filter(Officer_id=id)
                H=House.objects.filter(Status__isnull=True,Area=user_obj.Village)
                F=Farm.objects.filter(Status__isnull=True,Area=user_obj.Village)
                A=Agriculture.objects.filter(Status__isnull=True,Area=user_obj.Village)
                context={'house':H,'farm':F,'agri':A}
                return render(request,"dces/village/vallapps.html",context)
            else:
                context = {"error": "Invalid User"}
                HttpResponse(template.render(context, request))   
        except Exception as e:
            context = {"error": e}
            HttpResponse(template.render(context,request))
    return HttpResponse(template.render(context,request))

#village officer logout
def vlogout(request):
    del request.session['VUSERNAME']
    del request.session['VOFFICER_ID']
    return render(request, "dces/village/index.html")                 

#view village profile
def vprofile(request,id):
    v=villagereg.objects.filter(Officer_id=id)
    context={'Profile':v}
    template = loader.get_template("dces/village/vprofile.html")
    return HttpResponse(template.render(context,request))

# village officer registration
def villageregistration(request):
    template = loader.get_template("dces/admin/villagereg.html")
    context={}
    if request.method == "POST":
        name = request.POST["villname"]
        address = request.POST["villaddress"]
        contactno = request.POST["villcontact"]
        village = request.POST["villvillage"]
        block = request.POST["villblock"]
        district = request.POST["villdis"]
        emailaddress = request.POST["villeml"]
        username = request.POST["villusnme"]
        password = request.POST["villpswd"]
        vlg_obj = villagereg.objects.filter(User_id=username).exists()
        if vlg_obj:
            context={'error':'Username is not available !..'}
        else:
            village = villagereg(Name=name,Address=address,Contactno=contactno,Village=village,Block=block,District=district,User_id=username,Password=password,Email_id=emailaddress)
            village.save()
            vofficers=villagereg.objects.all().order_by('-Officer_id').values('Officer_id')
            
            subject='Village Officer Registration'
            message='Your Registration completed successfully.Your ID:'+str(vofficers[0]['Officer_id'])+',Username :'+username+' and password :'+password+'.Please Login  and continue to your account.'
            from_email='disasterecs@gmail.com'
            receipient=emailaddress
            try:
                send_mail(subject,message,from_email,[receipient])
            except BadHeaderError as be:
                print(be)
            vofficers=villagereg.objects.all()
            context={'VillageOfficer':vofficers}
            template = loader.get_template("dces/admin/villageofficers.html")    
    return HttpResponse(template.render(context,request))

#village profile update
def veditprofile(request,id):
    v=villagereg.objects.get(Officer_id=id)
    context={'Profile':v}
    template = loader.get_template("dces/village/vupdateprofile.html")

    if request.method == "POST":
        v.Name=request.POST['txtName']
        v.Address=request.POST['txtAddress']
        v.Contactno=request.POST['txtcontact']
        v.District=request.POST['txtDistrict']
        v.Email_id=request.POST['txtEmail']
        v.save()
        
        v=villagereg.objects.filter(Officer_id=id)
        context={'Profile':v}
        template = loader.get_template("dces/village/vprofile.html")
       
    return HttpResponse(template.render(context,request))

#village change password
def vchngpwd(request,id):
    v=villagereg.objects.get(Officer_id=id)
    context={'Profile':v}
    template = loader.get_template("dces/village/vchngpassword.html")
    if request.method == "POST":
        pwd=request.POST['Password']
        cpwd=request.POST['ConfirmPassword']
        if pwd == cpwd:
            v.Password=pwd
            v.save()
            v=villagereg.objects.filter(Officer_id=id)
            context={'Profile':v,'Error':'Password changed Successfully.Logout your account and Login again !.'}
            template = loader.get_template("dces/village/vchngpassword.html")
        else:
            v=villagereg.objects.filter(Officer_id=id)
            context={'Profile':v,'Error':'Password not matched'}
            template = loader.get_template("dces/village/vchngpassword.html")
    return HttpResponse(template.render(context,request))


# Village officer verify house
def vverifyhouse(request,id):
    template = loader.get_template("dces/village/vverifyhouse.html")
    context={}
    if request.method == "POST":
        h = House.objects.get(Houseno=id)
        status = request.POST['status']
        if request.POST['reason'] != '':
            reason = request.POST['reason']
            h.Status = status
            h.Reason = reason
            h.save()
        else:
            h.Status=status
            h.save()
        H=House.objects.filter(Houseno=id).values()
        U=Userreg.objects.filter(id=H[0]['Applicationno_id'])
        context={'house':H,'users':U}
        template = loader.get_template("dces/village/vverifyhouse.html")
    return HttpResponse(template.render(context,request))

# village verify farm
def vverifyfarm(request,id):
    template = loader.get_template("dces/village/vverifyfarm.html")
    if request.method == "POST":
        f = Farm.objects.get(Farmno=id)
        status = request.POST['status']
        if request.POST['reason'] != '':
            reason = request.POST['reason']
            f.Status = status
            f.Reason = reason
            f.save()
        else:
            f.Status=status
            f.save()
        F=Farm.objects.filter(Farmno=id).values()
        U=Userreg.objects.filter(id=F[0]['Applicationno_id'])
        context={'farm':F,'users':U}
        template = loader.get_template("dces/village/vverifyfarm.html")
    return HttpResponse(template.render(context,request))

# village verify farm
def vverifyagriculture(request,id):
    template = loader.get_template("dces/village/vverifyagri.html")
    if request.method == "POST":
        h = Agriculture.objects.get(id=id)
        status = request.POST['status']
        if request.POST['reason'] != '':
            reason = request.POST['reason']
            h.Status = status
            h.Reason = reason
            h.save()
        else:
            h.Status=status
            h.save()
        A=Agriculture.objects.filter(id=id).values()
        U=Userreg.objects.filter(id=A[0]['Appno_id'])
        context={'agri':A,'users':U}
        template = loader.get_template("dces/village/vverifyagri.html")
    return HttpResponse(template.render(context,request))

#village view compute house
'''def viewHcompute(request,hno):
    H=House.objects.filter(Houseno=hno).values()
    U=Userreg.objects.filter(id=H[0]['Applicationno_id'])
    context={'house':H,'users':U}
    template = loader.get_template("dces/village/vcomputehouse.html")
    return HttpResponse(template.render(context,request))'''
#village house estimation calculate
def hcompute(request,hno):
    H=House.objects.filter(Houseno=hno).values()
    U=Userreg.objects.filter(id=H[0]['Applicationno_id'])
    DM=Disaster_amount.objects.filter(Affectedno=hno,Applicationno=H[0]['Applicationno_id'])
    context={'house':H,'users':U,'Amount':DM}
    template = loader.get_template("dces/village/vcomputehouse.html")
    if request.method == 'POST':
        floor = 0
        roof = 0
        h = House.objects.filter(Houseno=hno).values()
        sq = h[0]['Sqfeet']
        St=0
        f = Disasterfloor.objects.get(Floor=h[0]['Floor'])
        # for f1 in f:
        # if h[0]['Floor'] == f.Floor:
        floor = int(h[0]['Sqfeet']) * int(f.Rate)
       
        if h[0]['Staircase'] == 1:
            St = 40000
        elif h[0]['Staircase']==2:
            St = 20000
        elif h[0]['Staircase']==3:
            St = 20000
        else:
            St = 10000
        r = Disasterroof.objects.all()
        for r1 in r:
            if h[0]['Roof'] == r1.Roof:
                roof = int(sq) * int(r1.Rate)
        dep = h[0]['Diprecition']
        amt = int(floor)+roof+St
        damt=amt*2/100
        damt = damt * 5
        amount =amt+ damt
        # print(floor,roof,St,amount,amt)
        Ano = hno
        Appno = h[0]['Applicationno_id']
        Amount = amount
        Depreciation = damt
        Status = 'Pending'
        DA = Disaster_amount(Affectedno=Ano,Applicationno=Appno,Amount=amount,Depreciation=damt,Status=Status)
        DA.save()
        H=House.objects.filter(Houseno=hno).values()
        U=Userreg.objects.filter(id=H[0]['Applicationno_id'])
        DM=Disaster_amount.objects.filter(Affectedno=hno,Applicationno=H[0]['Applicationno_id'])
        context={'house':H,'users':U,'Amount':DM}
        template = loader.get_template("dces/village/vcomputehouse.html")
    return HttpResponse(template.render(context,request))

#village farm estimation calculate
def fcompute(request,fno):
    F = Farm.objects.filter(Farmno=fno).values()
    U=Userreg.objects.filter(id=F[0]['Applicationno_id'])
    DM=Disaster_amount.objects.filter(Affectedno=fno,Applicationno=F[0]['Applicationno_id'])
    context={'farm':F,'users':U,'Amount':DM}
    template = loader.get_template("dces/village/vcomputefarm.html")
    if request.method == 'POST':
        A = Animalnum.objects.all()
        amt=0
        for animal in A:
            if animal.Animalname == F[0]['Animalname']:
                amt = F[0]['Numofanimal'] * animal.Rate
        appno = F[0]['Applicationno_id']
        DA = Disaster_amount(Affectedno=fno,Applicationno=appno,Amount=amt,Depreciation=0,Status='Pending')
        DA.save()
        F = Farm.objects.filter(Farmno=fno).values()
        U=Userreg.objects.filter(id=F[0]['Applicationno_id'])
        DM=Disaster_amount.objects.filter(Affectedno=fno,Applicationno=F[0]['Applicationno_id'])
        context={'farm':F,'users':U,'Amount':DM}
        template = loader.get_template("dces/village/vcomputefarm.html")
    return HttpResponse(template.render(context,request))

#village Agriculture estimation calculate
def Acompute(request,idno):
    A = Agriculture.objects.filter(id=idno).values()
    U=Userreg.objects.filter(id=A[0]['Appno_id'])
    DM=Disaster_amount.objects.filter(Affectedno=idno,Applicationno=A[0]['Appno_id'])
    context={'agri':A,'users':U,'Amount':DM}
    template = loader.get_template("dces/village/vcomputeagri.html")
    if request.method == 'POST':
        P = Productamount.objects.all()
        amt=0
        for product in P:
            if product.Productname == A[0]['Productname']:
                amt = A[0]['Quantity'] * product.Rate
        
        appno = A[0]['Appno_id']
        DA = Disaster_amount(Affectedno=idno,Applicationno=appno,Amount=amt,Depreciation=0,Status='Pending')
        DA.save()
        A = Agriculture.objects.filter(id=idno).values()
        U=Userreg.objects.filter(id=A[0]['Appno_id'])
        DM=Disaster_amount.objects.filter(Affectedno=idno,Applicationno=A[0]['Appno_id'])
        context={'agri':A,'users':U,'Amount':DM}
        template = loader.get_template("dces/village/vcomputeagri.html")
    return HttpResponse(template.render(context,request))

#village verified house
def verifiedhouse(request):
    User = Userreg.objects.filter(AppNo = request.session.APPNO)
    House = House.objects.filter(AppNo=request.session.APPNO)
    return render(request,"dces/village/computehouse.html")

#village verified farm
def verifiedfarm(request):
    User = Userreg.objects.filter(AppNo = request.session.APPNO)
    Farm = Farm.objects.filter(AppNo=request.session.APPNO)
    return render(request,"dces/village/computefarm.html")

#village verified Agriculture
def verifiedagriculture(request):
    User = Userreg.objects.filter(AppNo = request.session.APPNO)
    Agriculture = Agriculture.objects.filter(AppNo=request.session.APPNO)
    return render(request,"dces/village/computeagriculture.html")

# village add new events
def veventadd(request):
    events=Event.objects.all()
    context={'events':events}
    template = loader.get_template("dces/village/vevents.html")
    if request.method == 'POST':
        name=request.POST['txtName']
        Desc=request.POST['txtDesc']
        evt=Event(Eventname=name,Description=Desc)
        evt.save()
        events=Event.objects.all()
        context={'events':events}
        template = loader.get_template("dces/village/vevents.html")
    return HttpResponse(template.render(context,request))

#common event list
def eventlist(request):
    events=Event.objects.all()
    context={'events':events}
    template = loader.get_template("dces/village/vevents.html")
    return HttpResponse(template.render(context,request))

#village officer view all apps for verify app forms
def vlgallapps(request,id):
    village=villagereg.objects.filter(Officer_id=id).values()
    H=House.objects.filter(Status__isnull=True,Area=village[0]['Village'])
    F=Farm.objects.filter(Status__isnull=True,Area=village[0]['Village'])
    A=Agriculture.objects.filter(Status__isnull=True,Area=village[0]['Village'])
    context={'house':H,'farm':F,'agri':A}
    return render(request,"dces/village/vallapps.html",context)

#village officer view all apps for verified app forms
def vvapps(request,id):
    village=villagereg.objects.filter(Officer_id=id).values()
    H=House.objects.filter(Status='Verify',Area=village[0]['Village'])
    F=Farm.objects.filter(Status='Verify',Area=village[0]['Village'])
    A=Agriculture.objects.filter(Status='Verify',Area=village[0]['Village'])
    context={'house':H,'farm':F,'agri':A}
    return render(request,"dces/village/vvapps.html",context)

#village officer view all apps for not verify app forms
def vlgallappsnot(request,id):
    village=villagereg.objects.filter(Officer_id=id).values()
    H=House.objects.filter(Status='Not Verify',Area=village[0]['Village'])
    F=Farm.objects.filter(Status='Not Verify',Area=village[0]['Village'])
    A=Agriculture.objects.filter(Status='Not Verify',Area=village[0]['Village'])
    context={'house':H,'farm':F,'agri':A}
    return render(request,"dces/village/vallappsnot.html",context)



# village view house
def vviewHouse(request,hno):
    H=House.objects.filter(Houseno=hno).values()
    U=Userreg.objects.filter(id=H[0]['Applicationno_id'])
    context={'house':H,'users':U}
    return render(request,"dces/village/vverifyhouse.html",context)

#village view Farm
def vviewFarm(request,fno):
    H=Farm.objects.filter(Farmno=fno).values()
    U=Userreg.objects.filter(id=H[0]['Applicationno_id'])
    context={'farm':H,'users':U}
    return render(request,"dces/village/vverifyfarm.html",context)

#village view Agriculture
def vviewAgri(request,id):
    A=Agriculture.objects.filter(id=id).values()
    U=Userreg.objects.filter(id=A[0]['Appno_id'])
    context={'agri':A,'users':U}
    return render(request,"dces/village/vverifyagri.html",context)

#village section end
##########################################

###########################################
#manager section start

def mlogin(request):
    template = loader.get_template("dces/manager/index.html")
    context = {}
    if request.method == "POST":
        try:
            username = request.POST.get("mngruser")
            password = request.POST.get("mngrpwd")
            login_obj = Dismanagereg.objects.filter(user_id=username).exists()
            if login_obj:
                manager_obj = Dismanagereg.objects.get(user_id=username, Password=password)
                request.session['MUSERNAME'] = manager_obj.user_id
                H = House.objects.filter(Status='Verify')
                F = Farm.objects.filter(Status='Verify')
                A = Agriculture.objects.filter(Status='Verify')
                context={'house':H,'farm':F,'agri':A}
                return render(request, "dces/manager/mgrallapps.html",context)
            else: 
                context = {"error": "invalid user"}
                HttpResponse(template.render(context, request))
        except Exception as e:
            context = {"error": e}
            HttpResponse(template.render(context, request))
    return HttpResponse(template.render(context, request))

#manager registration
def managerreg(request):
    template = loader.get_template('dces/admin/managerreg.html')
    context={}
    if request.method == "POST":
        name = request.POST["mngrname"]
        address = request.POST["mngraddress"]
        contact = request.POST["mngrcontact"]
        district = request.POST["mngrdistrict"]
        email = request.POST["mngremail"]
        userid=request.POST['mngrusername']
        password = request.POST["mngrpwd"]
        mgr_obj = Dismanagereg.objects.filter(user_id=userid).exists()
        if mgr_obj:
            context={'error':'Username is not available !..'}
        else:
            manager = Dismanagereg(Name=name, Address=address, Mobno=contact, District=district, Email_id=email,user_id=userid,Password=password)
            manager.save()
            subject='Disaster Manager Registration'
            message='Your Registration completed successfully.Username is'+userid+'</b> and password is '+password+'.Please Login  and continue to your account.'
            from_email='disasterecs@gmail.com'
            receipient=email
            try:
                send_mail(subject,message,from_email,[receipient])
            except BadHeaderError as be:
                print(be)
            mgrs=Dismanagereg.objects.all()
            context={'Managers':mgrs}
            template = loader.get_template('dces/admin/managers.html')           
    return HttpResponse(template.render(context,request))

#manager edit profile
def meditprofile(request):
    m=Dismanagereg.objects.get(user_id=request.session['MUSERNAME'])
    context={'Profile':m}
    template = loader.get_template("dces/manager/editpro.html")
    if request.method == "POST":
        m.Name = request.POST["mngrname"]
        m.Address = request.POST["mngraddress"]
        m.Mobno = request.POST["mngrcontact"]
        m.District = request.POST["mngrdistrict"]
        m.Email_id = request.POST["mngremail"]
        m.save()
        
        m=Dismanagereg.objects.filter(user_id=request.session['MUSERNAME'])
        context={'Profile':m}
        template = loader.get_template("dces/manager/mprofile.html")
 
    return HttpResponse(template.render(context,request))


def mchngpwd(request):
    u=Dismanagereg.objects.get(user_id=request.session['MUSERNAME'])
    context={'Profile':u}
    template = loader.get_template("dces/manager/mgrchgpwd.html")
    if request.method == "POST":
        pwd=request.POST['Password']
        cpwd=request.POST['ConfirmPassword']
        if pwd == cpwd:
            u.Password=pwd
            u.save()
            context={'Profile':u,'Error':'Password changed Successfully.Logout your account and Login again !.'}
            template = loader.get_template("dces/manager/mgrchgpwd.html")
        else:
            u=Dismanagereg.objects.filter(user_id=request.session['MUSERNAME'])
            context={'Profile':u,'Error':'Password not matched'}
            template = loader.get_template("dces/manager/mgrchgpwd.html")
    return HttpResponse(template.render(context,request))

#view manager profile
def mprofile(request):
    m=Dismanagereg.objects.filter(user_id=request.session['MUSERNAME'])
    context={'Profile':m}
    template = loader.get_template("dces/manager/mprofile.html")
    return HttpResponse(template.render(context,request))

#Manager Logout 
def mlogout(request):
    del request.session['MUSERNAME']
    return render(request,"dces/manager/index.html")


#manager view all application
def mallapps(request):
    H = House.objects.filter(Status='Verify')
    F = Farm.objects.filter(Status='Verify')
    A = Agriculture.objects.filter(Status='Verify')
    context={'house':H,'farm':F,'agri':A}
    return render(request, "dces/manager/mgrallapps.html",context)

'''
def vhousemgr(request,id):
    template = loader.get_template('dces/manager/vhousemgr.html')
    context = {}
    if request.method == "POST":
        h = House.objects.get(Houseno=id)
        status = request.POST['status']
        h.status = status
        h.save()
        H = House.objects.filter(Houseno=id).values()
        U = Userreg.objects.filter(id=H[0]['Applicationno_id'])
        context = {'house':H,'users':U}
        template = loader.get_template('dces/manager/vhousemgr.html')
    return HttpResponse(template.render(context, request))
def vfarmmgr(request,id):
    template = loader.get_template('dces/manager/vfarmmgr.html')
    context = {}
    if request.method == "POST":
        f = Farm.objects.get(Farmno=id)
        status = request.POST['status']
        f.status = status
        f.save()
        F = Farm.objects.filter(Farmno=id).values()
        U = Userreg.objects.filter(id=F[0]['Applicationno_id'])
        context = {'farm': F, 'users': U}
        template = loader.get_template('dces/manager/vfarmmgr.html')
    return HttpResponse(template.render(context, request))
def vagriculturemgr(request,id):
    template = loader.get_template('dces/manager/vagriculturemgr.html')
    context = {}
    if request.method == "POST":
        a = Agriculture.objects.get(id=id)
        status = request.POST['status']
        a.status = status
        a.save()
        A = Agriculture.objects.filter(id=id).values()
        U = Userreg.objects.filter(id=A[0]['Applicationno_id'])
        context = {'farm': A, 'users': U}
        template = loader.get_template('dces/manager/vagriculturemgr.html')
    return HttpResponse(template.render(context, request))

'''

# Manager view house
def mviewHouse(request, hno):
    H=House.objects.filter(Houseno=hno).values()
    U=Userreg.objects.filter(id=H[0]['Applicationno_id'])
    DM=Disaster_amount.objects.filter(Affectedno=hno,Applicationno=H[0]['Applicationno_id'])
    if  DM.exists():
        context={'house':H,'users':U,'Amount':DM}
        template = loader.get_template("dces/manager/vhousemgr.html")
        Damt=Disaster_amount.objects.get(Affectedno=hno,Applicationno=H[0]['Applicationno_id'])
        if request.method == "POST":
            Damt.Status=request.POST['status']
            Damt.save()
            # context={'house':H,'users':U,'Amount':DM}
            # template = loader.get_template("dces/manager/vhousemgr.html")
    else:
        context={'house':H,'users':U}
        template = loader.get_template("dces/manager/vhousemgr.html")
    return HttpResponse(template.render(context, request))

# Manager view Farm
def mviewFarm(request, fno):
    H = Farm.objects.filter(Farmno=fno).values()
    U =Userreg.objects.filter(id=H[0]['Applicationno_id'])
    DM=Disaster_amount.objects.filter(Affectedno=fno,Applicationno=H[0]['Applicationno_id'])
    if  DM.exists():
        context = {'farm': H, 'users': U,'Amount':DM}
        template = loader.get_template("dces/manager/vfarmmgr.html")
        Damt=Disaster_amount.objects.get(Affectedno=fno,Applicationno=H[0]['Applicationno_id'])
        if request.method == "POST":
            Damt.Status=request.POST['status']
            Damt.save()
    else:
        context = {'farm': H, 'users': U}
        template = loader.get_template("dces/manager/vfarmmgr.html")
    return HttpResponse(template.render(context, request))

#Manager view Agriculture
def mviewAgri(request, id):
    A = Agriculture.objects.filter(id=id).values()
    U = Userreg.objects.filter(id=A[0]['Appno_id'])
    DM=Disaster_amount.objects.filter(Affectedno=id,Applicationno=A[0]['Appno_id'])
    if  DM.exists():
        context = {'agri': A, 'users': U,'Amount':DM}
        template = loader.get_template("dces/manager/vagriculturemgr.html")
        Damt=Disaster_amount.objects.get(Affectedno=id,Applicationno=A[0]['Appno_id'])
        if request.method == "POST":
            Damt.Status=request.POST['status']
            Damt.save()
    else:
        context = {'agri': A, 'users': U,'Amount':DM}
        template = loader.get_template("dces/manager/vagriculturemgr.html")
    return HttpResponse(template.render(context, request))


#manager view all paassed application
def mvallapps(request):
    H = House.objects.raw("select Houseno,Area,Applicationno_id from dces_house where Applicationno_id in(select Applicationno from dces_Disaster_amount) and Houseno in(select Affectedno from dces_Disaster_amount where Status='Passed')")
    F = Farm.objects.raw("select Farmno,Area,Applicationno_id from dces_farm where Applicationno_id in(select Applicationno from dces_Disaster_amount) and Farmno in(select Affectedno from dces_Disaster_amount where Status='Passed')")
    A = Agriculture.objects.raw("select id,Area,Appno_id from dces_agriculture where Appno_id in(select Applicationno from dces_Disaster_amount) and id in(select Affectedno from dces_Disaster_amount where Status='Passed')")
    context={'house':H,'farm':F,'agri':A}
    return render(request, "dces/manager/mgrvallapps.html",context)

#manager view all pending application
def mpallapps(request):
    H = House.objects.raw("select Houseno,Area,Applicationno_id from dces_house where Applicationno_id in(select Applicationno from dces_Disaster_amount) and Houseno in(select Affectedno from dces_Disaster_amount where Status='Pending')")
    F = Farm.objects.raw("select Farmno,Area,Applicationno_id from dces_farm where Applicationno_id in(select Applicationno from dces_Disaster_amount) and Farmno in(select Affectedno from dces_Disaster_amount where Status='Pending')")
    A = Agriculture.objects.raw("select id,Area,Appno_id from dces_agriculture where Appno_id in(select Applicationno from dces_Disaster_amount) and id in(select Affectedno from dces_Disaster_amount where Status='Pending')")
    context={'house':H,'farm':F,'agri':A}
    return render(request, "dces/manager/mgrrallapps.html",context)

#manager view all rejectsd application
def mrallapps(request):
    H = House.objects.raw("select Houseno,Area,Applicationno_id from dces_house where Applicationno_id in(select Applicationno from dces_Disaster_amount) and Houseno in(select Affectedno from dces_Disaster_amount where Status='Reject')")
    F = Farm.objects.raw("select Farmno,Area,Applicationno_id from dces_farm where Applicationno_id in(select Applicationno from dces_Disaster_amount) and Farmno in(select Affectedno from dces_Disaster_amount where Status='Reject')")
    A = Agriculture.objects.raw("select id,Area,Appno_id from dces_agriculture where Appno_id in(select Applicationno from dces_Disaster_amount) and id in(select Affectedno from dces_Disaster_amount where Status='Reject')")
    context={'house':H,'farm':F,'agri':A}
    return render(request, "dces/manager/mgrrallapps.html",context)

#manager view Passed house
'''def mviewHouse(request, hno):
    H=House.objects.filter(Houseno=hno).values()
    U=Userreg.objects.filter(id=H[0]['Applicationno_id'])
    DM=Disaster_amount.objects.filter(Affectedno=hno,Applicationno=H[0]['Applicationno_id'],Status__isnull=True)
    context={'house':H,'users':U,'Amount':DM}
    template = loader.get_template("dces/manager/mhouse.html")
    return HttpResponse(template.render(context, request))'''
##############################################
#ADMIN section start

#admin login
def adminlogin(request):
    template = loader.get_template("dces/admin/index.html")
    context = {}
    if request.method == "POST":
        try:
            username = request.POST.get("user")
            password = request.POST.get("pwd")
            login_obj = Adminlog.objects.filter(User_id=username).exists()
            if login_obj:
                manager_obj = Adminlog.objects.get(User_id=username, Password=password)
                request.session['UNAME'] = manager_obj.User_id
                H = House.objects.filter(Status='Verify')
                F = Farm.objects.filter(Status='Verify')
                A = Agriculture.objects.filter(Status='Verify')
                context={'house':H,'farm':F,'agri':A}
                return render(request, "dces/admin/allapps.html",context)
            else: 
                context = {"error": "invalid user"}
                HttpResponse(template.render(context, request))
        except Exception as e:
            context = {"error": e}
            HttpResponse(template.render(context, request))
    return HttpResponse(template.render(context, request))

#village change password
def achngpwd(request,uid):
    u=Adminlog.objects.get(User_id=uid)
    context={'Profile':u}
    template = loader.get_template("dces/admin/adminchngpwd.html")
    if request.method == "POST":
        pwd=request.POST['Password']
        cpwd=request.POST['ConfirmPassword']
        if pwd == cpwd:
            u.Password=pwd
            u.save()
            context={'Profile':u,'Error':'Password changed Successfully.Logout your account and Login again !.'}
            template = loader.get_template("dces/admin/adminchngpwd.html")
        else:
            u=Adminlog.objects.filter(User_id=uid)
            context={'Profile':u,'Error':'Password not matched'}
            template = loader.get_template("dces/admin/adminchngpwd.html")
    return HttpResponse(template.render(context,request))

#victim logout
def adminlogout(request):
    del request.session['UNAME']
    return render(request, 'dces/admin/index.html')
#managers
def managers(request):
    mgrs=Dismanagereg.objects.all()
    context={'Managers':mgrs}
    template = loader.get_template('dces/admin/managers.html')
    return HttpResponse(template.render(context,request))

#delete manager
def delManager(request,uid):
    mgr=Dismanagereg.objects.get(user_id=uid)
    mgr.delete()
    mgrs=Dismanagereg.objects.all()
    context={'Managers':mgrs}
    template = loader.get_template('dces/admin/managers.html')
    return HttpResponse(template.render(context,request))

#view Village officers
def villageoficers(request):
    vofficers=villagereg.objects.all()
    context={'VillageOfficer':vofficers}
    template = loader.get_template("dces/admin/villageofficers.html")
    return HttpResponse(template.render(context,request))
#delete manager
def delOfficer(request,id):
    vlg=villagereg.objects.get(Officer_id=id)
    vlg.delete()
    vofficers=villagereg.objects.all()
    context={'VillageOfficer':vofficers}
    template = loader.get_template("dces/admin/villageofficers.html")
    return HttpResponse(template.render(context,request))

#view applicants
def applicants(request):
    users=Userreg.objects.all()
    context={'Applicants':users}
    template = loader.get_template("dces/admin/applicants.html")
    return HttpResponse(template.render(context,request))

#delete Applicants
def delApplicant(request,id):
    usr=userreg.objects.get(id=id)
    usr.delete()
    users=Userreg.objects.all()
    context={'Applicants':users}
    template = loader.get_template("dces/admin/applicants.html")
    return HttpResponse(template.render(context,request))

#view all house Application
def allApps(request):
    H = House.objects.filter(Status='Verify')
    F = Farm.objects.filter(Status='Verify')
    A = Agriculture.objects.filter(Status='Verify')
    context={'house':H,'farm':F,'agri':A}
    return render(request, "dces/admin/allapps.html",context)
#view house
def viewHouse(request,hno):
    H=House.objects.filter(Houseno=hno).values()
    U=Userreg.objects.filter(id=H[0]['Applicationno_id'])
    DM=Disaster_amount.objects.filter(Affectedno=hno,Applicationno=H[0]['Applicationno_id'])
    context = {'house': H, 'users': U,'Amount':DM}
    return render(request, "dces/admin/house.html", context)

#view farm
def viewFarm(request,fno):
    H =Farm.objects.filter(Farmno=fno).values()
    U =Userreg.objects.filter(id=H[0]['Applicationno_id'])
    DM=Disaster_amount.objects.filter(Affectedno=fno,Applicationno=H[0]['Applicationno_id'])
    context = {'farm': H, 'users': U,'Amount':DM}
    return render(request, "dces/admin/farm.html", context)

#view Agriculture
def viewAgri(request,id):
    A = Agriculture.objects.filter(id=id).values()
    U = Userreg.objects.filter(id=A[0]['Appno_id'])
    DM=Disaster_amount.objects.filter(Affectedno=id,Applicationno=A[0]['Appno_id'])
    context = {'agri': A, 'users': U,'Amount':DM}
    return render(request, "dces/admin/agriculture.html", context)

def errorpage(request):
    return render(request,"dces/error.html")


def exit(request):
    return render(request,"dces/index.html")


#common event list
def events(request):
    events=Event.objects.all()
    context={'events':events}
    template = loader.get_template("dces/events.html")
    return HttpResponse(template.render(context,request))


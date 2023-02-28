from django.urls import re_path
from .import views
urlpatterns = [
    re_path(r'^$',views.index),
    #Amdin
    re_path(r'errorpage/$',views.errorpage,name='errorpage'),
    re_path(r'adminlogin/$',views.adminlogin,name='adminlogin'),
    re_path(r'allApps/$',views.allApps,name='allApps'),
    re_path(r'achngpwd/(\w+)$',views.achngpwd,name='achngpwd'),
    re_path(r'adminlogout/$',views.adminlogout,name='adminlogout'),

    re_path(r'villageregistration/$',views.villageregistration,name='villageregistration'),
    re_path(r'villageoficers/$',views.villageoficers,name='villageoficers'),
    re_path(r'delOfficer/(\d+)$',views.delOfficer,name='delOfficer'),

    re_path(r'managerreg/$',views.managerreg,name='managerreg'),
    re_path(r'managers/$',views.managers,name='managers'),
    re_path(r'delManager/(\w+)$',views.delManager,name='delManager'),

    re_path(r'applicants/$',views.applicants,name='applicants'),
    re_path(r'delApplicant/(\d+)$',views.delApplicant,name='delApplicant'),

    re_path(r'allApps/$',views.allApps,name='allApps'),
    re_path(r'viewHouse/(\d+)$',views.viewHouse,name='mviewHouse'),
    re_path(r'viewFarm/(\d+)$',views.viewFarm,name='mviewFarm'),
    re_path(r'viewAgri/(\d+)$',views.viewAgri,name='mviewAgri'),


    # User or Victim
    re_path(r'victim/$',views.victim,name='victim'),
    re_path(r'userreg/$',views.userreg,name='userreg'),
    re_path(r'userpers/$',views.userpers,name='userpers'),
    re_path(r'uprofile/(\d+)$',views.uprofile,name='uprofile'),
    re_path(r'userchgpwd/$',views.userchgpwd,name='userchgpwd'),
    re_path(r'victimlogout/$',views.victimlogout,name='victimlogout'),

    re_path(r'house/$',views.house,name='house'),
    re_path(r'farm/$',views.farm,name='farm'),
    re_path(r'agriculture/$',views.agriculture,name='agriculture'),

    re_path(r'viewhouse/(\d+)$',views.viewhouse,name='vhouse'),
    re_path(r'viewfarm/(\d+)$',views.viewfarm,name='vfarm'),
    re_path(r'viewagriculture/(\d+)$',views.viewagriculture,name='vagriculture'),

    re_path(r'vhouse/(\d+)$',views.vhouse,name='vhouse'),
    re_path(r'vfarm/(\d+)$',views.vfarm,name='vfarm'),
    re_path(r'vagriculture/(\d+)$',views.vagriculture,name='vagriculture'),

    #village officer
    re_path(r'vlogin/$',views.vLogin,name='vlogin'),
    re_path(r'vlogout/$',views.vlogout,name='vlogout'),
    re_path(r'vprofile/(\d+)$',views.vprofile,name='vprofile'),
    re_path(r'veditprofile/(\d+)$',views.veditprofile,name='veditprofile'),
    re_path(r'vchngpwd/(\d+)$',views.vchngpwd,name='vchngpwd'),
    
    re_path(r'vlgallapps/(\d+)$',views.vlgallapps,name='vlgallapps'),
    re_path(r'vvapps/(\d+)$',views.vvapps,name='vvapps'),
    re_path(r'vlgallappsnot/(\d+)$',views.vlgallappsnot,name='vlgallappsnot'),

    re_path(r'vviewHouse/(\d+)$',views.vviewHouse,name='vviewHouse'),
    re_path(r'vverifyhouse/(\d+)$',views.vverifyhouse,name='vverifyhouse'),
    

    re_path(r'vviewFarm/(\d+)$',views.vviewFarm,name='vviewFarm'),
    re_path(r'vverifyfarm/(\d+)$',views.vverifyfarm,name='vverifyfarm'),

    re_path(r'vviewAgri/(\d+)$',views.vviewAgri,name='vviewAgri'),
    re_path(r'vverifyagriculture/(\d+)$',views.vverifyagriculture,name='vverifyagriculture'),

    re_path(r'hcompute/(\d+)$',views.hcompute,name='hcompute'),
    re_path(r'fcompute/(\d+)$',views.fcompute,name='fcompute'),
    re_path(r'Acompute/(\d+)$',views.Acompute,name='Acompute'),

    re_path(r'veventadd/$',views.veventadd,name='veventadd'),
    re_path(r'eventlist/$',views.eventlist,name='eventlist'),

    #Manager
    re_path(r'mlogin/$',views.mlogin,name='mlogin'),
    re_path(r'mprofile/$',views.mprofile,name='mprofile'),
    re_path(r'meditprofile/$',views.meditprofile,name='meditprofile'),
    re_path(r'mchngpwd/$',views.mchngpwd,name='mchngpwd'),
    re_path(r'mlogout/$',views.mlogout,name='mlogout'),

    re_path(r'mallapps/$',views.mallapps,name='mallapps'),
    re_path(r'mviewHouse/(\d+)$',views.mviewHouse,name='mviewHouse'),
    re_path(r'mviewFarm/(\d+)$',views.mviewFarm,name='mviewFarm'),
    re_path(r'mviewAgri/(\d+)$',views.mviewAgri,name='mviewAgri'),

    re_path(r'mvallapps/$',views.mvallapps,name='mvallapps'),
    re_path(r'mrallapps/$',views.mrallapps,name='mrallapps'),
    re_path(r'mpallapps/$',views.mpallapps,name='mpallapps'),

    #outside
    re_path(r'ueventlist/$',views.ueventlist,name='ueventlist'),
    re_path(r'events/$',views.events,name='events'),
    re_path(r'exit/$',views.exit,name='exit'),
]

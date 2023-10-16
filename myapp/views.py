from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from myapp.form import SignUpForm, ProfileForm
from myapp.models import Profile, member, site, Open_ticket, ticket_stat, Downtime, tech_action
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from .my_function import objects_to_df, from_df
import os
from base64 import b64decode
from django.conf import settings
from pathlib import Path 
from django.core.files import File

sectionList = ['Other', 'PC', 'MC', 'JP', 'Rotor', 'Fin_PC', 'Fin_MC', 'Impeller', 'Stator', 'Assy', 'Final_Inspection', 'AIDA_DieCast']

sectionSites = ['Others','Pump Cashing','Motor Cashing','Jet Pump', 'Rotor','Finishing_PC','Finishing_MC','Impeller','Stator','Assy','Final Inspection','AIDA-DieCast']

#class SignUpView(generic.CreateView):
#    form_class = UserCreationForm
#    success_url = reverse_lazy("login")
#    template_name = "myapp/account/signup.html"

def user_role(usr_data):
    role = ''
    if usr_data['is_admin']:
        role = 'admin'
    elif usr_data['is_tech']:
        role ='technician'
    elif usr_data['is_lead']:
        role='Leader'
    elif usr_data['is_super']:
        role='Supervisor'    
    return role

@ensure_csrf_cookie
def register_user(request):
    resp = {"status":'failed','msg':'','link':'','section':''}
    fullname = None
    username = None
    reg_email = None
    section = None
    password = None
    re_password = None

    if request.POST:
        fullname = request.POST['reg_fullname']
        username =request.POST['reg_username']
        reg_email = request.POST['reg_email']
        section = request.POST['reg_section']
        password = request.POST['reg_password']
        re_password = request.POST['reg_re-password']
        
        if fullname and username and reg_email and section and password and re_password:
            user1 = User.objects.filter(username=username).first()
            if user1:
                resp['msg'] = 'Username sudah terpakai pilih yang lain'
            else:
                if password == re_password :
                    user = User.objects.create_user(
                        first_name = fullname,
                        email = reg_email,
                        username = username,
                        password = password,
                    )
                    user.save()
                    sectionIdx = sectionList.index(section) + 1
                    profile_update = Profile.objects.last()
                    profile_update.section = sectionIdx
                    profile_update.save()
                    resp['status'] = 'success'
                    
                else :
                    resp['msg'] = 'Password tidak sama'
        
    return HttpResponse(json.dumps(resp),content_type='application/json')


@ensure_csrf_cookie
def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':'','link':'','section':''}
    username = ''
    password = ''
    usr_role = ''
   
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            user_profile = Profile.objects.filter(user_id=user.id).values()
            is_active = (user_profile[0])['is_active']
            if is_active:
                resp['link'] = user_role(user_profile[0])
                if resp['link'] == "":
                   resp['msg'] = "User not activated yet. Please contact administrator"   
            else:
                resp['msg'] = "User not activated yet. Please contact administrator"
            
            # print(resp['link'])

            if resp['link'] != '':
                login(request, user)
                resp['status'] = 'success'
                resp['section'] = sectionList[(user_profile[0])['section']-1]
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')

def logoutuser(request):
    logout(request)
    return redirect('/')

@login_required
def choose(request):
    template = ''
    template_all = Dashboard
    user_profile = Profile.objects.filter(user_id=request.user.id).values()
    
    if user_profile[0]['is_admin']:
        template = MyDashboard
    elif user_profile[0]['is_tech']:
        if user_profile[0]['is_lead']:
            template = template_all#DashboardPE_lead
        elif user_profile[0]['is_super']:
            template = template_all#DashboardPE_Super
        else:
            template = template_all#DashboardPE
            # print('PE')
    elif user_profile[0]['is_lead']:
        template = template_all#DashboardLead
    elif user_profile[0]['is_super']:
        template = template_all#DashboardSuper
    else:
        logout(request)
    return redirect(template)

@login_required   
def Dashboard(request):
    if request.method == 'GET':
        if request.user.is_active:
            usr_id = (request.user.id)
            user_profile = Profile.objects.filter(user_id=usr_id).first()
            context = {
                'usr_profile' : user_profile,
                'page_title' : 'test',
            }
            return render(request, 'user/index.html', context)
    
    return render(request, 'user/index.html')

@login_required   
def MyDashboard(request):
    user_profile = Profile.objects.filter(user_id=request.user.id).values()
    if user_profile[0]['is_admin']:
        if request.method == 'GET':
            if request.user.is_active:
                usr_id = (request.user.id)
                user_profile = Profile.objects.filter(user_id=usr_id).first()
                context = {
                    'usr_profile' : user_profile,
                    'page_title' : 'test',
                }
                return render(request, 'user/dashboard.html', context)
    else:
        logout(request)

    return render(request, 'user/dashboard.html')

@login_required   
def DashboardPE(request):
    if request.method == 'GET':
        if request.user.is_active:
            usr_id = (request.user.id)
            user_profile = Profile.objects.filter(user_id=usr_id).first()
            context = {
                'usr_profile' : user_profile,
                'page_title' : 'test',
            }
            return render(request, 'user/dashboard_pe.html', context)
    
    return render(request, 'user/dashboard_pe.html')

@login_required   
def DashboardPE_lead(request):
    if request.method == 'GET':
        if request.user.is_active:
            usr_id = (request.user.id)
            user_profile = Profile.objects.filter(user_id=usr_id).first()
            context = {
                'usr_profile' : user_profile,
                'page_title' : 'test',
            }
            return render(request, 'user/dashboard_pe_lead.html', context)
    
    return render(request, 'user/dashboard_pe_lead.html')

@login_required   
def DashboardPE_Super(request):
    if request.method == 'GET':
        if request.user.is_active:
            usr_id = (request.user.id)
            user_profile = Profile.objects.filter(user_id=usr_id).first()
            context = {
                'usr_profile' : user_profile,
                'page_title' : 'test',
            }
            return render(request, 'user/dashboard_pe_super.html', context)
    
    return render(request, 'user/dashboard_pe_super.html')

@login_required   
def DashboardLead(request):
    if request.method == 'GET':
        if request.user.is_active:
            usr_id = (request.user.id)
            user_profile = Profile.objects.filter(user_id=usr_id).first()
            context = {
                'usr_profile' : user_profile,
                'page_title' : 'test',
            }
            return render(request, 'user/dashboard_lead.html', context)
    
    return render(request, 'user/dashboard_lead.html')

@login_required   
def DashboardSuper(request):
    if request.method == 'GET':
        if request.user.is_active:
            usr_id = (request.user.id)
            user_profile = Profile.objects.filter(user_id=usr_id).first()
            context = {
                'usr_profile' : user_profile,
                'page_title' : 'test',
            }
            return render(request, 'user/dashboard_super.html', context)
    
    return render(request, 'user/dashboard_lead.html')

@ensure_csrf_cookie
@login_required
def load_combo(request):
    resp = {"status":'failed','msg':'','count':''}
    if request.method == 'POST':
        site_lists=[]
        site_bak=[]
        site_buff=''
        data = request.POST['site_name']
        usr_id = (request.user.id)
        user_profile = Profile.objects.filter(user_id=usr_id).first()
        site_req = site.objects.filter(name=data, section=user_profile.section).values()
        for i in range(len(site_req)):
            try:
                site_buff = site_bak.index(site_req[i]['sub_name'])
            except ValueError:
                site_bak.append(site_req[i]['sub_name'])
        
        site_lists = site_bak
        if len(site_lists) > 0:
            resp['msg'] = site_lists
            resp['status'] = 'success'
        else:
            resp['msg'] = "Data Corrupt !!!"
    return HttpResponse(json.dumps(resp),content_type='application/json')

@login_required
@ensure_csrf_cookie
def tech_member(request):
    resp = {"status":'failed','msg':'','count':''}
    maint_name=[]
    if request.method == 'POST':
        if request.user.is_active:
            data = request.POST['shift']
            if data == '1':
                maint_member = member.objects.filter(shift=0).values()
                for x in range (len(maint_member)):
                    maint_name.append(maint_member[x]['name'])
            maint_member = member.objects.filter(shift=data).values()
            for x in range (len(maint_member)):
                maint_name.append(maint_member[x]['name'])    
            resp['msg'] = maint_name
            resp['status'] = 'success'
    return HttpResponse(json.dumps(resp),content_type='application/json')

@login_required
@ensure_csrf_cookie
def sites(request):
    sites_list = site.objects.all()
    StrID = sites_list.order_by('section').values()
    for x in range(len(StrID)):
        StrID1 = StrID[x]
        StrID1['section'] = sectionSites[(StrID1['section']-1)]
    usr_id = (request.user.id)
    user_profile = Profile.objects.filter(user_id=usr_id).first()
    # category_list = {}
    # print(StrID)
    context = {
        'page_title' : 'Category List',
        'sites' : StrID,
        'usr_profile' : user_profile,
    }
   
    return render(request, 'data/sites.html',context)

@login_required
def ticket_lead(request):
    user_profile = Profile.objects.filter(user_id=request.user.id).first()
    # print(user_profile.section)
    ticket_list = Open_ticket.objects.filter(site_section=user_profile.section)
    StrID = ticket_list.values()
    # category_list = {}
    context = {
        'page_title' : 'Category List',
        'ticket' : StrID,
        'usr_profile' : user_profile,
    }

    return render(request, 'data/ticket_lead.html',context)

@login_required
def ticket_finish(request):
    user_profile = Profile.objects.filter(user_id=request.user.id).first()
    # print(user_profile.section)
    ticket_list = Open_ticket.objects.filter(site_section=user_profile.section, status='finished')
    StrID = ticket_list.values()
    # category_list = {}
    context = {
        'page_title' : 'Category List',
        'ticket' : StrID,
        'usr_profile' : user_profile,
    }

    return render(request, 'data/ticket_finish.html',context)

@login_required
def ticket_lead_pe(request):
    user_profile = Profile.objects.filter(user_id=request.user.id).first()
    ticket_list = Open_ticket.objects.exclude(status='Waiting Supervisor Approval').values()
    test = ticket_stat.objects.exclude(super_approve_time=None)
    test = test.exclude(pe_approved_time__isnull=True).values()
    for x in range (len(test)):
        ticket_list = ticket_list.exclude(ticket_id = test[x]['ticket_id'])
    StrID = ticket_list#.values().order_by('time_issue')
    for x in range(len(StrID)):
        StrID1 = StrID[x]
        StrID1['site_section'] = sectionSites[(StrID1['site_section']-1)]

    context = {
        'page_title' : 'Category List',
        'ticket' : StrID,
        'usr_profile' : user_profile,
    }

    return render(request, 'data/ticket_lead_pe.html',context)

@login_required
def ticket_super_pe(request):
    user_profile = Profile.objects.filter(user_id=request.user.id).first()
    down_list3 = Downtime.objects.filter(complete=False, reasons='Take Action', approved=False).exclude(kyt_image='').values()
    for x in range(len(down_list3)):
        StrID1 = down_list3[x]
        StrID1['site_section'] = sectionSites[(StrID1['site_section']-1)]
    # category_list = {}
    context = {
        'page_title' : 'Category List',
        'ticket' : down_list3,
        'usr_profile' : user_profile,
    }

    return render(request, 'data/ticket_super_pe.html',context)

@login_required
def permohonan_perbaikan(request):
    user_profile = Profile.objects.filter(user_id=request.user.id).first()
    down_list = Downtime.objects.filter(complete=False, reasons='Take Action', kyt_image='').values()
    for x in range(len(down_list)):
        StrID3 = down_list[x]
        StrID3['site_section'] = sectionSites[(StrID3['site_section']-1)]
    down_list2 = Downtime.objects.filter(complete=False, approved=True, taken=False).values()
    for x in range(len(down_list2)):
        StrID2 = down_list2[x]
        StrID2['site_section'] = sectionSites[(StrID2['site_section']-1)]
        time = ticket_stat.objects.filter(ticket_id=down_list2[x]['ticket_id']).first()
        StrID2['approved'] = time.pe_man_approved_time
    down_list3 = Downtime.objects.filter(complete=False, reasons='Take Action', approved=False).exclude(kyt_image='').values()
    for x in range(len(down_list3)):
        StrID1 = down_list3[x]
        StrID1['site_section'] = sectionSites[(StrID1['site_section']-1)]
    # category_list = {}
    context = {
        'page_title' : 'Category List',
        'ticket' : down_list,
        'approved' : down_list3,
        'ready':down_list2,
        'usr_profile' : user_profile,
    }

    return render(request, 'data/permohonan_perbaikan.html',context)


@login_required
def ticket_super(request):
    user_profile = Profile.objects.filter(user_id=request.user.id).first()
    # print(user_profile.section)
    ticket_list = Open_ticket.objects.filter(site_section=user_profile.section, status='Waiting Supervisor Approval')
    StrID = ticket_list.values()
    # category_list = {}
    context = {
        'page_title' : 'Category List',
        'ticket' : StrID,
        'usr_profile' : user_profile,
    }

    return render(request, 'data/ticket_super.html',context)

@login_required
@ensure_csrf_cookie
def super_approval(request):
    data =  request.POST
    resp = {'status':''}
    try:
        site.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Category Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def manage_ticket(request):
    site_lists = ''
    site_bak = []
    if request.method == 'GET':
        user_profile = Profile.objects.filter(user_id=request.user.id).values()
        site_list = site.objects.filter(section=user_profile[0]['section']).values()
        for i in range(len(site_list)):
            try:
                site_buff = site_bak.index(site_list[i]['name'])
            except ValueError:
                site_bak.append(site_list[i]['name'])
        
        site_lists = site_bak

    context = {
        'sites' : site_lists,
    }


    return render(request, 'data/manage_ticket.html',context)

@login_required
def manage_ticket_super(request):
    site_lists = ''
    site_bak = []
    if request.method == 'GET':
        ticket_detail = Open_ticket.objects.filter(id=request.GET['id']).first()

    context = {
        'ticket' : ticket_detail,
    }

    return render(request, 'data/manage_ticket_super.html',context)

@login_required
def manage_ticket_lead_pe(request):
    site_lists = ''
    if request.method == 'GET':
        ticket_detail = Open_ticket.objects.filter(id=request.GET['id']).first()
        ticket_detail.site_section=sectionSites[ticket_detail.site_section-1]
           
    context = {
        'ticket' : ticket_detail,
    }

    return render(request, 'data/manage_ticket_lead_pe.html',context)

@login_required
def manage_permohonan_perbaikan(request):
    
    if request.method == 'GET':
        # print(request.GET)
        ticket_detail = Downtime.objects.filter(id=request.GET['id']).first()

    context = {
        'ticket' : ticket_detail,
    }

    return render(request, 'data/manage_permohonan_perbaikan.html',context)

@login_required
def manage_eksekusi(request):
    
    if request.method == 'GET':
        data= request.GET
        if (data['id']).isnumeric() and int(data['id']) > 0 :
            ticket_detail = Downtime.objects.filter(id=request.GET['id']).first()
            ticket_detail.site_section = sectionSites[ticket_detail.site_section-1]
        else:
            logout(request)

    context = {
        'ticket' : ticket_detail,
    }

    return render(request, 'data/manage_eksekusi.html',context)

@login_required
def manage_ready_eksekusi(request):
    
    if request.method == 'GET':
        ticket_detail = Downtime.objects.filter(id=request.GET['id']).first()
        ticket_detail.site_section = sectionSites[ticket_detail.site_section-1]

    context = {
        'ticket' : ticket_detail,
    }

    return render(request, 'data/manage_ready_eksekusi.html',context)

@login_required
def aproval_permohonan_perbaikan(request):
    
    if request.method == 'GET':
        ticket_detail = Downtime.objects.filter(id=request.GET['id']).first()

    context = {
        'ticket' : ticket_detail,
    }

    return render(request, 'data/aproval_permohonan_perbaikan.html',context)

@login_required
def show_kyt_image(request):
    
    if request.method == 'GET':
        ticket_detail = Downtime.objects.filter(id=request.GET['id']).first()

    context = {
        'ticket' : ticket_detail,
    }

    return render(request, 'data/show_kyt_image.html',context)

@login_required
def breakdown_list(request):
    months = datetime.datetime.now().month
    years = datetime.datetime.now().year
    user_profile = Profile.objects.filter(user_id=request.user.id).first()
    down_list1 = Downtime.objects.filter(complete=True).exclude(time_finish=None).filter(time_finish__year=years).filter(time_finish__month=months).values()
    for x in range(len(down_list1)):
        StrID2 = down_list1[x]
        duration1 = ticket_stat.objects.filter(ticket_id=down_list1[x]['ticket_id']).first()
        duration = '{:.0f}'.format((down_list1[x]['time_finish'] - duration1.pe_approved_time).total_seconds()/60)
        StrID2['time_finish'] = int(duration)
        data_in = tech_action.objects.filter(ticket_id=down_list1[x]['ticket_id']).first()
        StrID2['user_name'] = data_in.closed_by
        StrID2['reasons'] = data_in.action_taken
        StrID2['site_section'] = sectionSites[(StrID2['site_section']-1)]
    down_list2 = Downtime.objects.filter(complete=False, approved=True, taken=True).values()
    for x in range(len(down_list2)):
        StrID2 = down_list2[x]
        StrID2['site_section'] = sectionSites[(StrID2['site_section']-1)]
        time = tech_action.objects.filter(ticket_id=down_list2[x]['ticket_id']).first()
        StrID2['taken'] = time.pe_start
        StrID2['user_name'] = time.taken_by
        time2 = ticket_stat.objects.filter(ticket_id=down_list2[x]['ticket_id']).first()
        StrID2['approved'] = time2.pe_man_approved_time
    # category_list = {}
    context = {
        'page_title' : 'Category List',
        'ticket' : down_list1, 
        # 'approved' : down_list3,
        'ready':down_list2,
        'usr_profile' : user_profile,
    }

    return render(request, 'data/breakdown_list.html',context)

@login_required
@ensure_csrf_cookie
def save_ready_action(request):
    if request.POST:
        resp = {'status':'failed'}
        data = request.POST
        try:
            if (data['id']).isnumeric() and int(data['id']) > 0 :
                data_in=Downtime.objects.filter(id=data['id']).first()
                data_out=tech_action.objects.filter(ticket_id=data_in.ticket_id)
                if (len(data_out)) == 0:
                    data_save=tech_action(taken_by=request.user, ticket_id=data_in.ticket_id,pe_start=timezone.now(), pe_finish=None,closed=None,closed_by='',action_taken='',sparepart='')
                    data_save.save()
                else:
                    print('ok')
                updated = Downtime.objects.filter(ticket_id=data_in.ticket_id).update(taken=True)
                updated = Open_ticket.objects.filter(ticket_id=data_in.ticket_id).update(status=str(request.user)+ ' is on duty')
                resp['status'] = 'success'
        except:
            resp['status'] = 'failed'
        
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
@ensure_csrf_cookie
def save_eksekusi(request):
    resp = {'status':'failed'}
    if request.POST:
        data = request.POST
        try:
            if (data['id']).isnumeric() and int(data['id']) > 0 :
                data_in = Downtime.objects.filter(id=data['id']).update(spare_part=request.POST['spare_part'], complete=True, analisis=request.POST['action_analisis'])
                pointer = Downtime.objects.filter(id=data['id']).first()
                user = str(request.user)
                data_out = tech_action.objects.filter(ticket_id=pointer.ticket_id).update(closed_by=user ,pe_finish=timezone.now(), action_taken=request.POST['action_counter'], sparepart=request.POST['spare_part'])
                ticket = Open_ticket.objects.filter(ticket_id=pointer.ticket_id).update(status='finished')
                resp['status'] = 'success'
        except:
            resp['status'] = 'failed'
        
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
@ensure_csrf_cookie
def save_permohonan_perbaikan(request):
    
    if request.POST:
        resp = {'status':'failed'}
        data = request.POST
        try:
            if (data['id']).isnumeric() and int(data['id']) > 0 :
                base64Image =  request.POST['uploadfile']
                id_data = Downtime.objects.filter(id=request.POST['id']).first()
                header, encoded = base64Image.split("base64,", 1)
                base64_enc = b64decode(encoded)
                filename = 'kyt_'+ str(id_data.ticket_id) +'.png'
                # store temp image file
                with open(filename, "wb") as f:
                    f.write(base64_enc)
                kyt_data = Downtime.objects.get(id=id_data.id)
                # store current dir
                cur_dir = os.getcwd()
                # change to media directory and remove file if exist
                os.chdir(os.path.join(settings.MEDIA_ROOT, (kyt_data.kyt_image.field.upload_to).removesuffix('/')))
                if os.path.exists(filename):
                    os.remove(filename)
                # back to temp directory
                os.chdir(cur_dir)
                kyt_data.kyt_image.save(filename,File(open(filename,'rb')))
                kyt_data.save()
                # remove file temp
                if os.path.exists(filename):
                    os.remove(filename)
                resp['status'] = 'success'
        except:
            resp['status'] = 'failed'
        
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
@ensure_csrf_cookie
def super_approve_permohonan(request):
    if request.POST:
        resp = {'status':'failed'}
        data = request.POST
        try:
            if (data['id']).isnumeric() and int(data['id']) > 0 :
                select=Downtime.objects.filter(id=data['id'])
                update=select.update(approved=True)
                update=Open_ticket.objects.filter(ticket_id=select.first().ticket_id).update(status='Ready for execution')
                update=ticket_stat.objects.filter(ticket_id=select.first().ticket_id).update(pe_man_approved_time=timezone.now())
                resp['status'] = 'success'
        except:
            resp['status'] = 'failed'
        
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
@ensure_csrf_cookie
def save_ticket_lead(request):
    if request.POST:
        section = Profile.objects.filter(user_id=request.user.id).values()
        data =  request.POST
        resp = {'status':'failed'}
        SectionId = (section[0]['section'])
        ticketId = Open_ticket.objects.all().last()
        if ticketId != None :
            Id = ticketId.ticket_id+1
        else:
            Id = 100
        try:
            if (data['id']).isnumeric() and int(data['id']) > 0 :
                pointer = Open_ticket.objects.filter(id=data['id']).first()
                data_rec = ticket_stat.objects.filter(ticket_id=pointer.ticket_id).update(super_approve_time=timezone.now())
                data_rec2 = Open_ticket.objects.filter(id=data['id']).update(status='Waiting PE Approval')
                resp['status'] = 'success'
            else :
                save_ticket = Open_ticket(ticket_id=Id, user_name = request.user.username,site_name=data['name'],site_sub_name=data['sub_name'],site_section = SectionId,description=data['description'],status="Waiting Supervisor Approval")
                save_ticket.save()
                save_ticket2 = ticket_stat(ticket_id=Id,super_approve_time = None, pe_approved_time = None, pe_man_approved_time = None)
                save_ticket2.save()
                resp['status'] = 'success'
            # messages.success(request, 'Sites Successfully saved.')
        except:
            # print(request.user.username)
            resp['status'] = 'failed'
        # print(resp['status'])
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
@ensure_csrf_cookie
def save_ticket_lead_pe(request):
    if request.POST:
        section = Profile.objects.filter(user_id=request.user.id).values()
        data =  request.POST
        # print(data)
        resp = {'status':'failed'}
        try:
            pointer = Open_ticket.objects.filter(id=data['id']).first()
            data_rec = ticket_stat.objects.filter(ticket_id=pointer.ticket_id).update(pe_approved_time=timezone.now())
            data_rec = ticket_stat.objects.filter(ticket_id=pointer.ticket_id).first()
            downtime_rec = Downtime(ticket_id=pointer.ticket_id, user_name=pointer.user_name, site_name=pointer.site_name, site_sub_name=pointer.site_sub_name,site_section=pointer.site_section,description=pointer.description,time_issue=data_rec.pe_approved_time,status=request.POST['action'],time_finish=None,analisis=None,spare_part=None,reasons=request.POST['action'],kyt_image=None,complete=False)
            
            downtime_rec.save()
            resp['status'] = 'success'
        except:
            resp['status'] = 'failed'
        
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
@ensure_csrf_cookie
def manage_sites(request):
    category = {}
    section = sectionSites
    if request.method == 'GET':
        data =  request.GET
        id = ''
        sites = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            sites = site.objects.filter(id=id).first()
            sites.section = sectionSites[sites.section-1]
    
    context = {
        'category' : sites,
        'section' : section,
    }

    return render(request, 'data/manage_sites.html',context)

@login_required
@ensure_csrf_cookie
def save_sites(request):
    data =  request.POST
    resp = {'status':'failed','msg':''}
    try:
        sectionID  = sectionSites.index(data['section']) + 1
        # print(sectionID)
        if (data['id']).isnumeric() and int(data['id']) > 0 :
            save_sites = site.objects.filter(id = data['id']).update(name=data['name'], sub_name = data['sub_name'], section = sectionID)
            resp['status'] = 'success'
            resp['msg'] = 'Sites Successfully Updated'
        else:
            cek_site = site.objects.filter(name=data['name'], sub_name = data['sub_name'],section = sectionID)
            if len(cek_site) == 0 :
                save_sites = site(name=data['name'], sub_name = data['sub_name'],section = sectionID)
                save_sites.save()
                resp['status'] = 'success'
                resp['msg'] = 'Sites Successfully saved'
            else:
                resp['status'] = 'failed'
                resp['msg'] = 'SIte sudah ada sebelumnya'
    except:
        resp['status'] = 'failed'
    
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
@ensure_csrf_cookie
def delete_sites(request):
    data =  request.POST
    resp = {'status':''}
    try:
        site.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Category Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
@ensure_csrf_cookie
def complete_action(request):
    data =  request.POST
    resp = {'status':''}
    try:
        data_in = Open_ticket.objects.filter(id=data['id']).first()
        complete = Open_ticket.objects.filter(id=data['id']).update(status='complete')
        data_out = tech_action.objects.filter(ticket_id=data_in.ticket_id).update(closed=timezone.now())
        data_out = Downtime.objects.filter(ticket_id=data_in.ticket_id).update(time_finish=timezone.now())
        resp['status'] = 'success'
        messages.success(request, 'Job Complete')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required  
def gen_chart(request):

    request_att = request.GET.get('att')
    request_scale = request.GET.get('scale')

    labels = []
    data = []

    SECTION_NAME = sectionSites
    
    #scalling date => dataframe queries
    if request_scale == 'overall':
        months = datetime.datetime.now().month
        years = datetime.datetime.now().year
        time_scale = '%Y-%m-%d'
        
        down_list1 = list(Downtime.objects.filter(complete=True).exclude(time_finish=None).filter(time_finish__year=years).filter(time_finish__month=months).values())
        for x in range(len(down_list1)):
            StrID2 = down_list1[x]
            StrID2['site_section'] = sectionSites[(StrID2['site_section']-1)]
            duration1 = ticket_stat.objects.filter(ticket_id=down_list1[x]['ticket_id']).first()
            duration = '{:.0f}'.format((down_list1[x]['time_finish'] - duration1.pe_approved_time).total_seconds()/60)
            StrID2['status'] = int(duration) 
            StrID2['description'] = str(down_list1[x]['site_name']) + ' ' + str(down_list1[x]['site_sub_name'])

        df = objects_to_df(down_list1, fields=['ticket_id','site_section','time_finish', 'status', 'description'] ,date_cols=[time_scale, 'time_finish'], col_replace=['status','duration'])

        data, x = from_df(df,'duration','site_section','date')

   
    if request_att == 'all_ch':
        # total data frame
        aku = df.groupby('site_section').sum().sort_values(by=['duration'], ascending=False)
        labels = aku.index.to_list()
        values = aku['duration'].to_list()


        total = dict(zip(labels, values))
    #     #big 3 dataframe
        aku2 = df.groupby('description').sum().sort_values(by=['duration'], ascending=False).iloc[:5].drop(['ticket_id'], axis=1)
        print(df)
        print(aku2)
        labels = aku2.index.to_list()
        values = aku2['duration'].to_list()

        detail = dict(zip(labels, values))

    return JsonResponse(data={
        'labels': x,
        'data': data,
        'total': total,
        'detail':detail
        })

from django.urls import path,re_path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings

from django.conf.urls.static import static


sectionList = ['Other', 'PC', 'MC', 'JP', 'Rotor', 'Fin_PC', 'Fin_MC', 'Impeller', 'Stator', 'Assy', 'Final_Inspection', 'AIDA_DieCast']
urlpatterns=[
    path('', views.choose, name=''),
    path('dashboard', views.MyDashboard, name='dashboard'),
    path('dashboard_all', views.Dashboard, name='dashboard_all'),
     path('genchar/', views.gen_chart, name='gen-chart'),
    path('ticket_finish', views.ticket_finish, name='ticket_finish'),
    path('dash_pe', views.DashboardPE, name='dash_pe'),
    path('complete_action', views.complete_action, name='complete_action'),
    path('dash_pe_lead', views.DashboardPE_lead, name='dash_pe_lead'),
    path('dash_pe_super', views.DashboardPE_Super, name='dash_pe_super'),
    path('dash_lead', views.DashboardLead, name='dash_lead'),
    path('dash_super', views.DashboardSuper, name='dash_super'),
    # site manage section
    path('sites', views.sites, name='sites'),
    path('manage_sites', views.manage_sites, name="manage_sites"),
    path('save_sites', views.save_sites, name="save_sites"),
    path('delete_sites', views.delete_sites, name="delete_sites"),
    # site manage end
    # ticker manage section
    path('ticket_lead', views.ticket_lead, name='ticket_lead'),
    path('ticket_lead_pe', views.ticket_lead_pe, name='ticket_lead_pe'),
     path('ticket_super_pe', views.ticket_super_pe, name='ticket_super_pe'),
    path('ticket_super', views.ticket_super, name='ticket_super'),
    path('super_approval', views.super_approval, name='super_approval'),
    path('manage_ticket', views.manage_ticket, name="manage_ticket"),
    path('manage_ticket_lead_pe', views.manage_ticket_lead_pe, name="manage_ticket_lead_pe"),
    path('manage_ticket_super', views.manage_ticket_super, name="manage_ticket_super"),
    path('load_combo', views.load_combo, name="load_combo"),
    path('show_kyt_image', views.show_kyt_image, name="show_kyt_image"),
    path('breakdown_list', views.breakdown_list, name="breakdown_list"),
    path('save_ticket_lead', views.save_ticket_lead, name="save_ticket_lead"),
    path('save_ready_action', views.save_ready_action, name="save_ready_action"),
    path('save_ticket_lead_pe', views.save_ticket_lead_pe, name="save_ticket_lead_pe"),
    path('save_permohonan_perbaikan', views.save_permohonan_perbaikan, name="save_permohonan_perbaikan"),
    path('super_approve_permohonan', views.super_approve_permohonan, name="super_approve_permohonan"),
    path('permohonan_perbaikan', views.permohonan_perbaikan, name="permohonan_perbaikan"),
    path('manage_permohonan_perbaikan', views.manage_permohonan_perbaikan, name="manage_permohonan_perbaikan"),
    path('manage_ready_eksekusi', views.manage_ready_eksekusi, name="manage_ready_eksekusi"),
    path('aproval_permohonan_perbaikan', views.aproval_permohonan_perbaikan, name="aproval_permohonan_perbaikan"),
    # path('delete_ticket', views.delete_ticket, name="delete_ticket"),
    # ticket manage end
    path('save_eksekusi', views.save_eksekusi, name="save_eksekusi"),
    path('manage_eksekusi', views.manage_eksekusi, name="manage_eksekusi"),
    path('userlogin', views.login_user, name="login-user"),
    path('registeruser', views.register_user, name="register-user"),
    path('logout', views.logoutuser, name="logout"),
    path('login', auth_views.LoginView.as_view(extra_context={'test42': sectionList},template_name = 'account/login.html',redirect_authenticated_user=True), name="login"),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

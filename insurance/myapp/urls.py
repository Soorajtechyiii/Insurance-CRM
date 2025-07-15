from django.urls import path
from .import views

urlpatterns = [
   path('',views.home,name='home'),
   path('aboutus',views.aboutus,name='aboutus'),
   path('healthinsurance',views.healthinsurance,name='healthinsurance'),
   path('loginpage',views.loginpage,name='loginpage'),
   path('vehicle_health_insurance',views.vehicle_health_insurance,name='vehicle_health_insurance'),

   path('login_view',views.login_view,name='login_view'),

   path('adminhome',views.adminhome,name='adminhome'),
   path('add_agent',views.add_agent,name='add_agent'),
   path('validate-username/', views.validate_username, name='validate_username'),
   path('validate-email/', views.validate_email, name='validate_email'),
   path('validate-phone/', views.validate_phone, name='validate_phone'),
   path('agent_details',views.agent_details,name='agent_details'),
   path('edit/<int:id>',views.edit,name='edit'),
   path('edit_agent/<int:id>',views.edit_agent,name='edit_agent'),
   path('delete_agent/<int:id>',views.delete_agent,name='delete_agent'),
   path('client_application_details',views.client_application_details,name='client_application_details'),

   # campaign section
   path('add_campaign',views.add_campaign,name='add_campaign'),
   path('add_campaign_details',views.add_campaign_details,name='add_campaign_details'),
   path('show_campaign',views.show_campaign,name='show_campaign'),
   path('edit_campaign/<int:id>',views.edit_campaign,name='edit_campaign'),
   path('edit_campaign_details/<int:id>',views.edit_campaign_details,name='edit_campaign_details'),
   path('delete_campaign/<int:id>',views.delete_campaign,name='delete_campaign'),
   
   path('logoutadmin',views.logoutadmin,name='logoutadmin'),


   # userhome section
   path('userhome',views.userhome,name='userhome'),
   path('useredit',views.useredit,name='useredit'),
   path('reset_password',views.reset_password,name='reset_password'),
   path('client/<int:id>',views.client,name='client'),
   path('user_client',views.user_client,name='user_client'),
   path('validate-email-client/', views.validate_email_client, name='validate_email_client'),
   path('validate-phone-client/', views.validate_phone_client, name='validate_phone_client'),
   path('validate-aadhar/', views.validate_aadhar, name='validate_aadhar'),
   path('validate-pan/', views.validate_pan, name='validate_pan'),
   path('logoutuser',views.logoutuser,name='logoutuser'),
   # path('user_edit_details',views.user_edit_details,name='user_edit_details'),
]

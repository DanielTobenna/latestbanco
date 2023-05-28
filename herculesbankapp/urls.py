from django.urls import path

from . import views

urlpatterns=[
 path('', views.home, name='home'),
 path('about/', views.about, name='about'),
 path('current/', views.current, name='current'),
 path('kid/', views.kid, name='kid'),
 path('premium/', views.premium, name='premium'),
 path('saving/', views.saving, name='saving'),
 path('corporate/', views.corporate, name='corporate'),
 path('career/', views.career, name='career'),
 path('insurance/', views.insurance, name='insurance'),
 path('faq/', views.faq, name='faq'),
 path('card/', views.card, name='card'),
 path('contact/', views.contact, name='contact'),
 path('news/', views.news, name='news'),
 path('dashboard/', views.dashboard, name='dashboard'),
 path('account_settings/', views.account_settings, name='account_settings'),
 path('fundtransfer/', views.fundtransfer, name='fundtransfer'),
 path('foreign_transaction/', views.foreign_transaction, name='foreign_transaction'),
 path('transactionhistory/', views.transactionhistory, name='transactionhistory'),
 path('admindashboard/', views.admindashboard, name='admindashboard'),
 path('admincreateaccount/', views.admincreateaccount, name='admincreateaccount'),
 path('admingotouserprofile/<str:pk>/', views.admingotouserprofile, name='admingotouserprofile'),
 path('admincreditaccount/<str:pk>/', views.admincreditaccount, name='admincreditaccount'),
 path('admindebitaccount/<str:pk>/', views.admindebitaccount, name='admindebitaccount'),
 path('clientsignin/', views.clientsignin, name='clientsignin'),
 path('signup/', views.signup, name='signup'),
 path('logout/', views.logoutuser, name='logout'),
]
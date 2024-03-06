"""
URL configuration for helpdesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from aplicacion import views
from aplicacion.views import CambiarContraseñaView, CliCambiarContraseñaView, TecCambiarContraseñaView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index),

    path('accounts/login', views.login_user, name='login'),
    path('accounts/logout', views.logout_user, name='logout'),

    path('adm/dashboard', views.adm_dashboard, name='adm_dashboard'),
    path('adm/tickets', views.adm_tickets, name='adm_tickets'),
    path('adm/equipo', views.adm_equipo, name='adm_equipo'),
    path('adm/clientes', views.adm_clientes, name='adm_clientes'),
    path('adm/profile', views.adm_profile, name='adm_profile'),
    path('adm/create/cli', views.crear_cliente, name='create_cli'),
    path('adm/create/tec', views.crear_tecnico, name='create_tec'),
    path('adm/create/tick', views.crear_ticket, name='create_tick'),

    path('eliminar_cliente/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('eliminar_tecnico/<int:tecnico_id>/', views.eliminar_tecnico, name='eliminar_tecnico'),
    path('asignar_tecnico/<int:ticket_id>/', views.asignar_tecnico, name='asignar_tecnico'),
    path('ticket/<int:ticket_id>/agregar_respuesta/', views.agregar_respuesta, name='agregar_respuesta'),
    path('ticket/<int:ticket_id>/', views.detalle_ticket, name='detalle_ticket'),

    path('cambiar-contraseña/', CambiarContraseñaView.as_view(), name='cambiar_contraseña'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),


    path('cli/dashboard', views.cli_dashboard, name='cli_dashboard'),
    path('cli/profile', views.cli_profile, name='cli_profile'),
    path('cli/ticket', views.cli_ticket, name='cli_ticket'),
    path('cli/create/ticket', views.cli_crear_ticket, name='cli_crear_ticket'),
    path('cli/<int:ticket_id>/agregar_respuesta/', views.cli_agregar_respuesta, name='cli_agregar_respuesta'),
    path('cli/<int:ticket_id>/', views.cli_detalle_ticket, name='cli_detalle_ticket'),
    path('cli/cambiar-contraseña/', CliCambiarContraseñaView.as_view(), name='cli_cambiar_contraseña'),
    path('cli/edit-profile/', views.cli_edit_profile, name='cli_edit_profile'),


    path('download_archivo1/<int:ticket_id>/', views.download_archivo1, name='download_archivo1'),
    path('download_archivo2/<int:ticket_id>/', views.download_archivo2, name='download_archivo2'),

    path('tec/dashboard', views.tec_dashboard, name='tec_dashboard'),
    path('tec/profile', views.tec_profile, name='tec_profile'),
    path('tec/ticket', views.tec_ticket, name='tec_ticket'),
    path('tec/<int:ticket_id>/', views.tec_detalle_ticket, name='tec_detalle_ticket'),
    path('tec/<int:ticket_id>/agregar_respuesta/', views.tec_agregar_respuesta, name='tec_agregar_respuesta'),    
    path('tec/cambiar-contraseña/', TecCambiarContraseñaView.as_view(), name='tec_cambiar_contraseña'),
    path('tec/edit-profile/', views.tec_edit_profile, name='tec_edit_profile'),




]

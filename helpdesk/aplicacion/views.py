from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from .forms import ClienteForm, TecnicoForm, TicketsForm, AsignarTecnicoForm, RespuestaForm
from django.shortcuts import redirect, get_object_or_404

from .models import Administrador, Cliente, Estado, Tecnico, Ticket, Respuesta

# Create your views here.
@csrf_protect
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redireccionar según el grupo al que pertenece el usuario
            if user.groups.filter(name='Administracion').exists():
                return redirect('adm_dashboard')
            elif user.groups.filter(name='Tecnico').exists():
                return redirect('tec_dashboard')
            elif user.groups.filter(name='Cliente').exists():
                return redirect('cli_dashboard')
        else:
            return HttpResponse("Usuario o Contraseña incorrecta")
    # Devolver la plantilla de inicio de sesión para GET
    return render(request, 'registration/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

def index(request):
    return redirect('login')


##SECCION DE ADMINISTRACION
def adm_dashboard(request):
    return redirect('adm_tickets')

def adm_tickets(request):
    tickets = Ticket.objects.all()

    return render(request, 'administracion/tickets.html', {'tickets': tickets})

def adm_equipo(request):
    # Obtener todos los técnicos
    equipos = Tecnico.objects.all()

    return render(request, 'administracion/equipo.html', {'equipos': equipos})

def adm_clientes(request):
    # Obtener todos los clientes
    clientes = Cliente.objects.all()
    return render(request, 'administracion/clientes.html', {'clientes': clientes})

def crear_ticket(request):
    # Verificar si el usuario es de tipo Administracion o tiene una instancia de Cliente
    if request.user.groups.filter(name='Administracion').exists() or Cliente.objects.filter(user=request.user).exists():
        if request.method == 'POST':
            form = TicketsForm(request.POST, instance=Ticket(cliente=request.user))
            if form.is_valid():
                # Configurar el estado 'Nuevo' antes de guardar el ticket
                form.instance.estado = Estado.objects.get(pk=1)
                form.instance.num_respuestas = 0
                form.save()
                print("Ticket creado exitosamente")
                return redirect('adm_tickets')  # Redirige a la página de éxito
            else:
                print("Formulario no válido. Errores:", form.errors)
        else:
            form = TicketsForm()

        return render(request, 'administracion/crear_tickets.html', {'form': form})
    else:
        return HttpResponseForbidden("No tienes permisos para acceder a esta página.")

def asignar_tecnico(request, ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)

    if request.method == 'POST':
        form = AsignarTecnicoForm(request.POST, instance=ticket)
        if form.is_valid():
            form.instance.estado = Estado.objects.get(pk=2)
            form.save()
            return redirect('adm_tickets')  # Redirige a la página de éxito
    else:
        form = AsignarTecnicoForm(instance=ticket)

    return render(request, 'administracion/asignar_tecnico.html', {'form': form, 'ticket': ticket})

def agregar_respuesta(request, ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)

    if request.method == 'POST':
        form = RespuestaForm(request.POST)
        if form.is_valid():
            respuesta = form.save(commit=False)
            respuesta.ticket = ticket
            respuesta.tecnico = request.user  # Asigna al usuario actual como técnico
            respuesta.save()

            ticket.num_respuestas += 1
            ticket.save()

            messages.success(request, 'Respuesta agregada con éxito.')
            return redirect('adm_tickets')
    else:
        form = RespuestaForm()

    return render(request, 'administracion/agregar_respuesta.html', {'form': form, 'ticket': ticket})

def detalle_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    respuestas = Respuesta.objects.filter(ticket=ticket).order_by('fecha_respuesta')

    return render(request, 'administracion/detalle_ticket.html', {'ticket': ticket, 'respuestas': respuestas})

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adm_clientes')  # Redirige a la página de éxito
    else:
        form = ClienteForm()
    return render(request, 'administracion/crear_cliente.html', {'form': form})

def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    if request.method == 'POST':
        cliente.user.delete()  # Eliminar el usuario asociado al cliente
        cliente.delete()  # Eliminar el cliente
    return redirect('adm_clientes')  # Redirigir a la página deseada después de eliminar el cliente

def eliminar_tecnico(request, tecnico_id):
    tecnico = get_object_or_404(Tecnico, pk=tecnico_id)
    if request.method == 'POST':
        tecnico.user.delete()  # Eliminar el usuario asociado al cliente
        tecnico.delete()  # Eliminar el cliente
    return redirect('adm_equipo')  # Redirigir a la página deseada después de eliminar el cliente

def crear_tecnico(request):
    if request.method == 'POST':
        form = TecnicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adm_equipo')  # Redirige a la página de éxito
    else:
        form = TecnicoForm()
    return render(request, 'administracion/crear_tecnico.html', {'form': form})

def adm_profile(request):
    administrador = request.user

    print(administrador)

    return render(request, 'administracion/profile.html', {'administrador':administrador})


##SECCION DE CLIENTES
def cli_dashboard(request):
    return redirect('cli_ticket')

def cli_profile(request):
    cliente = request.user

    print(cliente)

    return render(request, 'cliente/profile.html', {'cliente':cliente})

def cli_ticket(request):
    # Obtener el cliente asociado al usuario logueado
    cliente = Cliente.objects.get(user=request.user)

    # Filtrar los tickets del cliente
    tickets_cliente = Ticket.objects.filter(cliente=request.user)

    return render(request, 'cliente/tickets.html', {'tickets_cliente': tickets_cliente, 'cliente': cliente})

def cli_crear_ticket(request):
    if request.method == 'POST':
        form = TicketsForm(request.POST, request.FILES, instance=Ticket(cliente=request.user))
        if form.is_valid():
            # Configurar el estado 'Nuevo' antes de guardar el ticket
            form.instance.estado = Estado.objects.get(pk=1)
            form.instance.num_respuestas = 0
            form.save()
            print("Ticket creado exitosamente")
            return redirect('cli_ticket')  # Redirige a la página de éxito
        else:
            print("Formulario no válido. Errores:", form.errors)
    else:
        form = TicketsForm()

    return render(request, 'cliente/crear_tickets.html', {'form': form})
    
def cli_agregar_respuesta(request, ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)

    if request.method == 'POST':
        form = RespuestaForm(request.POST)
        if form.is_valid():
            respuesta = form.save(commit=False)
            respuesta.ticket = ticket
            respuesta.tecnico = request.user  # Asigna al usuario actual como técnico
            respuesta.save()

            ticket.num_respuestas += 1
            ticket.save()

            messages.success(request, 'Respuesta agregada con éxito.')
            return redirect('cli_ticket')
    else:
        form = RespuestaForm()

    return render(request, 'cliente/agregar_respuesta.html', {'form': form, 'ticket': ticket})

def cli_detalle_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    respuestas = Respuesta.objects.filter(ticket=ticket).order_by('fecha_respuesta')

    
    # Pasa los archivos adjuntos al contexto
    adjuntos = [ticket.adjunto1, ticket.adjunto2]

    return render(request, 'cliente/detalle_ticket.html', {'ticket': ticket, 'respuestas': respuestas, 'adjuntos': adjuntos})



##SECCION DE TECNICOS
def tec_dashboard(request):
    return redirect('tec_ticket')

def tec_ticket(request):
    # Obtener el técnico asociado al usuario logueado
    tecnico = Tecnico.objects.get(user=request.user)

    # Filtrar los tickets asignados al técnico
    tickets_tecnico = Ticket.objects.filter(tecnico_asig=tecnico)

    return render(request, 'tecnico/tickets.html', {'tickets_tecnico': tickets_tecnico, 'tecnico': tecnico})

def tec_profile(request):
    tecnico = request.user

    print(tecnico)

    return render(request, 'tecnico/profile.html', {'tecnico':tecnico})

def tec_detalle_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    respuestas = Respuesta.objects.filter(ticket=ticket).order_by('fecha_respuesta')

    return render(request, 'tecnico/detalle_ticket.html', {'ticket': ticket, 'respuestas': respuestas})

def tec_agregar_respuesta(request, ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)

    if request.method == 'POST':
        form = RespuestaForm(request.POST)
        if form.is_valid():
            respuesta = form.save(commit=False)
            respuesta.ticket = ticket
            respuesta.tecnico = request.user  # Asigna al usuario actual como técnico
            respuesta.save()

            ticket.num_respuestas += 1
            ticket.save()

            messages.success(request, 'Respuesta agregada con éxito.')
            return redirect('tec_ticket')
    else:
        form = RespuestaForm()

    return render(request, 'tecnico/agregar_respuesta.html', {'form': form, 'ticket': ticket})
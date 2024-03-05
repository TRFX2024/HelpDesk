import random
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.utils import timezone

from django import forms
from .models import Cliente, Estado, Respuesta, Tecnico, Ticket
from django.contrib.auth.models import User, Group

def generar_username(nombre, apellido):
    # Obtener las dos primeras letras del nombre y del apellido
    letras_nombre = nombre[:2].lower()
    letras_apellido = apellido[:2].lower()
    # Generar un número aleatorio entre 0 y 9999
    numero_aleatorio = random.randint(0, 9999)
    # Combinar las letras y el número para formar el username
    username = f"{letras_nombre}{letras_apellido}{numero_aleatorio}"
    return username

from django import forms
from django.contrib.auth.models import User, Group
from .models import Cliente
from django.contrib.auth.hashers import make_password

class ClienteForm(forms.ModelForm):
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)
    comuna = forms.CharField(max_length=255)
    contraseña = forms.CharField(max_length=128, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        apellido = cleaned_data.get('apellido')
        comuna = cleaned_data.get('comuna')
        contraseña = cleaned_data.get('contraseña')
        # Generar username y contraseña aleatorios
        username = generar_username(nombre, apellido)
        # Asignar el grupo 'tecnico' al usuario
        grupo_cliente, creado = Group.objects.get_or_create(name='Cliente')
        cleaned_data['grupo'] = grupo_cliente
        cleaned_data['username'] = username
        cleaned_data['password'] = make_password(contraseña)
        return cleaned_data

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['contraseña'],  # Usar la contraseña proporcionada por el usuario
            first_name=self.cleaned_data['nombre'],
            last_name=self.cleaned_data['apellido']
        )
        user.groups.add(self.cleaned_data['grupo'])
        cliente = Cliente.objects.create(
            user=user,
            comuna=self.cleaned_data['comuna']
        )
        return cliente

    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'comuna', 'contraseña']


class TecnicoForm(forms.ModelForm):
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)
    nivel = forms.CharField(max_length=255)
    contraseña = forms.CharField(max_length=128, widget=forms.PasswordInput())


    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        apellido = cleaned_data.get('apellido')
        nivel = cleaned_data.get('nivel')
        contraseña = cleaned_data.get('contraseña')
        # Generar username y contraseña aleatorios
        username = generar_username(nombre, apellido)
        # Asignar el grupo 'tecnico' al usuario
        grupo_tecnico, creado = Group.objects.get_or_create(name='Tecnico')
        cleaned_data['grupo'] = grupo_tecnico
        cleaned_data['username'] = username
        cleaned_data['password'] = make_password(contraseña)
        return cleaned_data

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['contraseña'],  # Usar la contraseña proporcionada por el usuario
            first_name=self.cleaned_data['nombre'],
            last_name=self.cleaned_data['apellido']
        )
        user.groups.add(self.cleaned_data['grupo'])
        tecnico = Tecnico.objects.create(
            user=user,
            nivel=self.cleaned_data['nivel']
        )
        return tecnico

    class Meta:
        model = Tecnico
        fields = ['nombre', 'apellido', 'nivel', 'contraseña']

class TicketsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configurar valores predeterminados
        self.initial['estado'] = 1  # Configurar el estado "Nuevo" con el ID 1
        self.initial['num_respuestas'] = 0
        self.initial['tecnico_asig'] = None
        self.initial['fecha_solucion'] = None
        self.initial['tiempo_dedicado'] = None

    def clean_asunto(self):
        # Obtener el valor del campo "asunto"
        asunto = self.cleaned_data.get('asunto')
        
        # Convertir el asunto a mayúsculas
        return asunto.upper()
    
    class Meta:
        model = Ticket
        fields = ['asunto', 'descripcion']

        archivo1 = forms.FileField(required=False)
        archivo2 = forms.FileField(required=False)

        widgets = {
            'asunto': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),  # Puedes ajustar el número de filas según tu preferencia
        }

    archivo1 = forms.ImageField(required=False)  # Campo para el primer archivo adjunto
    archivo2 = forms.ImageField(required=False)  # Campo para el segundo archivo adjunto

class AsignarTecnicoForm(forms.ModelForm):
    tecnico_asig = forms.ModelChoiceField(
        queryset=Tecnico.objects.all(),
        empty_label="Seleccionar técnico",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Ticket
        fields = ['tecnico_asig']

class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuesta
        fields = ['respuesta']

        widgets = {
            'respuesta': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),  # Puedes ajustar el número de filas según tu preferencia
        }
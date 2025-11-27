from django.shortcuts import render, redirect, get_object_or_404
from .models import Programa, Asignatura, Profesor, Nivel, Estudiante, Asistencia
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ProgramaForm, AsignaturaForm

def index(request):
    programas = Programa.objects.prefetch_related('asignatura_set').all()

    context = {
        'programas': programas
    }
    return render(request, "index.html", context)

def precios_view(request):
    return render(request, "precios.html")

def taller_view(request):
    return render(request, "taller.html")

def contacto_view(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')
        # Por ahora solo lo retornamos como ejemplo
        print(nombre, email, asunto, mensaje)

    return render(request, "contacto.html")

@login_required
def asistencia(request):
    profesores = Profesor.objects.all()
    asignaturas = Asignatura.objects.select_related('programa').all()
    niveles = Nivel.objects.all()

    if request.method == "POST":
        profesor_id = request.POST.get("select-profesor")
        asignatura_id = request.POST.get("select-asignatura")
        nivel_id = request.POST.get("select-nivel")

        if not (profesor_id and asignatura_id and nivel_id):
            messages.error(request, "Debes seleccionar Profesor, Asignatura y Nivel.")
            return redirect('asistencia')

        try:
            profesor = Profesor.objects.get(id=profesor_id)
            asignatura = Asignatura.objects.get(id=asignatura_id)
            nivel = Nivel.objects.get(id=nivel_id)
        except (Profesor.DoesNotExist, Asignatura.DoesNotExist, Nivel.DoesNotExist):
            messages.error(request, "Profesor, Asignatura o Nivel no válido.")
            return redirect('asistencia')

        # Esperamos recibir los estados de asistencia como:
        # 'estudiante_1': 'P' / 'A' / 'J'
        for key, estado in request.POST.items():
            if key.startswith("estudiante_"):
                estudiante_id = key.split("_")[1]
                try:
                    estudiante = Estudiante.objects.get(id=estudiante_id)
                except Estudiante.DoesNotExist:
                    continue

                presente = estado == "P"
                ausente = estado == "A"
                justificado = estado == "J"

                # Guardamos la asistencia, si ya existía, la actualizamos
                asistencia_obj, created = Asistencia.objects.update_or_create(
                    estudiante=estudiante,
                    fecha=timezone.now().date(),
                    asignatura=asignatura,
                    defaults={
                        "nivel": nivel,
                        "profesor": profesor,
                        "presente": presente,
                        "ausente": ausente,
                        "justificado": justificado,
                    }
                )

        messages.success(request, "Asistencia registrada correctamente.")
        return redirect('asistencia')

    # Si GET, mostramos los select con datos de la base
    estudiantes = Estudiante.objects.all()
    context = {
        "profesores": profesores,
        "asignaturas": asignaturas,
        "niveles": niveles,
        "estudiantes": estudiantes,
    }
    return render(request, "asistencia.html", context)

def login_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Bienvenido {user.username}')
            return redirect('index')
        else:
            messages.error(request, 'Credenciales inválidas')
    return render(request, 'login.html')

@login_required
def logout_usuario(request):
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente.')
    return render(request, 'logout.html')
# -------------------------------
# Programas
# -------------------------------
@login_required
def programa_list(request):
    programas = Programa.objects.all()
    return render(request, 'crud/programa_list.html', {'programas': programas})

@login_required
def programa_create(request):
    if request.method == 'POST':
        form = ProgramaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Programa creado correctamente.")
            return redirect('programa_list')
    else:
        form = ProgramaForm()
    return render(request, 'crud/programa_form.html', {'form': form, 'titulo': 'Crear Programa'})

@login_required
def programa_edit(request, pk):
    programa = get_object_or_404(Programa, pk=pk)
    if request.method == 'POST':
        form = ProgramaForm(request.POST, instance=programa)
        if form.is_valid():
            form.save()
            messages.success(request, "Programa actualizado correctamente.")
            return redirect('programa_list')
    else:
        form = ProgramaForm(instance=programa)
    return render(request, 'crud/programa_form.html', {'form': form, 'titulo': 'Editar Programa'})

@login_required
def programa_delete(request, pk):
    programa = get_object_or_404(Programa, pk=pk)
    if request.method == 'POST':
        programa.delete()
        messages.success(request, "Programa eliminado correctamente.")
        return redirect('programa_list')
    return render(request, 'crud/programa_confirm_delete.html', {'programa': programa})

# -------------------------------
# Asignaturas
# -------------------------------
@login_required
def asignatura_list(request):
    asignaturas = Asignatura.objects.select_related('programa').all()
    return render(request, 'crud/asignatura_list.html', {'asignaturas': asignaturas})

@login_required
def asignatura_create(request):
    if request.method == 'POST':
        form = AsignaturaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Asignatura creada correctamente.")
            return redirect('asignatura_list')
    else:
        form = AsignaturaForm()
    return render(request, 'crud/asignatura_form.html', {'form': form, 'titulo': 'Crear Asignatura'})

@login_required
def asignatura_edit(request, pk):
    asignatura = get_object_or_404(Asignatura, pk=pk)
    if request.method == 'POST':
        form = AsignaturaForm(request.POST, instance=asignatura)
        if form.is_valid():
            form.save()
            messages.success(request, "Asignatura actualizada correctamente.")
            return redirect('asignatura_list')
    else:
        form = AsignaturaForm(instance=asignatura)
    return render(request, 'crud/asignatura_form.html', {'form': form, 'titulo': 'Editar Asignatura'})

@login_required
def asignatura_delete(request, pk):
    asignatura = get_object_or_404(Asignatura, pk=pk)
    if request.method == 'POST':
        asignatura.delete()
        messages.success(request, "Asignatura eliminada correctamente.")
        return redirect('asignatura_list')
    return render(request, 'crud/asignatura_confirm_delete.html', {'asignatura': asignatura})
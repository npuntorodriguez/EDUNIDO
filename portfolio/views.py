from django.shortcuts import render, redirect
from .models import Programa, Asignatura
from django.contrib import messages
from .models import Profesor, Asignatura, Nivel, Estudiante, Asistencia
from django.utils import timezone

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

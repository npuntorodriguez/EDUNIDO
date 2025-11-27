from django.contrib import admin
from .models import Estudiante, Nivel, Asistencia, Profesor, Asignatura, Programa


# --- Modelos de Asistencia ---

# 1. Registrar Estudiante
@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    # CRÍTICO: Aseguramos que se pueda gestionar la relación ManyToMany a Programas
    filter_horizontal = ('programas',) 
    
    list_display = ('nombre', 'apellido', 'email', 'nivel') # Incluimos el Nivel
    search_fields = ('nombre', 'apellido', 'email')
    list_filter = ('nivel', 'programas')
    
# 2. Registrar NIVEL (Antiguo Curso)
@admin.register(Nivel)
class NivelAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

# 3. Registrar PROGRAMA (¡NUEVO MODELO DE AGRUPACIÓN!)
@admin.register(Programa)
class ProgramaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    
# 4. Registrar Asignatura (Incluye relación a Programa)
@admin.register(Asignatura)
class AsignaturaAdmin(admin.ModelAdmin):
    # CRÍTICO: Mostramos a qué programa pertenece cada asignatura
    list_display = ('nombre', 'programa')
    search_fields = ('nombre',)
    list_filter = ('programa',) # Permitimos filtrar por la agrupación
    
# 5. Registrar Profesor
@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido',)
    search_fields = ('nombre', 'apellido',)

# 6. Registrar Asistencia 
@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    # CRÍTICO: Usamos 'nivel' en lugar de 'curso'
    list_display = ('estudiante', 'nivel', 'profesor', 'asignatura', 'fecha', 'presente', 'ausente', 'justificado')
    # CRÍTICO: Usamos 'nivel' en lugar de 'curso'
    list_filter = ('nivel', 'profesor', 'asignatura', 'fecha', 'presente')
    search_fields = ('estudiante__nombre', 'estudiante__apellido', 'nivel__nombre')
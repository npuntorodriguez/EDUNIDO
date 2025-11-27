from django.db import models

# =========================================================
# --- 1. Modelos de Estructura Educativa ---
# =========================================================

class Nivel(models.Model):
    """Representa el Nivel o Curso académico (Ej: 3° Básico, 5° Básico)."""
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Programa(models.Model):
    """Representa la Agrupación de Asignaturas o Currículum (Ej: Programa en Español, Talleres)."""
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Asignatura(models.Model):
    """Representa una asignatura específica que pertenece a un solo Programa."""
    nombre = models.CharField(max_length=100)
    
    programa = models.ForeignKey(
        Programa, 
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        default=1
    )

    def __str__(self):
        return f"{self.nombre} ({self.programa.nombre if self.programa else 'Sin Programa'})"

class Profesor(models.Model):
    """Representa a los profesores."""
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# =========================================================
# --- 2. Modelo Principal (Estudiante) ---
# =========================================================

class Estudiante(models.Model):
    """Representa un estudiante, relacionado con Nivel y Múltiples Programas."""
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    
    # Un estudiante pertenece a un solo Nivel
    nivel = models.ForeignKey(Nivel, on_delete=models.PROTECT)
    
    # Un estudiante puede tomar varias Agrupaciones de Asignaturas (Programas)
    programas = models.ManyToManyField(Programa) 

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# =========================================================
# --- 3. Modelo de Registro (Asistencia) ---
# =========================================================

class Asistencia(models.Model):
    """Registro de la asistencia de un estudiante a una asignatura en un Nivel específico."""
    
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    
    fecha = models.DateField(auto_now_add=True)
    presente = models.BooleanField(default=False)
    ausente = models.BooleanField(default=False)
    justificado = models.BooleanField(default=False)

    class Meta:
        unique_together = ('estudiante', 'fecha', 'asignatura')

    def __str__(self):
        estado = "P" if self.presente else "A" if self.ausente else "J"
        return f"{self.estudiante.nombre} - {self.asignatura.nombre} ({self.fecha}) [{estado}]"
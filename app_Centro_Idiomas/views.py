from django.shortcuts import render, redirect, get_object_or_404
from .models import Idioma, Profesor, Clase # Importa todos los modelos

def inicio_centro_idiomas(request):
    return render(request, 'inicio.html')

def agregar_idioma(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        nivel = request.POST.get('nivel')
        region = request.POST.get('region')
        descripcion = request.POST.get('descripcion')
        codigo = request.POST.get('codigo')
        # bandera_img = request.FILES.get('bandera_img') # Para manejar imágenes, se necesita configurar MEDIA_ROOT y MEDIA_URL en settings.py

        idioma = Idioma(
            nombre=nombre,
            nivel=nivel,
            region=region,
            descripcion=descripcion,
            codigo=codigo,
            # bandera_img=bandera_img
        )
        idioma.save()
        return redirect('ver_idiomas')
    return render(request, 'idioma/agregar_idioma.html')

def ver_idiomas(request):
    idiomas = Idioma.objects.all()
    return render(request, 'idioma/ver_idiomas.html', {'idiomas': idiomas})

def actualizar_idioma(request, id_idioma):
    idioma = get_object_or_404(Idioma, pk=id_idioma)
    if request.method == 'POST':
        idioma.nombre = request.POST.get('nombre')
        idioma.nivel = request.POST.get('nivel')
        idioma.region = request.POST.get('region')
        idioma.descripcion = request.POST.get('descripcion')
        idioma.codigo = request.POST.get('codigo')
        # if 'bandera_img' in request.FILES:
        #    idioma.bandera_img = request.FILES['bandera_img']
        idioma.save()
        return redirect('ver_idiomas')
    return render(request, 'idioma/actualizar_idioma.html', {'idioma': idioma})

def borrar_idioma(request, id_idioma):
    idioma = get_object_or_404(Idioma, pk=id_idioma)
    if request.method == 'POST':
        idioma.delete()
        return redirect('ver_idiomas')
    return render(request, 'idioma/borrar_idioma.html', {'idioma': idioma})

def agregar_profesor(request):
    idiomas = Idioma.objects.all() # Obtener todos los idiomas para el select
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        ap_paterno = request.POST.get('ap_paterno')
        ap_materno = request.POST.get('ap_materno')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        id_idioma_id = request.POST.get('id_idioma') # Obtener el ID del idioma seleccionado

        idioma_obj = get_object_or_404(Idioma, pk=id_idioma_id) # Obtener el objeto Idioma
        
        Profesor.objects.create(
            nombre=nombre,
            ap_paterno=ap_paterno,
            ap_materno=ap_materno,
            telefono=telefono,
            correo=correo,
            id_idioma=idioma_obj
        )
        return redirect('ver_profesores') # Redirigir a la lista de profesores
    return render(request, 'profesores/agregar_profesor.html', {'idiomas': idiomas})

# Función para ver todos los profesores
def ver_profesores(request):
    profesores = Profesor.objects.all()
    return render(request, 'profesores/ver_profesores.html', {'profesores': profesores})

# Función para editar un profesor (muestra el formulario con datos actuales)
def actualizar_profesor(request, pk):
    profesor = get_object_or_404(Profesor, pk=pk)
    idiomas = Idioma.objects.all()
    return render(request, 'profesores/actualizar_profesor.html', {'profesor': profesor, 'idiomas': idiomas})

# Función para realizar la actualización del profesor
def realizar_actualizacion_profesor(request, pk):
    if request.method == 'POST':
        profesor = get_object_or_404(Profesor, pk=pk)
        profesor.nombre = request.POST.get('nombre')
        profesor.ap_paterno = request.POST.get('ap_paterno')
        profesor.ap_materno = request.POST.get('ap_materno')
        profesor.telefono = request.POST.get('telefono')
        profesor.correo = request.POST.get('correo')
        
        id_idioma_id = request.POST.get('id_idioma')
        idioma_obj = get_object_or_404(Idioma, pk=id_idioma_id)
        profesor.id_idioma = idioma_obj
        
        profesor.save()
        return redirect('ver_profesores')
    return redirect('ver_profesores') # En caso de que se acceda por GET, redirigir

# Función para borrar un profesor
def borrar_profesor(request, pk):
    profesor = get_object_or_404(Profesor, pk=pk)
    if request.method == 'POST':
        profesor.delete()
        return redirect('ver_profesores')
    return render(request, 'profesores/borrar_profesor.html', {'profesor': profesor})

def agregar_clase(request):
    profesores = Profesor.objects.all()
    idiomas = Idioma.objects.all()

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        capacidad = request.POST.get('capacidad')
        nivel = request.POST.get('nivel')
        id_profesor_id = request.POST.get('id_profesor')
        idioma_id = request.POST.get('idioma')

        # Convertir id_profesor e idioma a sus objetos correspondientes
        profesor_obj = get_object_or_404(Profesor, pk=id_profesor_id)
        idioma_obj = get_object_or_404(Idioma, pk=idioma_id)

        Clase.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            capacidad=capacidad,
            nivel=nivel,
            id_profesor=profesor_obj,
            idioma=idioma_obj
        )
        return redirect('ver_clases')
    return render(request, 'clases/agregar_clase.html', {'profesores': profesores, 'idiomas': idiomas})

# Función para ver todas las clases
def ver_clases(request):
    clases = Clase.objects.all()
    return render(request, 'clases/ver_clases.html', {'clases': clases})

# Función para actualizar una clase (muestra el formulario con datos actuales)
def actualizar_clase(request, pk):
    clase = get_object_or_404(Clase, pk=pk)
    profesores = Profesor.objects.all()
    idiomas = Idioma.objects.all()
    return render(request, 'clases/actualizar_clase.html', {'clase': clase, 'profesores': profesores, 'idiomas': idiomas})

# Función para realizar la actualización (maneja el POST del formulario)
def realizar_actualizacion_clase(request, pk):
    clase = get_object_or_404(Clase, pk=pk)
    if request.method == 'POST':
        clase.nombre = request.POST.get('nombre')
        clase.descripcion = request.POST.get('descripcion')
        clase.capacidad = request.POST.get('capacidad')
        clase.nivel = request.POST.get('nivel')

        id_profesor_id = request.POST.get('id_profesor')
        idioma_id = request.POST.get('idioma')

        clase.id_profesor = get_object_or_404(Profesor, pk=id_profesor_id)
        clase.idioma = get_object_or_404(Idioma, pk=idioma_id)
        clase.save()
        return redirect('ver_clases')
    return redirect('actualizar_clase', pk=pk) # Redirige al formulario si no es POST

# Función para borrar una clase
def borrar_clase(request, pk):
    clase = get_object_or_404(Clase, pk=pk)
    if request.method == 'POST':
        clase.delete()
        return redirect('ver_clases')
    return render(request, 'clases/borrar_clase.html', {'clase': clase})
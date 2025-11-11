¡Excelente! Continuemos con la tercera parte del proyecto. Aquí tienes la estructura de carpetas y archivos actualizada, así como el código necesario para implementar la gestión de clases en tu Centro de Idiomas.

Estructura de Carpetas y Archivos Actualizada

    UIII_Centro_de_Idiomas_0498/
    ├── backend_Idiomas/
    │   ├── backend_Idiomas/
    │   │   ├── __init__.py
    │   │   ├── asgi.py
    │   │   ├── settings.py
    │   │   ├── urls.py
    │   │   └── wsgi.py
    │   ├── app_Idiomas/
    │   │   ├── migrations/
    │   │   │   └── __init__.py
    │   │   ├── templates/
    │   │   │   ├── base.html
    │   │   │   ├── navbar.html
    │   │   │   └── clases/
    │   │   │       ├── agregar_clase.html
    │   │   │       ├── ver_clases.html
    │   │   │       ├── actualizar_clase.html
    │   │   │       └── borrar_clase.html
    │   │   ├── __init__.py
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── models.py
    │   │   ├── tests.py
    │   │   └── views.py
    └── └── manage.py
1. Modelo Clase (Ya proporcionado)

        from django.db import models
        
        # Asegúrate de que los modelos Profesor e Idioma estén definidos o importados
        # Por ejemplo, si están en el mismo archivo:
        class Profesor(models.Model):
            nombre = models.CharField(max_length=150)
            apellido = models.CharField(max_length=150)
            email = models.EmailField(unique=True)
            telefono = models.CharField(max_length=20, blank=True, null=True)
            especialidad = models.CharField(max_length=100, blank=True, null=True)
        
            def __str__(self):
                return f"{self.nombre} {self.apellido}"
        
        class Idioma(models.Model):
            nombre = models.CharField(max_length=100, unique=True)
            codigo = models.CharField(max_length=10, unique=True)
            descripcion = models.TextField(blank=True, null=True)
        
            def __str__(self):
                return self.nombre
        
        
        # ==========================================
        # MODELO: CLASE
        # ==========================================
        class Clase(models.Model):
            nombre = models.CharField(max_length=150)
            descripcion = models.TextField(blank=True, null=True)
            capacidad = models.PositiveIntegerField()
            nivel = models.CharField(max_length=50,
            choices=[ ('Básico A1', 'Básico A1'), ('Básico A2', 'Básico A2'),
                      ('Intermedio B1', 'Intermedio B1'), ('Intermedio B2', 'Intermedio B2'),
                      ('Avanzado C1', 'Avanzado C1'), ('Avanzado C2', 'Avanzado C2') ])
            id_profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name="clases")
            idioma = models.ForeignKey(Idioma, on_delete=models.CASCADE, related_name="clases_idioma")
        
            def __str__(self):
                return f"{self.nombre} ({self.idioma.nombre})"
2. Procedimiento para realizar las migraciones

Abre tu terminal en la raíz del proyecto UIII_Centro_de_Idiomas_0498 y ejecuta los siguientes comandos:

    python manage.py makemigrations app_Idiomas
    python manage.py migrate
3. Ahora trabajamos con el MODELO: Clase
4. En views.py de app_Idiomas crear las funciones

        from django.shortcuts import render, redirect, get_object_or_404
        from .models import Clase, Profesor, Idioma # Asegúrate de importar todos los modelos necesarios
        
        # Función para agregar una clase
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
5. y 6. Modificar navbar.html y crear subcarpeta clases

navbar.html (dentro de app_Idiomas/templates/)

    <nav class="navbar navbar-expand-lg navbar-dark" style="background-color: #6a1b9a;">
        <div class="container-fluid">
            <a class="navbar-brand" href="{% url 'home' %}">Centro de Idiomas</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavDropdown">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="{% url 'home' %}">Inicio</a>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="navbarProfesoresDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            Profesores
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="navbarProfesoresDropdown" style="background-color: #9c27b0;">
                            <li><a class="dropdown-item text-white" href="{% url 'agregar_profesor' %}">Agregar Profesor</a></li>
                            <li><a class="dropdown-item text-white" href="{% url 'ver_profesores' %}">Ver Profesores</a></li>
                        </ul>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="navbarIdiomasDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            Idiomas
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="navbarIdiomasDropdown" style="background-color: #9c27b0;">
                            <li><a class="dropdown-item text-white" href="{% url 'agregar_idioma' %}">Agregar Idioma</a></li>
                            <li><a class="dropdown-item text-white" href="{% url 'ver_idiomas' %}">Ver Idiomas</a></li>
                        </ul>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="navbarClasesDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            Clases
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="navbarClasesDropdown" style="background-color: #9c27b0;">
                            <li><a class="dropdown-item text-white" href="{% url 'agregar_clase' %}">Agregar Clase</a></li>
                            <li><a class="dropdown-item text-white" href="{% url 'ver_clases' %}">Ver Clases</a></li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

Crear la subcarpeta clases:
Dentro de app_Idiomas/templates/ crea una nueva carpeta llamada clases.

7. Crear los archivos HTML con sus códigos correspondientes

agregar_clase.html (dentro de app_Idiomas/templates/clases/)

agregar_clase.html

    {% extends 'base.html' %}
    
    {% block title %}Agregar Clase{% endblock %}
    
    {% block content %}
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card shadow-lg" style="border-radius: 15px; border: none;">
                    <div class="card-header text-white text-center" style="background-color: #8e24aa; border-top-left-radius: 15px; border-top-right-radius: 15px;">
                        <h2 class="mb-0">Agregar Nueva Clase</h2>
                    </div>
                    <div class="card-body p-4" style="background-color: #f3e5f5;">
                        <form method="post">
                            {% csrf_token %}
                            <div class="mb-3">
                                <label for="nombre" class="form-label text-purple-dark">Nombre de la Clase:</label>
                                <input type="text" class="form-control" id="nombre" name="nombre" required style="border-radius: 8px; border-color: #ce93d8;">
                            </div>
                            <div class="mb-3">
                                <label for="descripcion" class="form-label text-purple-dark">Descripción:</label>
                                <textarea class="form-control" id="descripcion" name="descripcion" rows="3" style="border-radius: 8px; border-color: #ce93d8;"></textarea>
                            </div>
                            <div class="mb-3">
                                <label for="capacidad" class="form-label text-purple-dark">Capacidad:</label>
                                <input type="number" class="form-control" id="capacidad" name="capacidad" required style="border-radius: 8px; border-color: #ce93d8;">
                            </div>
                            <div class="mb-3">
                                <label for="nivel" class="form-label text-purple-dark">Nivel:</label>
                                <select class="form-select" id="nivel" name="nivel" required style="border-radius: 8px; border-color: #ce93d8;">
                                    <option value="Básico A1">Básico A1</option>
                                    <option value="Básico A2">Básico A2</option>
                                    <option value="Intermedio B1">Intermedio B1</option>
                                    <option value="Intermedio B2">Intermedio B2</option>
                                    <option value="Avanzado C1">Avanzado C1</option>
                                    <option value="Avanzado C2">Avanzado C2</option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <label for="id_profesor" class="form-label text-purple-dark">Profesor:</label>
                                <select class="form-select" id="id_profesor" name="id_profesor" required style="border-radius: 8px; border-color: #ce93d8;">
                                    {% for profesor in profesores %}
                                        <option value="{{ profesor.pk }}">{{ profesor.nombre }} {{ profesor.apellido }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                            <div class="mb-3">
                                <label for="idioma" class="form-label text-purple-dark">Idioma:</label>
                                <select class="form-select" id="idioma" name="idioma" required style="border-radius: 8px; border-color: #ce93d8;">
                                    {% for idioma in idiomas %}
                                        <option value="{{ idioma.pk }}">{{ idioma.nombre }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                            <div class="d-grid gap-2">
                                <button type="submit" class="btn text-white" style="background-color: #ab47bc; border-radius: 8px;">Agregar Clase</button>
                                <a href="{% url 'ver_clases' %}" class="btn btn-outline-secondary" style="border-radius: 8px;">Cancelar</a>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    {% endblock %}

ver_clases.html

    {% extends 'base.html' %}
    
    {% block title %}Ver Clases{% endblock %}
    
    {% block content %}
    <div class="container mt-5">
        <h2 class="text-center mb-4" style="color: #6a1b9a;">Lista de Clases</h2>
        <div class="table-responsive">
            <table class="table table-hover table-striped shadow-sm" style="border-radius: 10px; overflow: hidden; background-color: #f3e5f5;">
                <thead class="text-white" style="background-color: #8e24aa;">
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Nombre</th>
                        <th scope="col">Descripción</th>
                        <th scope="col">Capacidad</th>
                        <th scope="col">Nivel</th>
                        <th scope="col">Profesor</th>
                        <th scope="col">Idioma</th>
                        <th scope="col">Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {% for clase in clases %}
                    <tr>
                        <th scope="row">{{ forloop.counter }}</th>
                        <td>{{ clase.nombre }}</td>
                        <td>{{ clase.descripcion|default:"N/A" }}</td>
                        <td>{{ clase.capacidad }}</td>
                        <td>{{ clase.nivel }}</td>
                        <td>{{ clase.id_profesor.nombre }} {{ clase.id_profesor.apellido }}</td>
                        <td>{{ clase.idioma.nombre }}</td>
                        <td>
                            <a href="{% url 'actualizar_clase' clase.pk %}" class="btn btn-sm btn-info text-white me-2" style="background-color: #ab47bc; border: none;">Editar</a>
                            <a href="{% url 'borrar_clase' clase.pk %}" class="btn btn-sm btn-danger" style="background-color: #e57373; border: none;">Borrar</a>
                        </td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="8" class="text-center p-4">No hay clases disponibles. <a href="{% url 'agregar_clase' %}" style="color: #6a1b9a;">¡Agrega una ahora!</a></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        <div class="text-center mt-4">
            <a href="{% url 'agregar_clase' %}" class="btn text-white" style="background-color: #6a1b9a; border-radius: 8px;">Agregar Nueva Clase</a>
        </div>
    </div>
    {% endblock %}

actualizar_clase.html

    {% extends 'base.html' %}
    
    {% block title %}Actualizar Clase{% endblock %}
    
    {% block content %}
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card shadow-lg" style="border-radius: 15px; border: none;">
                    <div class="card-header text-white text-center" style="background-color: #8e24aa; border-top-left-radius: 15px; border-top-right-radius: 15px;">
                        <h2 class="mb-0">Actualizar Clase: {{ clase.nombre }}</h2>
                    </div>
                    <div class="card-body p-4" style="background-color: #f3e5f5;">
                        <form method="post" action="{% url 'realizar_actualizacion_clase' clase.pk %}">
                            {% csrf_token %}
                            <div class="mb-3">
                                <label for="nombre" class="form-label text-purple-dark">Nombre de la Clase:</label>
                                <input type="text" class="form-control" id="nombre" name="nombre" value="{{ clase.nombre }}" required style="border-radius: 8px; border-color: #ce93d8;">
                            </div>
                            <div class="mb-3">
                                <label for="descripcion" class="form-label text-purple-dark">Descripción:</label>
                                <textarea class="form-control" id="descripcion" name="descripcion" rows="3" style="border-radius: 8px; border-color: #ce93d8;">{{ clase.descripcion|default_if_none:"" }}</textarea>
                            </div>
                            <div class="mb-3">
                                <label for="capacidad" class="form-label text-purple-dark">Capacidad:</label>
                                <input type="number" class="form-control" id="capacidad" name="capacidad" value="{{ clase.capacidad }}" required style="border-radius: 8px; border-color: #ce93d8;">
                            </div>
                            <div class="mb-3">
                                <label for="nivel" class="form-label text-purple-dark">Nivel:</label>
                                <select class="form-select" id="nivel" name="nivel" required style="border-radius: 8px; border-color: #ce93d8;">
                                    {% for choice in clase.get_nivel_display_choices %} {# Esto es un ejemplo, Django no tiene get_choices para CharField, se usa una lista manual #}
                                    {% with current_choice=choice.0 %}
                                    <option value="{{ current_choice }}" {% if clase.nivel == current_choice %}selected{% endif %}>{{ choice.1 }}</option>
                                    {% endwith %}
                                    {% empty %}
                                    <option value="Básico A1" {% if clase.nivel == 'Básico A1' %}selected{% endif %}>Básico A1</option>
                                    <option value="Básico A2" {% if clase.nivel == 'Básico A2' %}selected{% endif %}>Básico A2</option>
                                    <option value="Intermedio B1" {% if clase.nivel == 'Intermedio B1' %}selected{% endif %}>Intermedio B1</option>
                                    <option value="Intermedio B2" {% if clase.nivel == 'Intermedio B2' %}selected{% endif %}>Intermedio B2</option>
                                    <option value="Avanzado C1" {% if clase.nivel == 'Avanzado C1' %}selected{% endif %}>Avanzado C1</option>
                                    <option value="Avanzado C2" {% if clase.nivel == 'Avanzado C2' %}selected{% endif %}>Avanzado C2</option>
                                    {% endfor %}
                                </select>
                            </div>
                            <div class="mb-3">
                                <label for="id_profesor" class="form-label text-purple-dark">Profesor:</label>
                                <select class="form-select" id="id_profesor" name="id_profesor" required style="border-radius: 8px; border-color: #ce93d8;">
                                    {% for profesor in profesores %}
                                        <option value="{{ profesor.pk }}" {% if clase.id_profesor.pk == profesor.pk %}selected{% endif %}>{{ profesor.nombre }} {{ profesor.apellido }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                            <div class="mb-3">
                                <label for="idioma" class="form-label text-purple-dark">Idioma:</label>
                                <select class="form-select" id="idioma" name="idioma" required style="border-radius: 8px; border-color: #ce93d8;">
                                    {% for idioma in idiomas %}
                                        <option value="{{ idioma.pk }}" {% if clase.idioma.pk == idioma.pk %}selected{% endif %}>{{ idioma.nombre }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                            <div class="d-grid gap-2">
                                <button type="submit" class="btn text-white" style="background-color: #ab47bc; border-radius: 8px;">Actualizar Clase</button>
                                <a href="{% url 'ver_clases' %}" class="btn btn-outline-secondary" style="border-radius: 8px;">Cancelar</a>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    {% endblock %}

borrar_clase.html 

    {% extends 'base.html' %}
    
    {% block title %}Borrar Clase{% endblock %}
    
    {% block content %}
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card shadow-lg border-danger" style="border-radius: 15px;">
                    <div class="card-header bg-danger text-white text-center" style="border-top-left-radius: 15px; border-top-right-radius: 15px;">
                        <h2 class="mb-0">Confirmar Eliminación de Clase</h2>
                    </div>
                    <div class="card-body p-4" style="background-color: #ffebee;">
                        <p class="lead text-center">¿Estás seguro de que quieres eliminar la clase <strong>"{{ clase.nombre }}"</strong>?</p>
                        <p class="text-center text-danger">¡Esta acción no se puede deshacer!</p>
                        <form method="post">
                            {% csrf_token %}
                            <div class="d-grid gap-2 mt-4">
                                <button type="submit" class="btn btn-danger" style="border-radius: 8px;">Sí, Eliminar Clase</button>
                                <a href="{% url 'ver_clases' %}" class="btn btn-outline-secondary" style="border-radius: 8px;">Cancelar</a>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    {% endblock %}

9. No utilizar forms.py (ya implementado en las vistas directamente con request.POST.get)
10. Procedimiento para agregar en urls.py en app_Idiomas

# UIII_Centro_de_Idiomas_0498/backend_Idiomas/app_Idiomas/urls.py

    from django.urls import path
    from . import views
    
    urlpatterns = [
        path('', views.home, name='home'), # Asegúrate de tener una vista 'home'
        
        # URLs para Profesores
        path('profesores/agregar/', views.agregar_profesor, name='agregar_profesor'),
        path('profesores/', views.ver_profesores, name='ver_profesores'),
        path('profesores/actualizar/<int:pk>/', views.actualizar_profesor, name='actualizar_profesor'),
        path('profesores/actualizar_post/<int:pk>/', views.realizar_actualizacion_profesor, name='realizar_actualizacion_profesor'),
        path('profesores/borrar/<int:pk>/', views.borrar_profesor, name='borrar_profesor'),
    
        # URLs para Idiomas
        path('idiomas/agregar/', views.agregar_idioma, name='agregar_idioma'),
        path('idiomas/', views.ver_idiomas, name='ver_idiomas'),
        path('idiomas/actualizar/<int:pk>/', views.actualizar_idioma, name='actualizar_idioma'),
        path('idiomas/actualizar_post/<int:pk>/', views.realizar_actualizacion_idioma, name='realizar_actualizacion_idioma'),
        path('idiomas/borrar/<int:pk>/', views.borrar_idioma, name='borrar_idioma'),
    
        # URLs para Clases
        path('clases/agregar/', views.agregar_clase, name='agregar_clase'),
        path('clases/', views.ver_clases, name='ver_clases'),
        path('clases/actualizar/<int:pk>/', views.actualizar_clase, name='actualizar_clase'),
        path('clases/actualizar_post/<int:pk>/', views.realizar_actualizacion_clase, name='realizar_actualizacion_clase'),
        path('clases/borrar/<int:pk>/', views.borrar_clase, name='borrar_clase'),
    ]


11. Procedimiento para registrar los modelos en admin.py y volver a realizar las migraciones.

# UIII_Centro_de_Idiomas_0498/backend_Idiomas/app_Idiomas/admin.py

    from django.contrib import admin
    from .models import Profesor, Idioma, Clase
    
    # Registra tus modelos aquí
    admin.site.register(Profesor)
    admin.site.register(Idioma)
    admin.site.register(Clase)

Después de registrar los modelos, si ya habías ejecutado makemigrations y migrate, no es estrictamente necesario volver a hacerlo a menos que hayas realizado cambios en la estructura del modelo. Sin embargo, si quieres estar seguro:

    python manage.py makemigrations app_Idiomas
    python manage.py migrate
12. Trabajando con todos los modelos

Con esto, ya tienes la base para interactuar con los modelos de Profesor, Idioma y Clase a través del administrador de Django y a través de las vistas que has creado. Puedes crear profesores e idiomas primero para luego poder asignarlos a las clases.

13. y 14. Colores suaves, atractivos y modernos, y sin validación de entrada de datos.

Los estilos Bootstrap con los colores pasteles y tonos morados que he añadido en base.html y los templates de clases buscan cumplir con este requisito. La validación de datos no se ha implementado como se solicitó.

15. Proyecto totalmente funcional.

Con todos estos pasos, tu proyecto debería ser funcional para las operaciones CRUD en Clases, Profesores e Idiomas.

16. Finalmente ejecutar servidor en el puerto 8498.

Abre tu terminal en la raíz del proyecto UIII_Centro_de_Idiomas_0498 y ejecuta:

    python manage.py runserver 8498

Luego, abre tu navegador y ve a http://127.0.0.1:8498/. Verás la página de inicio, y desde la barra de navegación podrás acceder a la gestión de Profesores, Idiomas y Clases.

¡Aquí tienes una vista previa de cómo se vería la interfaz de "Ver Clases" con los colores y estilos aplicados!

from django.shortcuts import render, HttpResponse, redirect
from miapp.models import Articulo
from django.db.models import Q
from miapp.forms import FormArticulo
from django.contrib import messages

# Create your views here.

layout= """
<h1> Proyecto Web (LP3 2024) | Flor Cerdán </h1>
<hr/>
<ul>
    <li>
        <a href="/index"> Inicio</a>
    </li>
    <li>
        <a href="/saludo"> Mensaje de Saludo</a>
    </li>
    <li>
        <a href="/rango"> Mostrar Números [a,b]</a>
    </li>
    <li>
        <a href="/rango2/40/30"> Mostrar Números [40,30]</a>
    </li>
</ul>
<hr/>
"""
def saludo(request):
    return render(request, 'saludo.html',{
        'titulo':'Saludo',
        'autor':'Carlos Peña'
    })

def index(request):
    estudiantes = ['Joel Chirinos',
                 'Alberto Cohen',
                 'Jhon Hernandez',
                 'Piero Monsefu']
    return render(request, 'index.html',{
        'titulo':'Iniciooo',
        'mensaje':'Proyecto web con Django',
        'estudiantes': estudiantes})

def rango(request):
    a=10
    b=20
    rango_numeros= range(a,b+1)

    return render(request,'rango.html',{
        'titulo':'Rango',
        'a':a,
        'b':b,
        'rango_numeros':rango_numeros
    })

def rango2(request,a=10,b=15):
    if a>b:
        return redirect('rango2',a=b,b=a)
    
    resultado = f"""
    <h2>Numeros de [{a},{b}]</h2>
    resultado: <br>
    <ul>
    """
    while a<=b:
        resultado += f"<li> {a} </li>"
        a+=1
    resultado += "</ul>"
    return HttpResponse(layout + resultado)

def save_articulo(request):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        if len(titulo)<=5:
            return HttpResponse("<h2>El tamaño del título es pequeño, intente nuevamente</h2>")
        contenido = request.POST['contenido']
        publicado = request.POST['publicado']

        articulo = Articulo(
            titulo = titulo,
            contenido = contenido,
            publicado = publicado
        )
        articulo.save()
        return HttpResponse(f"Articulo Creado: {articulo.titulo} - {articulo.contenido}")
    else:
        return HttpResponse("<h2>No se ha podido registrar el artículo</h2>")

def create_articulo(request):
    return render(request, 'create_articulo.html')

def buscar_articulo(request):
    try:
        articulo = Articulo.objects.get(id=1)
        resultado = f"""Articulo: 
                        <br> <strong>ID:</strong> {articulo.id} 
                        <br> <strong>Título:</strong> {articulo.titulo} 
                        <br> <strong>Contenido:</strong> {articulo.contenido}
                        """
    except:
        resultado = "<h1> Artículo No Encontrado </h1>"
    return HttpResponse(resultado)

def editar_articulo(request, id):
    articulo = Articulo.objects.get(pk=id)


    articulo.titulo = "Enseñanza onLine en la UNTELS"
    articulo.contenido = "Aula Virtual, Google Meet, Portal Académico, Google Classroom..."
    articulo.publicado = False


    articulo.save()
    return HttpResponse(f"Articulo Editado: {articulo.titulo} - {articulo.contenido}")

def listar_articulos(request):
    articulos = Articulo.objects.all()
    """articulos = Articulo.objects.filter(
        Q(titulo__contains="Py") |
        Q(titulo__contains="Hab")
    )"""
    return render(request, 'listar_articulos.html',{
        'articulos':articulos,
        'titulo': 'Listado de Artículos'
    })

def eliminar_articulo(request, id):
    articulo = Articulo.objects.get(pk=id)
    articulo.delete()
    return redirect('listar_articulos')

def create_full_articulo(request):
    if request.method == 'POST':
        formulario = FormArticulo(request.POST)
        if formulario.is_valid():
            data_form = formulario.cleaned_data
            # Hay 2 formas de recuperar la información
            titulo  = data_form.get('titulo')
            contenido = data_form['contenido']
            publicado = data_form['publicado']
            articulo = Articulo(
                titulo = titulo,
                contenido = contenido,
                publicado = publicado
            )
            articulo.save()
            # Crear un mensaje flash (Sesión que solo se muestra 1 vez)
            messages.success(request, f'Se agregó correctamente el artículo {articulo.id}')
            return redirect('listar_articulos')
            #return HttpResponse(articulo.titulo + ' -  ' + articulo.contenido + ' - ' + str(articulo.publicado))
    else:
        formulario = FormArticulo()
        # Generamos un formulario vacío
    return render(request, 'create_full_articulo.html',{
        'form': formulario
    })


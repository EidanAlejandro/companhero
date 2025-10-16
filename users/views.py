from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Usuario, Perfil, EstadoPerfil, Direccion
from organization.models import Departamento, Territorial, JefeCuadrilla
from django.shortcuts import render, redirect, get_object_or_404

@login_required
def welcome_view(request):
    return render(request, 'users/welcome.html', {
        'user': request.user
    })

@login_required
def crear_usuario_simple(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        
        if nombre and apellido and correo:
            try:
                # Obtener estado de perfil por defecto (Activo)
                estado, _ = EstadoPerfil.objects.get_or_create(
                    nombre_estado='Activo'
                )
                
                # Obtener perfil por defecto (Usuario Normal)
                perfil, _ = Perfil.objects.get_or_create(
                    nombre_perfil='Usuario Normal',
                    defaults={
                        'id_estado_perfil': estado,
                        'descripcion': 'Perfil de usuario normal'
                    }
                )
                
                # Crear el usuario
                usuario = Usuario.objects.create(
                    id_perfil=perfil,
                    nombre=nombre,
                    apellido=apellido,
                    correo=correo,
                    telefono=telefono or ''
                )
                
                # Mensaje de éxito
                messages.success(request, 'Usuario creado con éxito', extra_tags='usuario_creado')
                return redirect('crear_usuario_simple')
                
            except Exception as e:
                error = f"Error al crear usuario: {str(e)}"
                return render(request, 'users/crear_usuario_simple.html', {
                    'error': error
                })
    
    return render(request, 'users/crear_usuario_simple.html')

@login_required
def crear_direccion(request):
    # Obtener todos los usuarios para el dropdown
    usuarios = Usuario.objects.all()
    
    if request.method == 'POST':
        nombre_direccion = request.POST.get('nombre_direccion')
        usuario_id = request.POST.get('usuario')
        
        if nombre_direccion and usuario_id:
            try:
                # Crear la dirección
                direccion = Direccion.objects.create(
                    nombre_direccion=nombre_direccion,
                    id_usuario_id=usuario_id
                )
                
                # Mensaje de éxito
                messages.success(request, 'Dirección creada con éxito', extra_tags='direccion_creada')
                return redirect('crear_direccion')
                
            except Exception as e:
                error = f"Error al crear dirección: {str(e)}"
                return render(request, 'users/crear_direccion.html', {
                    'usuarios': usuarios,
                    'error': error
                })
    
    return render(request, 'users/crear_direccion.html', {
        'usuarios': usuarios
    })

#---------------------------------------------------------------------#

@login_required
def listar_usuarios(request):
    # Obtener todos los usuarios con información relacionada
    usuarios = Usuario.objects.select_related('id_perfil').all()
    
    # Crear una lista con la información adicional que necesitamos
    usuarios_con_info = []
    
    for usuario in usuarios:
        # Buscar si el usuario tiene una dirección asignada
        direccion_usuario = Direccion.objects.filter(id_usuario=usuario).first()
        
        # Buscar si el usuario tiene un departamento asignado
        departamento_usuario = Departamento.objects.filter(id_usuario=usuario).first()
        
        usuarios_con_info.append({
            'usuario': usuario,
            'direccion': direccion_usuario.nombre_direccion if direccion_usuario else '',
            'departamento': departamento_usuario.nombre_departamento if departamento_usuario else '',
        })
    
    return render(request, 'users/listar_usuarios.html', {
        'usuarios_con_info': usuarios_con_info
    })


#---------------------------------------------------------------------#

@login_required
def administracion(request):
    direcciones = Direccion.objects.all()
    departamentos = Departamento.objects.all()
    
    if request.method == 'POST':
        # Obtener usuario por defecto
        usuario_default = Usuario.objects.first()
        if not usuario_default:
            # Crear usuario por defecto si no existe
            from .models import Perfil, EstadoPerfil
            estado, _ = EstadoPerfil.objects.get_or_create(nombre_estado='Activo')
            perfil, _ = Perfil.objects.get_or_create(
                nombre_perfil='Usuario Sistema',
                defaults={'id_estado_perfil': estado, 'descripcion': 'Usuario del sistema'}
            )
            usuario_default = Usuario.objects.create(
                id_perfil=perfil,
                nombre='Sistema',
                apellido='Admin',
                correo='sistema@cim.com',
                telefono=''
            )
        
        # Verificar tipo de acción
        accion = request.POST.get('accion')
        
        if accion == 'crear_direccion':
            # Crear nueva dirección
            nombre_direccion = request.POST.get('nombre_direccion', '').strip()
            
            if nombre_direccion:
                nombre_formateado = nombre_direccion.title()
                
                if Direccion.objects.filter(nombre_direccion__iexact=nombre_formateado).exists():
                    messages.error(request, f'La dirección "{nombre_formateado}" ya existe')
                else:
                    Direccion.objects.create(
                        nombre_direccion=nombre_formateado,
                        id_usuario=usuario_default
                    )
                    messages.success(request, f'Dirección "{nombre_formateado}" creada exitosamente')
                    return redirect('administracion')
            else:
                messages.error(request, 'Debe ingresar un nombre para la dirección')
                
        elif accion == 'crear_departamento':
            # Crear nuevo departamento
            nombre_departamento = request.POST.get('nombre_departamento', '').strip()
            
            if nombre_departamento:
                nombre_formateado = nombre_departamento.title()
                
                if Departamento.objects.filter(nombre_departamento__iexact=nombre_formateado).exists():
                    messages.error(request, f'El departamento "{nombre_formateado}" ya existe')
                else:
                    # Obtener una dirección por defecto
                    direccion_default = Direccion.objects.first()
                    if not direccion_default:
                        direccion_default = Direccion.objects.create(
                            nombre_direccion='Dirección Principal',
                            id_usuario=usuario_default
                        )
                    
                    Departamento.objects.create(
                        nombre_departamento=nombre_formateado,
                        id_direccion=direccion_default,
                        id_usuario=usuario_default
                    )
                    messages.success(request, f'Departamento "{nombre_formateado}" creado exitosamente')
                    return redirect('administracion')
            else:
                messages.error(request, 'Debe ingresar un nombre para el departamento')
                
        elif 'direccion_id' in request.POST:
            # Eliminar dirección existente
            direccion_id = request.POST.get('direccion_id')
            if direccion_id:
                try:
                    direccion = get_object_or_404(Direccion, id_direccion=direccion_id)
                    nombre_direccion = direccion.nombre_direccion
                    direccion.delete()
                    messages.success(request, f'Dirección "{nombre_direccion}" eliminada exitosamente')
                    return redirect('administracion')
                except Exception as e:
                    messages.error(request, f'Error al eliminar dirección: {str(e)}')
                    
        elif 'departamento_id' in request.POST:
            # Eliminar departamento existente
            departamento_id = request.POST.get('departamento_id')
            if departamento_id:
                try:
                    departamento = get_object_or_404(Departamento, id_departamento=departamento_id)
                    nombre_departamento = departamento.nombre_departamento
                    departamento.delete()
                    messages.success(request, f'Departamento "{nombre_departamento}" eliminado exitosamente')
                    return redirect('administracion')
                except Exception as e:
                    messages.error(request, f'Error al eliminar departamento: {str(e)}')
    
    return render(request, 'users/administracion.html', {
        'direcciones': direcciones,
        'departamentos': departamentos
    })
#---------------------------------------------------------------------#
def asignar_cargo(request):
    usuarios = Usuario.objects.all()
    direcciones = Direccion.objects.all()
    departamentos = Departamento.objects.all()  # Agregar departamentos
    
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario')
        direccion_id = request.POST.get('direccion')
        cargo = request.POST.get('cargo')
        departamento_id = request.POST.get('departamento')  # Nuevo campo
        
        if usuario_id and cargo:
            try:
                usuario = Usuario.objects.get(id_usuario=usuario_id)
                
                if cargo == 'encargado_direccion' and direccion_id:
                    # Lógica existente para Encargado de Dirección
                    direccion = Direccion.objects.get(id_direccion=direccion_id)
                    
                    # 1. Eliminar departamento del NUEVO usuario
                    Departamento.objects.filter(id_usuario=usuario).delete()
                    
                    # 2. Verificar si la dirección YA TIENE un encargado
                    encargado_actual = direccion.id_usuario
                    
                    if encargado_actual and encargado_actual != usuario:
                        # Lógica para remover encargado anterior...
                        estado, _ = EstadoPerfil.objects.get_or_create(nombre_estado='Activo')
                        perfil_normal, _ = Perfil.objects.get_or_create(
                            nombre_perfil='Usuario Normal',
                            defaults={
                                'id_estado_perfil': estado,
                                'descripcion': 'Perfil de usuario normal'
                            }
                        )
                        encargado_actual.id_perfil = perfil_normal
                        encargado_actual.save()
                        
                        # Asignar dirección a usuario por defecto
                        usuario_default = Usuario.objects.first()
                        direcciones_anterior = Direccion.objects.filter(id_usuario=encargado_actual, id_direccion=direccion_id)
                        if direcciones_anterior.exists():
                            direcciones_anterior.update(id_usuario=usuario_default)
                        
                        Departamento.objects.filter(id_usuario=encargado_actual).delete()
                        
                        messages.info(request, f'Se removió el cargo de Encargado de Dirección a {encargado_actual.nombre} {encargado_actual.apellido}')
                    
                    # 3. Asignar el NUEVO encargado
                    estado, _ = EstadoPerfil.objects.get_or_create(nombre_estado='Activo')
                    perfil_encargado, _ = Perfil.objects.get_or_create(
                        nombre_perfil='Encargado de Dirección',
                        defaults={
                            'id_estado_perfil': estado,
                            'descripcion': 'Encargado de dirección'
                        }
                    )
                    
                    usuario.id_perfil = perfil_encargado
                    usuario.save()
                    
                    direccion.id_usuario = usuario
                    direccion.save()
                    
                    messages.success(request, f'Usuario {usuario.nombre} {usuario.apellido} asignado como Encargado de Dirección de {direccion.nombre_direccion}')
                
                elif cargo == 'encargado_departamento' and departamento_id:
                    # Lógica para Encargado de Departamento
                    departamento = Departamento.objects.get(id_departamento=departamento_id)
                    
                    # Aquí irá la lógica para asignar Encargado de Departamento
                    messages.success(request, f'Lógica para Encargado de Departamento - Usuario: {usuario.nombre}, Departamento: {departamento.nombre_departamento}')
                
                return redirect('asignar_cargo')
                
            except Usuario.DoesNotExist:
                messages.error(request, 'El usuario seleccionado no existe')
            except Direccion.DoesNotExist:
                messages.error(request, 'La dirección seleccionada no existe')
            except Departamento.DoesNotExist:
                messages.error(request, 'El departamento seleccionado no existe')
            except Exception as e:
                messages.error(request, f'Error al asignar cargo: {str(e)}')
        else:
            messages.error(request, 'Debe seleccionar usuario y cargo')
    
    return render(request, 'users/asignar_cargo.html', {
        'usuarios': usuarios,
        'direcciones': direcciones,
        'departamentos': departamentos  # Pasar departamentos al template
    })

#---------------------------------------------------------------------#
#---------------------------------------------------------------------#
#---------------------------------------------------------------------#
#---------------------------------------------------------------------#
#---------------------------------------------------------------------#
#---------------------------------------------------------------------#
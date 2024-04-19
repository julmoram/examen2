from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

# Create your views here.
def home(request):
    return render(request, "home.html")

def registro(request):
    form = UserCreationForm()
    if request.method == 'GET':
        return render(request, "registro.html", {"form": form})
    else:
        req = request.POST
        if req['password1'] == req['password2']:
            try:
                user = User.objects.create_user(
                    username=req['username'], 
                    password=req['password1']
                )
                user.save()
                login(request, user)
                return redirect('/')
            except IntegrityError:
                return render(request, "registro.html", {
                    "form": form, 
                    "msg": "El usuario ya existe"
                })
            except Exception as e:
                return render(request, "registro.html", {
                    "form": form, 
                    "msg": f"Ocurrió el siguiente error: {e}. Intente de nuevo"
                })
        else:
            return render(request, "registro.html", {
                "form": form,
                "msg": "Las contraseñas no coinciden"
            })

def iniciarsesion(request):
    if request.method == 'GET':
        return render(request, "login.html",{
            "form":AuthenticationForm,
        })
    else:
        try:
            user=authenticate(request=request,
                            username=request.POST["username"],password=request.POST["password"])
            if user is not None:
                login(request,user)
                return redirect("/")
            else:
                return render(request, "login.html",{
                "form":AuthenticationForm,
                "msg":"Usuario o contraseña incorrecta",
                })
        except Exception as e:
            return render(request, "login.html",{
            "form":AuthenticationForm,
            "msg":f"Ocurrio un error {e}",
            })
            
def cerrarsesion(request):
    logout(request)
    return redirect("/")

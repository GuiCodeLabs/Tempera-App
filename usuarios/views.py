import json

from django.conf import settings
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from .forms import UsuarioCadastroForm
from .models import GoogleAccount


User = get_user_model()


def cadastro(request):
    if request.method == "POST":
        form = UsuarioCadastroForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect("home")
    else:
        form = UsuarioCadastroForm()

    return render(request, "criar_usuario.html", {
        "form": form,
        "GOOGLE_CLIENT_ID": settings.GOOGLE_CLIENT_ID,
        "GOOGLE_LOGIN_URL": reverse("google_login"),
    })

def login_usuario(request):
    return render(request, "login_usuario.html")


@csrf_exempt
@require_POST
def google_login(request):
    try:
        body = json.loads(request.body)
        token = body.get("token")

        if not token:
            return JsonResponse({"error": "Token não enviado."}, status=400)

        request_adapter = google_requests.Request()

        idinfo = id_token.verify_oauth2_token(
            token,
            request_adapter,
            settings.GOOGLE_CLIENT_ID
        )

        google_sub = idinfo.get("sub")
        email = idinfo.get("email")
        email_verified = idinfo.get("email_verified", False)
        name = idinfo.get("name", "")
        picture = idinfo.get("picture", "")

        if not google_sub:
            return JsonResponse({"error": "Token inválido: sub ausente."}, status=401)

        if not email:
            return JsonResponse({"error": "Token inválido: email ausente."}, status=401)

        if not email_verified:
            return JsonResponse({"error": "Email do Google não verificado."}, status=401)

        # Primeiro procura se essa conta Google já foi vinculada
        google_account = GoogleAccount.objects.filter(google_sub=google_sub).first()

        if google_account:
            user = google_account.user

            # Atualiza foto caso tenha mudado
            if picture and google_account.picture != picture:
                google_account.picture = picture
                google_account.save()

            # Atualiza nome do usuário, se vier diferente
            if name and user.first_name != name:
                user.first_name = name
                user.save()

        else:
            # Se não houver vínculo Google, procura usuário pelo e-mail
            user = User.objects.filter(email=email).first()

            if not user:
                username_base = email.split("@")[0]
                username = username_base
                contador = 1

                while User.objects.filter(username=username).exists():
                    username = f"{username_base}{contador}"
                    contador += 1

                user = User.objects.create(
                    username=username,
                    email=email,
                    first_name=name,
                )
                user.set_unusable_password()
                user.save()
            else:
                if name and user.first_name != name:
                    user.first_name = name
                    user.save()

            # Verifica se o usuário já tem uma GoogleAccount
            try:
                user.googleaccount.google_sub = google_sub
                user.googleaccount.picture = picture
                user.googleaccount.save()
            except GoogleAccount.DoesNotExist:
                GoogleAccount.objects.create(
                    user=user,
                    google_sub=google_sub,
                    picture=picture
                )

        login(request, user)

        return JsonResponse({
            "ok": True,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.first_name,
                "username": user.username,
                "picture": picture,
            }
        })

    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido."}, status=400)

    except ValueError:
        return JsonResponse({"error": "Token Google inválido."}, status=401)

    except Exception as e:
        return JsonResponse({"error": f"Erro interno: {str(e)}"}, status=500)


@require_GET
def me(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Não autenticado."}, status=401)

    google_account = GoogleAccount.objects.filter(user=request.user).first()

    return JsonResponse({
        "user": {
            "id": request.user.id,
            "email": request.user.email,
            "name": request.user.first_name,
            "username": request.user.username,
            "picture": google_account.picture if google_account else None,
        }
    })


@require_POST
def logout_view(request):
    logout(request)
    return JsonResponse({"ok": True})


@login_required
def perfil(request):
    return render(request, "perfil.html", {"usuario": request.user})


@login_required
def editar_perfil(request):
    if request.method == "POST":
        form = UsuarioCadastroForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("perfil")
    else:
        form = UsuarioCadastroForm(instance=request.user)

    return render(request, "criar_usuario.html", {
        "form": form,
        "editando": True,
        "GOOGLE_CLIENT_ID": settings.GOOGLE_CLIENT_ID,
        "GOOGLE_LOGIN_URL": reverse("google_login"),
    })


@login_required
@require_POST
def deletar_usuario(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect("cadastro")
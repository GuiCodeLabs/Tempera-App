# 🍲 Tempêra

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?style=flat-square&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![Google OAuth](https://img.shields.io/badge/Google_OAuth-2.0-4285F4?style=flat-square&logo=google&logoColor=white)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange?style=flat-square)

> 🥘 **Seus ingredientes. Infinitas receitas.**

O **Tempêra** é uma plataforma web de curadoria gastronômica desenvolvida com Django. O conceito central é simples e poderoso: o usuário informa os ingredientes que já tem em casa e o sistema sugere receitas compatíveis — reduzindo o desperdício alimentar e tornando o ato de cozinhar mais acessível e criativo.

Além da busca por ingredientes, a plataforma conta com categorias culinárias, filtros por tempo de preparo e tipo de dieta (vegano, sem glúten, low carb), culinária por país de origem e uma seção de receitas em destaque com curadoria editorial. Usuários autenticados podem salvar favoritos, montar sua coleção pessoal e receber sugestões editoriais por e-mail.

O sistema de autenticação suporta cadastro tradicional e login social via **Google One Tap**, com verificação de token JWT no servidor e criação automática de conta vinculada ao perfil Google do usuário.

---

## 📐 Arquitetura do Projeto

O projeto segue a arquitetura MVT (Model-View-Template) padrão do Django, organizada em dois apps distintos com responsabilidades bem separadas:

```
├── 📁 Config                          # Módulo de configuração do projeto Django
│   ├── 🐍 __init__.py
│   ├── 🐍 asgi.py
│   ├── 🐍 settings.py                 # Configurações globais (DB, Auth, Google OAuth, CORS)
│   ├── 🐍 urls.py                     # Roteador raiz — despacha para os apps
│   └── 🐍 wsgi.py
├── 📁 tempera                         # App principal — landing page e futuras receitas
│   ├── 📁 Templates
│   │   └── 📁 Tempera
│   │       └── 🌐 home.html           # Landing page completa (UI pronta, sem backend ainda)
│   ├── 📁 migrations
│   │   └── 🐍 __init__.py
│   ├── 📁 static
│   │   └── 📁 tempera
│   │       ├── 📁 css
│   │       │   └── 🎨 home.css        # Estilos da landing page
│   │       └── 📁 images              # Variações do logotipo
│   │           ├── 🖼️ Logo_principal.png
│   │           ├── 🖼️ logo_gourmet.png
│   │           ├── 🖼️ logo_horinzotal.png
│   │           ├── 🖼️ logo_principal_black.png
│   │           ├── 🖼️ logo_principal_white.png
│   │           ├── 🖼️ logo_simples.png
│   │           └── 🖼️ logo_simples_black.png
│   ├── 🐍 __init__.py
│   ├── 🐍 admin.py
│   ├── 🐍 apps.py
│   ├── 🐍 models.py                   # (vazio — modelos de Receita ainda não implementados)
│   ├── 🐍 tests.py
│   ├── 🐍 urls.py                     # Rota raiz `/`
│   └── 🐍 views.py                    # View `home` (render direto do template)
├── 📁 usuarios                        # App de autenticação e gerenciamento de usuários
│   ├── 📁 migrations
│   │   ├── 🐍 0001_initial.py         # Criação do model Usuario (AbstractUser)
│   │   ├── 🐍 0002_googleaccount.py   # Criação do model GoogleAccount
│   │   └── 🐍 __init__.py
│   ├── 📁 static
│   │   ├── 📁 css
│   │   │   ├── 🎨 criar_usuario.css   # Estilos da tela de cadastro/login
│   │   │   └── 🎨 perfil.css         # Estilos da tela de perfil
│   │   └── 📁 js
│   │       ├── 📄 perfil.js           # Interações da tela de perfil
│   │       └── 📄 server.js           # Handler do fluxo Google One Tap
│   ├── 📁 templates
│   │   ├── 🌐 criar_usuario.html      # Tela de cadastro/login (suporta Google One Tap)
│   │   └── 🌐 perfil.html            # Tela de perfil do usuário autenticado
│   ├── 🐍 __init__.py
│   ├── 🐍 admin.py
│   ├── 🐍 apps.py
│   ├── 🐍 forms.py                    # UsuarioCadastroForm (UserCreationForm extendido)
│   ├── 🐍 models.py                   # Usuario (AbstractUser) + GoogleAccount
│   ├── 🐍 tests.py
│   ├── 🐍 urls.py                     # Prefixo `/usuarios/`
│   └── 🐍 views.py                    # cadastro, google_login, me, perfil, editar_perfil, deletar_usuario
├── ⚙️ .gitignore
├── 📝 README.md
├── 🐍 manage.py
├── 📄 requirements.txt
└── 🗄️ db.sqlite3                      # Banco SQLite local (desenvolvimento)
```

---

## ✅ O Que Está Implementado

### Autenticação e Usuários (`usuarios/`)

| Feature | Status | Notas |
|:---|:---:|:---|
| Cadastro com formulário | ✅ | `UserCreationForm` customizado com `email`, `telefone`, `data_nascimento` |
| Login/Logout padrão Django | ✅ | Session-based, rotas em `/usuarios/` |
| Login via Google (OAuth 2.0) | ✅ | Fluxo completo: Google One Tap → token JWT → verificação server-side com `google-auth` |
| Criação automática de conta Google | ✅ | Cria `Usuario` com `set_unusable_password()` e vincula ao `GoogleAccount` |
| Atualização de perfil Google | ✅ | Sincroniza `first_name` e `picture` a cada login |
| Tela de Perfil (view protegida) | ✅ | `@login_required` |
| Edição de Perfil | ✅ | Reutiliza `UsuarioCadastroForm` com `instance=request.user` |
| Exclusão de Conta | ✅ | Logout + `user.delete()` via `POST` |
| Endpoint `/usuarios/me/` | ✅ | Retorna dados do usuário autenticado em JSON |
| Upload de foto de perfil | ✅ | Campo `ImageField` → `MEDIA_ROOT` |

### Landing Page (`tempera/`)

| Feature | Status |
|:---|:---:|
| Hero com busca por ingredientes | ✅ (estático) |
| Seção de destaque de receitas | ✅ (estático) |
| Receita Surpresa | ✅ (estático) |
| Filtros Rápidos (tempo, dieta) | ✅ (estático) |
| Categorias de receitas | ✅ (estático) |
| Sabores do Mundo (culinária por país) | ✅ (estático) |
| CTA / Newsletter | ✅ (estático) |
| Estado autenticado vs. anônimo no navbar | ✅ (template Django) |

> **Nota:** "estático" significa que o HTML/CSS está implementado mas ainda sem integração com dados reais do backend.

---

## 🛠 Stack Tecnológica

### Back-end
- **Python 3.12+**
- **Django 6.0.3** — Framework MVT principal
- **google-auth** — Verificação server-side de tokens Google OAuth2 (`id_token.verify_oauth2_token`)
- **Pillow** — Processamento de uploads de imagem (`ImageField`)
- **SQLite** — Banco de dados padrão para desenvolvimento local

### Front-end
- **HTML5 / CSS3 Vanilla** — Sem frameworks CSS, estilização manual completa
- **JavaScript Vanilla** — Handler do Google One Tap (`server.js`), interações do perfil
- **Google Fonts** — `Plus Jakarta Sans` (headings) + `Inter` (body)
- **Google Material Symbols** — Ícones

### Integrações Externas
- **Google Identity Services** — Autenticação social via Google One Tap (client-side SDK + verificação server-side)

---

## 🔗 Rotas Implementadas

### Core (`/`)
| Método | Rota | View | Descrição |
|:---:|:---|:---|:---|
| `GET` | `/` | `tempera.views.home` | Landing page principal |

### Usuários (`/usuarios/`)
| Método | Rota | View | Descrição |
|:---:|:---|:---|:---|
| `GET/POST` | `/usuarios/cadastro/` | `cadastro` | Tela de cadastro e login |
| `POST` | `/usuarios/google/` | `google_login` | Endpoint JSON para autenticação Google OAuth |
| `POST` | `/usuarios/logout/` | `logout_view` | Encerra a sessão; retorna `{"ok": true}` |
| `GET` | `/usuarios/me/` | `me` | Dados do usuário atual em JSON |
| `GET` | `/usuarios/perfil/` | `perfil` | Tela de perfil `@login_required` |
| `GET/POST` | `/usuarios/perfil/editar/` | `editar_perfil` | Edição de dados do perfil |
| `POST` | `/usuarios/perfil/deletar/` | `deletar_usuario` | Exclusão permanente da conta |

### Admin
| Rota | Descrição |
|:---|:---|
| `/admin/` | Django Admin padrão |

---

## 🗄 Modelos de Dados

### `usuarios.Usuario` (estende `AbstractUser`)
| Campo | Tipo | Observação |
|:---|:---|:---|
| `username` | `CharField` | Herdado |
| `email` | `EmailField` | `unique=True`, obrigatório |
| `foto` | `ImageField` | Upload em `fotos_perfil/` |
| `bio` | `TextField` | Opcional |
| `data_nascimento` | `DateField` | Opcional |
| `telefone` | `CharField(20)` | Opcional |

### `usuarios.GoogleAccount`
| Campo | Tipo | Observação |
|:---|:---|:---|
| `user` | `OneToOneField(Usuario)` | Cascata de delete |
| `google_sub` | `CharField(255)` | Identificador único do Google, `unique=True` |
| `picture` | `URLField` | URL do avatar do Google |

---

## ⚙️ Instalação e Execução

### Pré-requisitos
- Python 3.12+
- Git

### 1. Clonar o repositório

```bash
git clone https://github.com/GuiCodeLabs/Tempera-App.git
cd Tempera-App
```

### 2. Criar e ativar o ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto. As variáveis mínimas necessárias são:

```env
SECRET_KEY=sua_django_secret_key_aqui
DEBUG=True
GOOGLE_CLIENT_ID=seu_google_client_id_aqui
```

> **Atenção:** O `GOOGLE_CLIENT_ID` atualmente está hardcoded em `Config/settings.py`. Para produção, mova-o para o `.env` e leia via `os.environ`.

### 5. Aplicar as migrations

```bash
python manage.py migrate
```

### 6. (Opcional) Criar superusuário para o Admin

```bash
python manage.py createsuperuser
```

### 7. Rodar o servidor de desenvolvimento

```bash
python manage.py runserver
```

Acesse em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🔑 Autenticação Google OAuth — Fluxo Técnico

O fluxo implementado usa **Google Identity Services (GIS)** no client-side:

```
1. Usuário clica no botão Google One Tap (renderizado pelo SDK GIS)
2. Google retorna um ID Token (JWT) para o callback JS handleCredentialResponse()
3. server.js faz POST para /usuarios/google/ com { token: <jwt> }
4. Django verifica o token com google.oauth2.id_token.verify_oauth2_token()
5. Se válido: busca ou cria Usuario + GoogleAccount, então chama login()
6. Retorna JSON { ok: true } → frontend redireciona para /
```

### Configuração no Google Cloud Console

Para habilitar o OAuth, acesse o [Google Cloud Console](https://console.cloud.google.com/) e configure:

**Origens JavaScript autorizadas:**
```
http://localhost:8000
http://127.0.0.1:8000
```

**URIs de redirecionamento autorizados:**
```
http://localhost:8000/usuarios/google/callback/
http://127.0.0.1:8000/usuarios/google/callback/
```

> **Nota:** O fluxo atual usa **Google One Tap** (token enviado via `fetch` para `/usuarios/google/`), que não depende de um URI de redirecionamento. Os URIs acima são necessários caso o projeto evolua para o fluxo OAuth padrão com redirecionamento (Authorization Code Flow).

---

## 📋 To-Do List (Backlog)

### Alta Prioridade — Core do Produto
- [ ] **Model `Receita`** — Criar modelo com campos: `titulo`, `descricao`, `ingredientes`, `modo_preparo`, `tempo_preparo`, `categoria`, `pais_origem`, `imagem`, `autor (FK Usuario)`
- [ ] **CRUD de Receitas** — Views e templates para criar, listar, detalhar, editar e excluir receitas
- [ ] **Sistema de Favoritos** — Model `Favorito (Usuario ↔ Receita)` + endpoint toggle (o botão já existe no frontend)
- [ ] **Busca por Ingredientes** — Lógica de query no backend para a caixa de busca da landing page (atualmente sem ação)
- [ ] **Filtros Funcionais** — Conectar filtros de tempo e dieta da landing page a queries reais

### Média Prioridade — UX e Funcionalidades
- [ ] **Receita Surpresa** — Endpoint que retorna receita aleatória do banco (`Receita.objects.order_by('?').first()`)
- [ ] **Filtro por Culinária/País** — Os botões "Sabores do Mundo" precisam de lógica de filtragem
- [ ] **Categorias** — Model `Categoria` e páginas de listagem por categoria
- [ ] **Newsletter** — Model para captura de e-mails e integração com serviço de disparo (ex: Mailchimp ou SMTP)
- [ ] **Página "Sobre"** — Criar rota e template para a seção de missão

### Qualidade e Segurança
- [ ] **Mover segredos para `.env`** — `GOOGLE_CLIENT_ID` e `SECRET_KEY` estão hardcoded em `settings.py`
- [ ] **Configurar `ALLOWED_HOSTS`** — Atualmente vazio; precisa ser preenchido para qualquer deploy
- [ ] **Testes automatizados** — Os arquivos `tests.py` existem mas estão vazios
- [ ] **`STATIC_ROOT` + `collectstatic`** — Necessário para servir estáticos em produção
- [ ] **Login social completo** — A tela de cadastro redireciona para `cadastro` tanto para Login quanto Registrar; separar os fluxos
- [ ] **Paginação** — Nas futuras listagens de receitas

### Infraestrutura (Futuro)
- [ ] **Docker + Docker Compose** — Ainda não há `Dockerfile` nem `docker-compose.yml` no repositório
- [ ] **PostgreSQL** — Migrar de SQLite para Postgres (especialmente para deploy)
- [ ] **Variáveis de ambiente com `django-environ` ou `python-decouple`**

---

## ⚠️ Observações Técnicas

- **`AUTH_USER_MODEL = 'usuarios.Usuario'`** — O modelo de usuário foi substituído logo no início do projeto. Qualquer app Django adicionado futuramente deve referenciar `settings.AUTH_USER_MODEL`, nunca `auth.User` diretamente.
- **CORS e CSRF** — `CSRF_TRUSTED_ORIGINS` está configurado apenas para `localhost`. Ao adicionar um domínio de produção, essa lista deve ser atualizada.
- **`SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin-allow-popups'`** — Necessário para o popup de autenticação Google funcionar corretamente.
- **Imagens externas no template** — A landing page atual referencia imagens hospedadas externamente (CDN do Google). Em produção, hospedar localmente ou via object storage.

---

## 👨‍💻 Autores

Desenvolvido por **Guilherme Beserra** e **Pedro Henrique**

> 🚧 Projeto em desenvolvimento ativo.
> Feito com ❤️ muito ☕ e muita dedicação 🚀

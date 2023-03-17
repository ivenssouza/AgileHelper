from ninja import Router
from schema.user_schema import UserSchemaOut, UserSchemaIn, UserSchemaLogIn
from schema.http_exceptions import BadRequestHttpException,ConflictHttpException, HttpException
from django.contrib.auth.models import User
from django.contrib import auth, messages

router = Router()

@router.get(path="", tags=["Users"], summary="GET all existing Users", description="GET all existing Users", response={200: list[UserSchemaOut], 500: HttpException},)
def getUser(request):
    try:
        list_users = User.objects.all()
        return list_users
    except Exception as e:
        return 500, HttpException(
            status= 500,
            message= e.message,
        )

@router.post(path="/createUser", tags=["Users"], summary="Sign up new Users", description="Sign up new users", response={201: UserSchemaOut, 400: BadRequestHttpException, 409: ConflictHttpException, 500: HttpException},)
def createUser(request, body:UserSchemaIn):
    try:
        if campo_vazio(body.username):
            return 400, BadRequestHttpException(
                status = 400,
                message = "User Name field is mandatory"
            )
        
        if campo_vazio(body.first_name):
            return 400, BadRequestHttpException(
                status = 400,
                message = "First Name field is mandatory"
            )
        
        if campo_vazio(body.last_name):
            return 400, BadRequestHttpException(
                status = 400,
                message = "Last Name field is mandatory"
            )

        if campo_vazio(body.email):
            return 400, BadRequestHttpException(
                status = 400,
                message = "E-mail field is mandatory"
            )
            
        if User.objects.filter(username=body.username).exists() or User.objects.filter(email=body.email).exists():
            return 409, ConflictHttpException(
                status = 409,
                message = "User Name or e-mail already exists",
            ) 

        user = User.objects.create_user(username=body.username,first_name=body.first_name,last_name=body.last_name,email=body.email,password=body.password)
        user.save()
        return 201, user
    except Exception as e:
        return 500, HttpException(
            status= 500,
            message= e.message,
        )

@router.get(path="/login", tags=["Users"], summary="Log in the system", description="Log in the system", response={200: None, 400: BadRequestHttpException, 500: HttpException},)
def login(request, body: UserSchemaLogIn):

    if campo_vazio(body.username):
        return 400, BadRequestHttpException(
            status = 400,
            message = "User Name or E-mail field are mandatory"
        )
    
    if campo_vazio(body.password):
        return 400, BadRequestHttpException(
            status = 400,
            message = "Password field is mandatory"
        )

    if User.objects.filter(email=body.username).exists():
        nome = User.objects.filter(email=body.username).values_list('username', flat=True).get()
        user = auth.authenticate(request, username=nome, password=senha)
        if user is not None:
            auth.login(request, user)
            print('Login realizado com sucesso')
            return redirect('dashboard')
        
    if User.objects.filter(email=body.username).exists() or User.objects.filter(username=body.username).exists():
        nome = User.objects.filter(email=body.username).values_list('username', flat=True).get()
        user = auth.authenticate(request, username=nome, password=senha)
        if user is not None:
            auth.login(request, user)
            print('Login realizado com sucesso')
            return redirect('dashboard')

    return render(request, 'usuarios/login.html')

@router.post(path="/logout", tags=["Users"], summary="Log out the system", description="Log out the system", response={201: str, 400: BadRequestHttpException, 409: str, 500: HttpException},)
def logout(request):
    auth.logout(request)
    #return redirect('index')

#EXEMPLO PARA VERIFICAR SE O USUÁRIO ESTÁ LOGADO
#def dashboard(request):
#    if request.user.is_authenticated:
#        id = request.user.id
#        receitas = Receita.objects.order_by('-data_receita').filter(pessoa=id)
#
#        dados = { 
#            'receitas' : receitas
#        }
#        return render(request, 'usuarios/dashboard.html', dados)
#    else:
#        return redirect('index')

def campo_vazio(campo):
    return not campo.strip()

def senhas_nao_sao_iguais(senha, senha2):
    return senha != senha2
# FastAPI Crud
Esta API tiene como objetivo ser un crud de usuarios, autenticar y consumir el api de [Studio Ghibli](https://ghibliapi.vercel.app/) según el rol de cada usuario.
- CRUD para usuarios
- Autenticación / Autorización
- Notificación de a usuarios después de la creación
- Cosumo de API [Studio Ghibli](https://ghibliapi.vercel.app/)

## Develop
Este proyecto utiliza como framework [FastAPI](https://fastapi.tiangolo.com/), en base de datos [MongoDB](https://www.mongodb.com/cloud/atlas) y [Docker](https://docs.docker.com/).

### Requisitos
- Tener instalado docker
- Tener un api-key de [Brevo](https://www.brevo.com/es/) y un template. Dicho template debe recibir como paramentros: name y role.

### Tech-stack
- Python 3.12
- [FastAPI](https://fastapi.tiangolo.com/)
- [MongoDB](https://www.mongodb.com/cloud/atlas)
- [Docker](https://docs.docker.com/)

### Instalación
1. Clonar repositorio
    ``` bash
    git clone 'https://github.com/irvyncornejo/fastapi-crud.git'
    ```
2. Verificar que tenemos docker
    ``` bash
    docker version
    ```
    * En caso de no tener docker instalado, favor de instalarlo.

3. Movernos a la carpeta fastapi-crud
    ``` bash
    cd fastapi-crud
    ```
4. Crear el archivo con las variables de entorno.
    ``` bash
    nano .env
    ```
    * Copia y pega las variables de prueba y en caso de tener el api-key de Brevo; cambiala, para que puedas recibir las notificaciones por correo.
    ``` bash
    export mongo_conn_str = 'mongodb://root:example@mongo:27017'
    export env = 'DEV'
    export api_key_brevo = ''
    export secret_key = 'TEST09'
    export db_name = 'public'
    export users_colecction_name = 'users'
    export admin_email = 'admin@test.com'
    export admin_password = '56er%hji90G567'
    ```

5. Construir y ejecutar los contenedores (FastAPI y MongoDB)
    ``` bash
    docker-compose up --build
    ```
    * Verificar contenedores
    ``` bash
    docker ps
    ```
6. Después de que la aplicación está corriendo podemos ingresar a la documentación.
    - URL Doc http://127.0.0.1:8000/docs


## Funcionalidades
1. Autenticación de usuarios
    * Es necesario proporciona username(email) y password, para obtener el access token.
    * Método: POST
    * Path: [api/v2/auth](http://localhost:8000/docs#/Auth/auth_auth_post)

2. Creación de usuarios
    * No se requiere autenticación
    * Este endpoint crea usuarios con los siguientes roles
        - films
        - people
        - locations
        - species
        - vehicles
    * Si el correo proporcionado es real se envia una notificación por correo eléctronico, después de la creación.
    * Se válida que el usuario no este registrado o que tenga una solicitud de eliminar
    * Método: POST
    * Path: [api/v2/users](http://localhost:8000/docs#/Users/create_user_users_post)

3.  Obtener usuarios
    * Requiere autenticación
    * Este endpoint esta disponible solo para le rol admin; cualquier otro rol no tiene los permisos necesarios
    * Método: GET
    * Path: [api/v2/users](http://localhost:8000/docs#/Users/retrieve_users_users_get)

4.  Obtener usuario
    * Requiere autenticación
    * Los usuario con rol admin pueden ver cualquier usuario y cualquier otro rol; solo puede consultar su información. En el nodo data se incluye la consulta al api de Studio Ghibli
    * Método: GET
    * Path: [api/v2/users](http://localhost:8000/docs#/Users/retrieve_users_users_get)

5.  Actualizar usuario
    * Requiere autenticación
    * Solo se puede actualizar la información del usuario autenticado
    * Método: PUT
    * Path: [api/v2/users](http://localhost:8000/docs#/Users/update_user_users__id__put)

6.  Eliminar usuario
    * Requiere autenticación
    * Si la socilicitud la hace un usuario admin el borrado es total y si es otro rol el borrado el lógico
    * Método: DELETE
    * Path: [api/v2/users](http://localhost:8000/docs#/Users/delete_user_users__id__delete)

7.  Recuperar información del usuario autenticado
    * Requiere autenticación
    * Método: DELETE
    * Path: [api/v2/me](http://localhost:8000/docs#/Users/retrive_me_me_get)

8.  Registrar Admin(User)
    * Requiere autenticación con role admin
        - Por default se tiene un usuario admin, revisar variables de entorno
    * Método: POST
    * Path: [api/v2/admins](http://localhost:8000/docs#/Admins/create_user_admin_admins_post)

## Test
Se tienen algunos casos cubiertos en las pruebas
1. Copiar variables para ejecutar pruebas
    ``` bash
    cp .env ./app/.env
    ```
2. Ejecutar pruebas
    ``` bash
    cd app
    pytest test -s
    ```

## License

This project is licensed under the Apache-2 permissive license - see the [Licence file](LICENSE) for details.
# Penguin Random House Grupo Editorial - Entrevista Tecnica

El siguiente repositorio contiene el desarrollo de la [consigna](./Consigna_ML_Engineer_RS.pdf) para la Entrevista Tecnica para Penguin Random House Grupo Editorial. 



## Ejecutar localmente

1. Instalar [entorno virtual](https://virtualenv.pypa.io/en/latest/installation.html) de python, buildear y activar un nuevo entorno virtual.


```
# Build the virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

2. Instalar dependencias

```
pip install -r requirements.txt
```

3. Ejecutar el servidor localmente

```
uvicorn src.app:app --host 0.0.0.0 --port 8123 --reload
```

4. Ir a [`http://localhost:8123/docs`](http://localhost:8123/docs) para usar Swagger API


## Ejecutar en un contenedor de Docker

1. [Instalar Docker](https://docs.docker.com/engine/install/) localmente y asegurarse de que este corriendo.

2. Buildear la imagen de Docker

```
docker build -t project_image -f Dockerfile .
```

3. Ejecutar la imagen dentro de un contenedor

```
docker run -d -p 8123:8123 -v $(pwd):/code --name project_container project_image
```

4. Ir a [`http://localhost:8123/docs`](http://localhost:8123/docs) para usar Swagger API

# Probando el servidor

Una vez que este ejecutandose el servidor, bien sea de forma local o en un container Docker, podemos hacer un request rapido y sencillo para verificar que este funcionando correctamente.

1. Abrir la terminal

2. Ejecuta el siguiente comando

```
curl "localhost:8123/data_analysis?mean=true&include_ar=true"
```

3. Deberías obtener la siguiente salida

```
{"AR":{"mean":656.5600000000001}}
```

# Tests unitarios

* Dado que el alcance del problema es muy pequeño y solo tenemos un unico endpoint, se consideraron las pruebas unitarias y las pruebas de integracion como las mismas. Es decir, hacemos los tests directamente sobre la API.
    * En caso de que el proyecto crezca, es recomendable desacoplar estos tests.   

* Se implementaron los siguientes caso de uso felices

1. Cuando el usuario solicita una o varias metricas en argentina, entonces el sistema devuelve las metricas para argentina.

2. Cuando el usuario solicita una o varias metricas en argentina y filtrando para un año especifico, entonces el sistema devuelve las metricas para argentina en ese año.

3. Cuando el usuario solicita una o varias metricas en uno o varios paises, entonces el sistema devuelve la informacion correcta para cada pais.

4. Cuando el usuario solicita una o varias metricas en uno o varios paises e indica que es un resultado global, entonces el sistema devuelve metricas globales.

* Se implementaron los siguientes casos de uso borde:

1. Cuando el usuario no envia ninguna metrica a calcular, entonces el sistema devuelve un error legible indicando que debe indicar **por lo menos una metrica** a calcular

2. Cuando el usuario no especifica ningun pais sobre el cual calcular las metricas, entonces el sistema devuelve un error legible indicando que debe indicar **por lo menos un pais** sobre el cual operar

3. Cuando los filtros devuelven un dataset vacio, entonces se espera que devuelva un error legible.

## Correr los tests

* Para correr todos los tests localmente, ejecuta el siguiente comando

```
pytest test/
```

* Para correr un test especifico, ejecuta el siguiente comando

```
pytest test/test_[filename]::test_[function_name]
```

# Proceso CI/CD

* Este proyecto tiene una pequeña integracion CI/CD usando [Github Actions](https://docs.github.com/en/actions) y [Railway](https://railway.com/). Se puede acceder a una demo del proyecto en el siguiente enlace: [https://penguin-random-house-interview-production.up.railway.app/docs](https://penguin-random-house-interview-production.up.railway.app/docs)

* Como parte del proceso CI, se bloqueo el permiso para pushear directo a main, y los Pull Requests unicamente se pueden mergearse con main una vez que todos los tests pasen.
* Cambios a main automaticamente se despliegan en la plataforma de Railway.

# Preguntas conceptuales

## Experiencia previa en nuestro stack tecnológico (Snowflake, Airflow, DBT, AWS, Databricks, CI/CD en gitlab) o similares. Breve resumen de algún proyecto en el que hayas aplicado estas herramientas.

[TODO]

## ¿Cuál te parece la mejor estrategia para versionar y guardar datos y modelos en Databricks?

[TODO]


## ¿Qué estrategias usarías para optimizar costos en clústeres?

* Herramientas como Apache Spark se especializan en manejo de sistemas distribuidos. Para poder optimizar costos nos conviene distribuir la carga en multiples nodos dentro del cluster de manera que ninguno especifico este sobresaturado.

[TODO]

## ¿Cómo implementarías seguridad (secret scopes, roles)?

* Desde el punto de vista de seguridad en la nube, utilizaria el [principle of least privilege](https://www.cloudflare.com/learning/access-management/principle-of-least-privilege/) en donde cada usuario, grupo o rol se le asigna unicamente los permisos que requiere y nada mas.
* Para almacenar informacion sensible como credenciales o API tokens, usaria el secret manager de la plataforma que se este utilizando, ya que suele brindar una forma segura, nativa y facil de utilizar. Por ejemplo en AWS usaria [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html), en Github usaria [secrets en GitHub Actions](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets), en Databricks usaria [Secret management](https://docs.databricks.com/aws/en/security/secrets/)
* Desde el punto de vista de seguridad en APIs se podria utilizar tokens para poder identificar a los usuarios. Una posible implementacion es utilizando [AWS Security Token Service](https://docs.aws.amazon.com/STS/latest/APIReference/welcome.html) el cual se integra con el servicio [Amazon API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html)
* Implementaria trazabilidad utilizando monitoreo, alertas y acciones para detectar en tiempo real cuando existen cambios inesperados en los recursos.
* En linea general, siendo que la seguridad informatica es muy extensa, me guiaria del [pilar de seguridad informatica de AWS](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/security.html) en donde explican los principales decisiones de diseño a tener en cuenta a la hora de crear y usar productos y servicios en la nube.


## ¿Cómo harías troubleshooting si un job tarda 3 horas en vez de 30 min?

* Verificaria si el error es interno (el codigo de la empresa esta fallando) o externo (los servidores de la nube estan fallando)
    * Si el error es externo, si es posible, correria el job desde otro provider para verificar que no hayan errores
    * Si el error es interno:
        * Iria al sistema de monitoreo y buscaria por algunos errores que este arrojando y empezaria a investigar estos errores.
        * Buscaria por deadlocks, loops infinitos o bloqueo por ausencia de líder (en caso de sistemas distribuidos).
        * En caso de ser un sistema distribuido, evaluaria los logs de cada nodo para entender en cual punto esta fallando y por que.


## ¿Para qué sirve un Dockerfile y qué produce cuando se construye?

* Dockerfile sirve para escribir declarativamente instrucciones que Docker va a ejecutar para construir una Docker Image.
* Los containers ejecutan instances de Docker images.

## ¿Qué diferencias hay entre un request GET y un POST trabajando con una API?

GET y POST son metodos HTTP utilizados para operaciones CRUD (create, retrieve, update, delete) en una API REST.

* [GET](https://restfulapi.net/http-methods/#get) se utiliza unicamente para consultar (**retrieve**) informacion (recursos)
* [POST](https://restfulapi.net/http-methods/#post) se utiliza para crear (**create**) recursos


## ¿Qué buenas prácticas seguirías para trabajar en equipo usando herramientas de versionado?

1. Bloquear acceso para pushear a directo main. Unicamente agregar codigo a travez de Pull Requests
2. Realizar commits pequeños y descriptivos.
3. Documentar infraestructura, instrucciones para correr y cualquier cosa relevante dentro de `README.md`
4. Agregar tests unitarios y de integracion al crear nuevas features y validar que los cambios no hayan roto tests anteriores.
5. Crear una nueva branch para cada nueva implementacion y seguir estandares de branch naming
    * `feature/xxx` nueva feature
    * `hotfix/xxx` arreglo urgente
    * `develop` rama ligeramente mas avanzada a main en donde se prueban las nuevas features en un entorno staging antes de ser llevadas a produccion.
    

Algunas buenas practicas adicionales que brinda Github

1. Rapidamente levantar un nuevo requisito (feature request) a travez de [Github issues](https://docs.github.com/en/issues). Para tener mayor orden, se puede usar un template y rellenar los campos.
2. [Tableros Kanban](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects) para tener un vistazo de que esta trabajando cada persona y que tareas quedan pendientes.
3. Cuando una tarea este lista para revision, abrir [Github Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request), esperar feedback y corregirlos en el mismo PR, y luego mergear a main.
4. [Opcional] Usando Github Actions o con pre-commit, automatizar linter (por ejemplo [mypy](https://mypy.readthedocs.io/en/stable/index.html) o [black](https://pypi.org/project/black/)) para seguir estandares internos de calidad de codigo.
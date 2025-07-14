# UnencryptPDF

UnencryptPDF es una Función de Azure (Azure Function) diseñada para desencriptar archivos PDF protegidos con contraseña. La función se activa a través de una petición HTTP, procesa el archivo en memoria y lo devuelve desencriptado si la contraseña es correcta.

## ✨ Características

  * Desencripta archivos PDF protegidos por contraseña.
  * Implementado como una API sin servidor (serverless) en Azure Functions.
  * Validación de la existencia del archivo y la contraseña en la petición.
  * Verifica si el PDF está realmente encriptado antes de procesarlo.
  * Manejo de errores para contraseñas incorrectas, archivos no válidos o vacíos.
  * Configuración para un fácil despliegue y desarrollo local con Visual Studio Code.

## 📋 Requisitos Previos

Antes de comenzar, asegúrese de tener instalado lo siguiente:

  * Python 3.8 o superior.
  * [Azure Functions Core Tools](https://learn.microsoft.com/es-es/azure/azure-functions/functions-run-local).
  * Una cuenta de Azure (para el despliegue).
  * Visual Studio Code (recomendado) con las siguientes extensiones:
      * [Azure Functions](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions)
      * [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

## 🚀 Instalación

1.  **Clone el repositorio:**

    ```bash
    git clone <URL-DEL-REPOSITORIO>
    cd <NOMBRE-DEL-DIRECTORIO>
    ```

2.  **Cree y active un entorno virtual:**
    Se recomienda encarecidamente utilizar un entorno virtual para gestionar las dependencias del proyecto.

    ```bash
    # Crear entorno virtual (.venv es el nombre configurado en settings.json)
    python -m venv .venv

    # Activar en Windows
    .venv\Scripts\activate

    # Activar en macOS/Linux
    source .venv/bin/activate
    ```

3.  **Instale las dependencias:**
    El proyecto incluye un archivo `requirements.txt` con todas las bibliotecas de Python necesarias.

    ```bash
    pip install -r requirements.txt
    ```

## ▶️ Uso

### Ejecución Local

Puede iniciar la función localmente para pruebas utilizando las tareas predefinidas de VS Code o la CLI de Azure Functions.

  * **Usando VS Code:**

    1.  Abra el proyecto en Visual Studio Code.
    2.  Presione `F5` o vaya a la pestaña "Ejecutar y depurar" y seleccione "Attach to Python Functions". Esto iniciará el host de la función y adjuntará el depurador. La tarea `pip install` se ejecutará automáticamente si es necesario.

  * **Usando la CLI:**

    ```bash
    func host start
    ```

La función estará disponible en la siguiente URL local:
`http://localhost:7071/api/decrypt`

### Petición a la API

Para usar la función, debe enviar una petición `POST` de tipo `multipart/form-data` con los siguientes campos:

  * `pdf_file`: El archivo PDF encriptado que desea procesar.
  * `password`: La contraseña para desencriptar el PDF.

#### Ejemplo con cURL

A continuación, un ejemplo de cómo llamar a la API utilizando cURL desde su terminal:

```bash
curl -X POST \
  http://localhost:7071/api/decrypt \
  -F "pdf_file=@/ruta/a/su/archivo.pdf" \
  -F "password=su_contraseña_secreta" \
  --output decrypted.pdf
```

  * Reemplace `/ruta/a/su/archivo.pdf` con la ruta real de su archivo PDF.
  * Reemplace `su_contraseña_secreta` con la contraseña del archivo.
  * El comando guardará el archivo desencriptado como `decrypted.pdf` en el directorio actual.

### Respuestas de la API

  * **`200 OK`**: Si la desencriptación es exitosa, la respuesta contendrá el flujo del archivo PDF desencriptado (`application/pdf`).
  * **`400 Bad Request`**: Si falta el archivo (`pdf_file`) o la contraseña (`password`) en la petición, o si el archivo no es un PDF válido.
  * **`401 Unauthorized`**: Si la contraseña proporcionada es incorrecta.
  * **`422 Unprocessable Entity`**: Si intenta desencriptar un archivo PDF que no está encriptado.
  * **`500 Internal Server Error`**: Si ocurre un error inesperado en el servidor durante el procesamiento.

## ☁️ Despliegue en Azure

Este proyecto está configurado para ser desplegado en Azure Functions. La configuración en `.vscode/settings.json` especifica que el despliegue debe hacerse desde la raíz del proyecto y que las dependencias deben construirse durante el despliegue (`scmDoBuildDuringDeployment`).

Puede desplegar la función utilizando la extensión de Azure Functions en VS Code o a través de la CLI de Azure.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si desea mejorar este proyecto, por favor, siéntase libre de hacer un fork del repositorio, crear una nueva rama y enviar un Pull Request.

## 📄 Licencia

Este proyecto no especifica una licencia. Considere añadir un archivo `LICENSE` para aclarar los términos bajo los cuales otros pueden usar y distribuir su código.
# Proyecto: Automatización de Rutas Urbanas
**Autor:** Alonso Hernández González
**Fecha:** Febrero 2025  
**Cohorte:** 20  
**Sprint:** 8  

## Descripción
Este proyecto utiliza Selenium para automatizar la interacción con una página web de solicitud de taxis urbanos. Permite realizar acciones como ingresar direcciones de origen y destino, seleccionar la tarifa Comfort, agregar un número de teléfono y tarjeta de crédito, solicitar artículos adicionales y confirmar la búsqueda de un taxi.

## Requisitos
Antes de ejecutar el proyecto, asegúrate de tener instalado lo siguiente:

- Python 3.x
- Google Chrome
- ChromeDriver compatible con la versión de Chrome instalada
- Librerías necesarias:
  ```bash
  pip install selenium
  ```

## Instalación
1. Clona este repositorio o descarga los archivos.
2. Instala las dependencias requeridas utilizando el comando mencionado anteriormente.
3. Asegúrate de tener configurado `ChromeDriver` en el PATH o proporciona su ruta en el código si es necesario.

## Uso
Para ejecutar las pruebas automatizadas:

```bash
pytest main.py
```

O puedes ejecutar manualmente el script en Python:

```bash
python main.py
```

### Funcionalidades
El script automatiza las siguientes tareas:
- Ingreso de direcciones de origen y destino.
- Selección de la tarifa Comfort.
- Registro y confirmación de un número de teléfono.
- Adición de una tarjeta de crédito.
- Envío de mensajes personalizados al conductor.
- Solicitud de artículos adicionales como mantas y pañuelos.
- Pedido de helados como extra en el viaje.
- Confirmación del proceso de búsqueda de taxi.

## Estructura del Proyecto
- `main.py`: Contiene la implementación de las pruebas y la automatización de la página.
- `data.py`: Contiene datos como URL de la web, número de teléfono, tarjetas de crédito de prueba, etc. *(No incluido, pero debe ser creado si se requiere para ejecutar el script.)*

## Notas
- El código usa Selenium WebDriver con Chrome.
- Se requiere conexión a internet para ejecutar correctamente el script.
- Asegúrate de que los selectores de los elementos en la web no hayan cambiado; de lo contrario, necesitarás actualizarlos en `main.py`.

## Contribución
Si deseas mejorar este proyecto, puedes enviar un pull request con mejoras o correcciones. También puedes reportar problemas en la sección de "Issues".

## Licencia
Este proyecto está bajo la licencia MIT. Puedes utilizarlo y modificarlo libremente.


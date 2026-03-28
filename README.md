# 💳 Alke Wallet — Fintech App

Una aplicación web robusta y profesional para la gestión de billeteras digitales, desarrollada con **Django** y **SQLite**. Este proyecto permite administrar usuarios, múltiples cuentas bancarias y transacciones financieras con un sistema de filtrado y ordenamiento avanzado.

---

## ✨ Características Principales

- **Gestión Multi-Cuenta**: Un único usuario puede poseer y gestionar múltiples cuentas bancarias (Corriente y Ahorro) de forma simultánea.
- **Filtrado Avanzado (ORM)**: Capacidad para filtrar clientes por tipo de cuenta y realizar ordenamientos dinámicos por saldo total acumulado.
- **Historial de Transacciones**: Registro detallado de depósitos y retiros con actualización automática de saldos e integridad referencial.
- **Interfaz Premium**: Diseño visualmente atractivo, centrado y profesional, optimizado para la gestión administrativa de clientes.
- **Seguridad y Robustez**: Implementación de variables de entorno para protección de claves y manejo de integridad en cascada (`on_delete=CASCADE`).
- **Arquitectura**: Sigue el patrón MVT de Django con una base de datos relacional altamente eficiente.

---

## 🚀 Instalación y Uso

### 1. Clonar el repositorio
```bash
git clone https://github.com/ramirousnayo/alke_wallet.git
cd alke_wallet
```

### 2. Configurar el entorno
Se recomienda usar un entorno virtual:
```bash
python3 -m venv venv
source venv/bin/activate  # En Mac/Linux
venv\Scripts\activate # En Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto copiando el archivo de ejemplo:
```bash
cp .env.example .env
```
Genera una clave única y segura con el siguiente comando:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```
Luego abre el archivo `.env` y pega la clave generada en la variable `SECRET_KEY`.


### 5. Preparar la Base de Datos
Es fundamental aplicar las migraciones para activar el esquema multi-cuenta:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Ejecutar la Aplicación
```bash
python manage.py runserver
```
Visita `http://127.0.0.1:8000` en tu navegador.

---

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python 3.x, Django
- **Frontend**: HTML5, CSS3 (Vanilla), Django Templates
- **Base de Datos**: SQLite3
- **Seguridad**: Python-dotenv (Gestión de variables de entorno)

---

## 📄 Documentación Técnica

Para una explicación detallada del modelo de datos de esta wallet, su arquitectura relacional y guías de uso, consulta el [Documento Explicativo](documento_explicativo.md).

---

## 👤 Autor

**Ramiro Usnayo**

---

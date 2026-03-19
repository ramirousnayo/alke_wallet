# 💳 Alke Wallet — Fintech App

Una aplicación web robusta y elegante para la gestión de billeteras digitales, desarrollada con **Django** y **SQLite**. Este proyecto permite administrar usuarios, cuentas y transacciones financieras con actualización de saldo en tiempo real.

---

## ✨ Características Principales

- **Gestión de Usuarios (CRUD)**: Registro, edición y visualización detallada de clientes.
- **Finanzas en Tiempo Real**: Creación automática de cuentas al registrar usuarios y cálculo dinámico de saldos mediante depósitos y retiros.
- **Seguridad**: Implementación de variables de entorno para proteger claves sensibles.
- **Diseño Premium**: Interfaz limpia, responsiva y con sistema de notificaciones integrado.
- **Arquitectura**: Sigue el patrón MVT de Django con una base de datos relacional robusta.

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
python -m venv venv
source venv/bin/activate  # En Mac/Linux
# o venv\Scripts\activate en Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto basándote en lo siguiente:
```ini
SECRET_KEY=tu_clave_secreta_aqui
DEBUG=True
```

### 5. Ejecutar la Aplicación
```bash
python manage.py runserver
```
Visita `http://127.0.0.1:8000` en tu navegador.

---

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python 3.x, Django 6.x
- **Frontend**: HTML5, CSS3 (Vanilla), Django Templates
- **Base de Datos**: SQLite3
- **Seguridad**: Python-dotenv

---

## 📄 Documentación Técnica

Para una explicación detallada del modelo de datos, las relaciones y capturas de pantalla del funcionamiento, consulta el [Documento Explicativo](documento_explicativo.md).

---

## 👤 Autor

**Ramiro Usnayo**
- GitHub: [@ramirousnayo](https://github.com/ramirousnayo)

---

> Prototipo desarrollado para el proyecto final del módulo de desarrollo web con Django.

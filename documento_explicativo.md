# Documento Explicativo — Alke Wallet

## 1. Modelo de Datos
El sistema se basa en tres entidades principales:
- **Usuario**: Representa a la persona. Campos: `nombre`, `email` (único), `creado_en`.
- **Cuenta**: Una billetera digital vinculada a un usuario (Relación 1 a 1). Campos: `usuario`, `saldo` (decimal), `activa` (boolean).
- **Transacción**: Registra movimientos de dinero (Relación de 1 a muchos con Cuenta). Campos: `cuenta`, `tipo` (depósito/retiro), `monto`, `fecha`, `descripción`.

## 2. Operaciones Implementadas (CRUD)
Se desarrollaron vistas y plantillas para las siguientes acciones:
- **Crear**: Formulario para registrar usuarios. Al guardar, se genera automáticamente una cuenta con saldo inicial de 0.
- **Leer**: Lista de usuarios registrados y vista de detalle con información de su cuenta.
- **Actualizar**: Edición de datos básicos de usuario.
- **Eliminar**: Eliminación de usuario y su cuenta asociada (vía `CASCADE`).

## 3. Funcionamiento Técnico
- **ORM**: Todas las operaciones usan el ORM de Django.
- **Migraciones**: Se han aplicado todas las migraciones necesarias al archivo `db.sqlite3`.
- **Navegación**: Las URLs están centralizadas en `wallet/urls.py` e integradas en el proyecto principal.

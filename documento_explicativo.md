# Documento Explicativo — Alke Wallet

## 1. Modelo de Datos

Para este proyecto, se diseñaron tres modelos interconectados que representan la lógica de negocio de una billetera digital:

- **Modelo `Usuario`**: Representa al cliente del banco.
    - **Campos**: `nombre` (CharField), `email` (EmailField único), `creado_en` (DateTimeField automático).
    - **Relación**: Es el modelo base. No tiene claves foráneas externas.

- **Modelo `Cuenta`**: Representa las cuentas bancarias asociadas a un usuario.
    - **Campos**: `saldo` (DecimalField con 2 decimales), `tipo_cuenta` (CharField con opciones: 'corriente' o 'ahorro').
    - **Relación**: **ForeignKey (1 a N)** hacia `Usuario`. Un usuario puede tener múltiples cuentas. Se usa `on_delete=CASCADE` para mantener la integridad.

- **Modelo `Transaccion`**: Registra los movimientos de dinero.
    - **Campos**: `monto` (DecimalField), `tipo` (CharField: 'deposito' o 'retiro'), `fecha` (DateTimeField), `descripcion` (TextField opcional).
    - **Relación**: **ForeignKey (1 a N)** hacia `Cuenta`. Cada transacción pertenece a una sola cuenta.

---

## 2. Operaciones CRUD Implementadas

Se han desarrollado vistas basadas en funciones utilizando el ORM de Django para las siguientes operaciones:

### 👤 Gestión de Usuarios
- **Crear**: A través de `UsuarioForm`, se validan y guardan nuevos clientes en la base de datos.
- **Leer**: Se implementó una lista general de usuarios (`Usuario.objects.all()`) con filtros avanzados por tipo de cuenta y ordenamiento por saldo. También existe una vista de detalle que recupera un usuario específico y sus cuentas relacionadas.
- **Actualizar**: Permite modificar el nombre o email de un cliente existente.
- **Eliminar**: Elimina el registro del usuario y, por efecto de la relación `CASCADE`, borra automáticamente sus cuentas y transacciones.

### 💰 Gestión de Cuentas (Banco)
- **Crear**: Permite añadir nuevas cuentas (ahorro/corriente) a un usuario existente.
- **Actualizar/Eliminar**: Permite gestionar las cuentas de forma independiente desde el perfil del usuario.

### 💳 Gestión de Transacciones
- **Crear**: Permite registrar ingresos o egresos vinculados a una cuenta.
- **Leer**: Listado global de todas las transacciones realizadas en el sistema, permitiendo ver el historial completo de movimientos del banco.
- **Detalle/Editar/Eliminar**: Gestión completa de cada movimiento individual para correcciones o auditoría.

---

## 3. Capturas de Pantalla

### Lista de Usuarios
![Lista de usuarios](capturas/usuario_list.png)

### Crear Usuario
![Formulario de creación](capturas/usuario_create.png)

### Editar Usuario
![Formulario de edición](capturas/usuario_edit.png)

### Eliminar Usuario
![Confirmación de eliminación](capturas/usuario_delete.png)

### Lista de Transacciones
![Lista de transacciones](capturas/transaccion_list.png)

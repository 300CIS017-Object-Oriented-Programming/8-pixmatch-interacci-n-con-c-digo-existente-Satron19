## Requisitos Funcionales y Criterios de Aceptación

### 1. Configuración de Nivel de Dificultad
**Requisito:** Los jugadores deben poder seleccionar el nivel de dificultad antes de iniciar el juego.

**Criterios de Aceptación:**
- Debe haber opciones de dificultad disponibles: fácil, medio y difícil.
- La elección de dificultad debe afectar la mecánica del juego, incluida la frecuencia de regeneración de imágenes y la puntuación.
- Los tiempos de regeneración deben ser específicos:
  - Fácil: cada 8 segundos.
  - Medio: cada 6 segundos.
  - Difícil: cada 5 segundos.

### 2. Visualización de la Matriz de Juego
**Requisito:** El sistema debe mostrar una matriz de juego donde los jugadores puedan interactuar.

**Criterios de Aceptación:**
- La matriz debe tener un tamaño determinado por el nivel de dificultad seleccionado.
- Debe mostrarse una variedad de imágenes en la matriz, representando los elementos del juego.
- La matriz debe actualizarse dinámicamente para reflejar los cambios en el estado del juego.

### 3. Interacción del Jugador
**Requisito:** Los jugadores deben poder interactuar con la matriz de juego al presionar botones.

**Criterios de Aceptación:**
- Se deben proporcionar botones para que el jugador elija las imágenes que desea seleccionar en la matriz.
- Al presionar un botón, se debe actualizar el estado de la matriz y el puntaje del jugador.
- La selección de imágenes debe ser limitada según las opciones disponibles en cada momento.

### 4. Puntuación del Jugador
**Requisito:** El sistema debe mantener un registro de la puntuación del jugador durante el juego.

**Criterios de Aceptación:**
- La puntuación debe aumentar cada vez que el jugador realiza una acción válida, como seleccionar una imagen correcta.
- La puntuación debe disminuir cada vez que el jugador realiza una acción válida, como seleccionar una imagen incorrecta.
- La puntuación debe mostrarse claramente al jugador en todo momento durante el juego.

### 5. Líderes y Tablero de Puntuación
**Requisito:** El sistema debe incluir un tablero de puntuación para mostrar las puntuaciones más altas.

**Criterios de Aceptación:**
- Se debe mantener un registro de las puntuaciones más altas de los jugadores.
- El tablero de puntuación debe ser visible para los jugadores y mostrar las puntuaciones más altas junto con los nombres de los jugadores.
- Debe haber una opción para restablecer el tablero de puntuación si es necesario.

### 6. Experiencia de Usuario
**Requisito:** El sistema debe proporcionar una experiencia de usuario fluida y agradable.

**Criterios de Aceptación:**
- La interfaz de usuario debe ser intuitiva y fácil de entender para los jugadores de todos los niveles.
- Se deben proporcionar indicadores visuales claros para guiar al jugador a través del juego, como botones resaltados o mensajes informativos.
- El rendimiento del juego debe ser óptimo, con tiempos de carga mínimos y sin retrasos perceptibles durante la interacción del jugador.

### 7. Personalización de Nombre del Jugador
**Requisito:** Los jugadores deben poder personalizar su nombre antes de comenzar el juego.

**Criterios de Aceptación:**
- Debe haber un campo de entrada donde los jugadores puedan escribir su nombre antes de iniciar el juego.
- El nombre del jugador debe mostrarse durante el juego junto con su puntuación.
- Se debe permitir a los jugadores omitir la personalización si lo desean, en cuyo caso se utilizará un nombre predeterminado.

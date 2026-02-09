[![progress-banner](https://backend.codecrafters.io/progress/ai-agent/id/placeholder)](https://app.codecrafters.io/courses/ai-agent/overview)

This is a starting point for Python solutions to the
["Build Your Own AI Agent" Challenge](https://app.codecrafters.io/courses/ai-agent/overview).

In this challenge, you'll build an AI coding agent similar to Claude Code or Cursor Agent. Your agent will be able to use tools like reading/writing files, executing terminal commands, and more.

**Note**: Head over to [codecrafters.io](https://codecrafters.io) to try the challenge.

---

# AI Coding Agent

Un agente de IA que puede ejecutar tareas de programación usando herramientas (tools) como leer/escribir archivos y ejecutar comandos en terminal.

## Arquitectura

El proyecto usa POO con las siguientes clases:

- **`Tool`** (ABC): Clase base abstracta para definir herramientas
- **`ToolRegistry`**: Registro para gestionar y ejecutar herramientas
- **`Agent`**: Implementa el loop de conversación con el LLM

### Tools disponibles

| Tool | Descripción |
|------|-------------|
| `read_file` | Lee el contenido de un archivo |
| `write_file` | Escribe contenido a un archivo |
| `bash_terminal` | Ejecuta comandos en bash |

## Uso

```bash
./your_program.sh -p "tu prompt aquí"
```

### Ejemplos

```bash
# Leer un archivo
./your_program.sh -p "Lee el contenido de README.md"

# Ejecutar comandos
./your_program.sh -p "Lista los archivos en el directorio actual"

# Tareas complejas
./your_program.sh -p "Encuentra todos los archivos Python y cuenta las líneas de código"
```

## Configuración

Variables de entorno:

| Variable | Descripción | Default |
|----------|-------------|---------|
| `OPENROUTER_API_KEY` | API key de OpenRouter | (requerido) |
| `OPENROUTER_BASE_URL` | URL base de la API | `https://openrouter.ai/api/v1` |
| `OPENROUTER_MODEL` | Modelo a usar | `anthropic/claude-haiku-4.5` |

## Estructura del proyecto

```
app/
├── main.py      # Entry point
├── agent.py     # Clase Agent (loop de conversación)
├── tool.py      # Clases base Tool y ToolRegistry
└── tools.py     # Implementaciones concretas de tools
```

## Agregar un nuevo Tool

1. Crear una clase que herede de `Tool` en `tools.py`
2. Implementar las propiedades `name`, `description`, `parameters`
3. Implementar el método `execute(**kwargs)`
4. Registrar en `create_default_registry()`
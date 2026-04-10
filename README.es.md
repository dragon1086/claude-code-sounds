<div align="center">
  <img src="docs/assets/banner.png" alt="claude-code-sounds" width="600" />
</div>

<div align="center">

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Validate](https://github.com/dragon1086/claude-code-sounds/actions/workflows/validate.yml/badge.svg)](https://github.com/dragon1086/claude-code-sounds/actions/workflows/validate.yml)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey)
![Hook Coverage](https://img.shields.io/badge/hooks-27%20events%20covered-7c3aed)

</div>

<div align="center">

**[English](README.md) · [한국어](README.ko.md) · [中文](README.zh.md) · [日本語](README.ja.md)**

</div>

Un plugin que reproduce sonidos cada vez que Claude Code realiza una acción. 27 eventos — inicio de sesión, modificación de archivos, tareas completadas y más — tienen efectos de sonido asignados. El pack predeterminado usa voces del anime One Piece, y puedes cambiar de pack modificando un solo archivo de configuración.

## Cómo funciona

<div align="center">
  <img src="docs/assets/flow.png" alt="How claude-code-sounds works" width="700" />
</div>

Utiliza el sistema de hooks nativo de Claude Code para ejecutar un script de Python y reproducir sonidos cuando ocurren eventos específicos. No requiere demonios ni procesos en segundo plano.

## Instalación

### Opción A — Marketplace de plugins (recomendado)

Escribe esto en el chat de Claude Code:

```
/plugin marketplace add https://github.com/dragon1086/claude-code-sounds
/plugin install claude-code-sounds
```

Al seleccionar el alcance:

| Opción | Resultado |
|--------|-----------|
| **user (global)** ✅ | Los sonidos se reproducen en todos los proyectos automáticamente — esta es la opción recomendada |
| project | Solo en este proyecto — requiere configuración adicional (ver abajo) |
| local | Igual que project, pero excluido de git (configuración personal) — también requiere configuración adicional |

> **Tras la instalación:** Reinicia Claude Code para activar los hooks.

#### Configuración adicional para alcance project/local

Ejecuta esto una vez dentro de tu proyecto:

```bash
bash "$(find ~/.claude/plugins/cache/claude-code-sounds -name "claude-sounds.sh" | head -1)" setup-project
```

Reinicia Claude Code y los sonidos funcionarán. Este comando copia los hooks en `.claude/hooks/` y los registra en `.claude/settings.json`.

---

### Opción B — Instalación con curl (alcance project)

Instala en `.claude/hooks/` del proyecto actual. Ejecuta desde dentro del directorio del proyecto. Repite en cada proyecto donde quieras sonidos.

```bash
curl -fsSL https://raw.githubusercontent.com/dragon1086/claude-code-sounds/main/install.sh | bash
```

### Opción C — Clonar manualmente (alcance project)

Igual que la Opción B — instala solo en el proyecto actual.

```bash
git clone https://github.com/dragon1086/claude-code-sounds
cd claude-code-sounds && ./install.sh
```

> **Tras la instalación:** Reinicia Claude Code para activar los hooks.

## Requisitos

- Python 3
- macOS (`afplay`), Linux (`paplay` / `aplay` / `ffplay`), o Windows (`winsound` integrado)

No se necesitan bibliotecas adicionales.

## Cambiar de pack de sonido

Usa el comando `claude-sounds.sh use` para cambiar todos los sonidos a la vez. Esta es la única forma de cambiar de pack — `activePack` en `hooks-config.json` es solo una etiqueta que indica qué pack se aplicó por última vez y no afecta los sonidos que se reproducen en tiempo de ejecución.

### Packs incluidos

| Pack | Descripción |
|------|-------------|
| `onepiece` | Voces reales del anime One Piece — escenas icónicas de Luffy, Zoro, Robin y más |
| `best-practice` | Voz ElevenLabs "Samara X" — portada desde el proyecto claude-code-best-practice |
| `silent` | 100ms de silencio — desactiva los sonidos sin eliminar los hooks |
| `default` | Set de efectos de sonido básicos |

### Cómo cambiar de pack

**Marketplace de plugins (alcance user) — caso más común:**

```bash
bash "$(find ~/.claude/plugins/cache/claude-code-sounds -name "claude-sounds.sh" | sort -V | tail -1)" use onepiece
```

No es necesario reinstalar. El cambio se aplica de inmediato.

**install.sh / clonado manualmente:**

```bash
# Paso 1: cambiar el pack en el repositorio
./claude-sounds.sh use onepiece

# Paso 2: volver a aplicar al proyecto
./install.sh --force
```

Ver el pack activo actualmente: `./claude-sounds.sh current`

Listar todos los packs disponibles: `./claude-sounds.sh list`

### Packs de la comunidad

Consulta [PACKS.md](PACKS.md) para ver los packs contribuidos por la comunidad. Para contribuir con tu propio pack, consulta [packs/README.md](packs/README.md).

## Personalizar sonidos individuales

Si solo quieres cambiar el sonido de un evento específico, reemplaza el archivo en `.claude/hooks/sounds/{evento}/`:

```
.claude/hooks/sounds/stop/
└── stop.wav   ← reemplaza esto con tu propio sonido
```

El nombre del archivo debe coincidir con el nombre de la carpeta. Se admiten tanto `.wav` como `.mp3` (se intenta `.wav` primero).

### Especial: sonidos por comando Bash

Puedes asignar sonidos específicos a comandos bash concretos. Por ejemplo, `git commit` reproduce `pretooluse-git-committing.wav` en lugar del genérico `pretooluse.wav`.

Agrega tus propios patrones en `hooks.py`:

```python
BASH_PATTERNS = [
    (r'git commit', "pretooluse-git-committing"),  # incluido por defecto
    (r'npm test',   "pretooluse-npm-testing"),      # añade el tuyo
    (r'rm -rf',     "pretooluse-danger"),
    (r'git push',   "pretooluse-git-pushing"),
]
```

Cada patrón necesita un archivo correspondiente en `sounds/pretooluse/pretooluse-{nombre}.wav`.

## Deshabilitar hooks específicos

Para desactivar hooks individuales sin desinstalar, crea `.claude/hooks/config/hooks-config.local.json` (ignorado por git automáticamente):

```json
{
  "disablePostToolUseHook": true,
  "disableLogging": true
}
```

Consulta `hooks/config/hooks-config.local.json.example` para ver todas las opciones disponibles.

## Cobertura de hooks

Los 27 eventos de hooks de Claude Code están conectados, más 6 eventos con alcance de agente:

| Categoría | Eventos |
|-----------|---------|
| Sesión | `SessionStart`, `SessionEnd`, `Setup` |
| Herramienta | `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied` |
| Turno | `UserPromptSubmit`, `Stop`, `StopFailure`, `Notification` |
| Subagente | `SubagentStart`, `SubagentStop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted` |
| Contexto | `PreCompact`, `PostCompact`, `InstructionsLoaded`, `ConfigChange` |
| Entorno | `CwdChanged`, `FileChanged`, `WorktreeCreate`, `WorktreeRemove` |
| MCP | `Elicitation`, `ElicitationResult` |

## Sonidos para agentes

Las sesiones de subagentes pueden reproducir sonidos distintos. Conecta los hooks en el frontmatter de tu agente:

```yaml
---
name: my-agent
hooks:
  PreToolUse:
    - type: command
      command: python3 $CLAUDE_PROJECT_DIR/.claude/hooks/scripts/hooks.py --agent=my-agent
      async: true
      timeout: 5000
  Stop:
    - type: command
      command: python3 $CLAUDE_PROJECT_DIR/.claude/hooks/scripts/hooks.py --agent=my-agent
      async: true
      timeout: 5000
---
```

Los archivos de sonido van en `agent_pretooluse/`, `agent_stop/`, etc.

## Desinstalar

```bash
./uninstall.sh
```

## Créditos

Inspirado en [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice), que demostró por primera vez cómo integrar retroalimentación de audio en los hooks de Claude Code. Este proyecto toma esa idea y la convierte en un plugin independiente e instalable con cobertura completa de hooks, packs de sonido y soporte multiplataforma.

## Licencia

MIT

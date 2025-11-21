# GitHub Actions - Workflows

Este directorio contiene los workflows de CI/CD para el proyecto BookMe API.

## Workflows Disponibles

### 1. CI Pipeline (`ci.yml`)

**Trigger:** Push o Pull Request a `main` o `develop`

**Jobs:**

#### Test
- Ejecuta tests en múltiples versiones de Python (3.10, 3.11, 3.12)
- Tests unitarios con cobertura
- Tests de integración
- Genera reporte de cobertura y lo sube a Codecov

#### Lint
- Verifica formato de código con Black
- Verifica orden de imports con isort
- Analiza código con Flake8

#### Security
- Escanea dependencias con Safety
- Analiza seguridad del código con Bandit

### 2. Deploy Pipeline (`deploy.yml`)

**Trigger:** Push a `main` o tags que empiecen con `v*`

**Jobs:**

#### Deploy
- Ejecuta tests antes del deployment
- Construye imagen Docker
- Crea release en GitHub (solo para tags)
- Deployment a producción (requiere configuración)

## Configuración Necesaria

### Secrets de GitHub

Para que los workflows funcionen completamente, necesitas configurar estos secrets en tu repositorio:

1. `CODECOV_TOKEN` (opcional): Token para subir cobertura a Codecov
2. `DEPLOY_KEY` (opcional): Credenciales para deployment

**Cómo agregar secrets:**
1. Ve a tu repositorio en GitHub
2. Settings → Secrets and variables → Actions
3. Click en "New repository secret"
4. Agrega los secrets necesarios

### Badges para README

Agrega estos badges a tu README.md principal:

```markdown
![CI Pipeline](https://github.com/USUARIO/REPO/workflows/CI%20Pipeline/badge.svg)
![Deploy](https://github.com/USUARIO/REPO/workflows/CD%20Pipeline%20-%20Deploy/badge.svg)
[![codecov](https://codecov.io/gh/USUARIO/REPO/branch/main/graph/badge.svg)](https://codecov.io/gh/USUARIO/REPO)
```

## Ejecución Local de Tests

Antes de hacer push, puedes ejecutar los tests localmente:

```bash
# Activar entorno virtual
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac

# Tests unitarios con cobertura
pytest tests/unit/ -v --cov=src --cov-report=term-missing

# Tests de integración
pytest tests/integration/ -v

# Todos los tests
pytest tests/ -v --cov=src --cov-report=xml

# Linting
black --check src/ tests/
isort --check-only src/ tests/
flake8 src/ tests/ --max-line-length=120
```

## Docker

### Build local
```bash
docker build -t bookme-api .
```

### Run con Docker Compose
```bash
docker-compose up -d
```

### Stop
```bash
docker-compose down
```

## Estrategia de Branches

- `main`: Rama de producción, protegida
- `develop`: Rama de desarrollo
- `feature/*`: Ramas de características
- `hotfix/*`: Ramas de correcciones urgentes

## Pull Request Checklist

Antes de crear un PR, asegúrate de:

- [ ] Todos los tests pasan localmente
- [ ] Código formateado con Black
- [ ] Imports ordenados con isort
- [ ] Sin errores de Flake8
- [ ] Cobertura de tests mantenida o mejorada
- [ ] Documentación actualizada si es necesario
- [ ] CHANGELOG.md actualizado

## Troubleshooting

### Error: "pytest: command not found"
Asegúrate de tener el entorno virtual activado y las dependencias instaladas.

### Tests fallan en GitHub pero pasan localmente
Verifica que:
- La versión de Python sea la misma
- Las dependencias en `requirements.txt` estén actualizadas
- No haya dependencias de archivos locales

### Docker build falla
Verifica que:
- `.dockerignore` esté configurado correctamente
- Todas las dependencias estén en `requirements.txt`
- Los paths en el Dockerfile sean correctos

# Guía de Uso - GitHub Actions CI/CD

## 📋 Contenido

Los siguientes archivos han sido creados para el pipeline de CI/CD:

### Workflows de GitHub Actions
- `.github/workflows/ci.yml` - Pipeline de Integración Continua
- `.github/workflows/deploy.yml` - Pipeline de Deployment
- `.github/workflows/README.md` - Documentación de workflows

### Docker
- `Dockerfile` - Configuración para construir imagen Docker
- `.dockerignore` - Archivos a excluir del build
- `docker-compose.yml` - Orquestación de contenedores

### Configuración de Herramientas
- `pytest.ini` - Configuración de pytest
- `.flake8` - Configuración de linting
- `.isort.cfg` - Configuración de ordenamiento de imports

### Scripts de Validación
- `scripts/pre-push.sh` - Script bash para validaciones pre-push
- `scripts/pre-push.ps1` - Script PowerShell para validaciones pre-push

## 🚀 Primeros Pasos

### 1. Instalar Dependencias Actualizadas

```bash
# Activar entorno virtual
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac

# Instalar todas las dependencias (incluyendo herramientas de dev)
pip install -r requirements.txt
```

### 2. Probar Localmente

#### Ejecutar Tests
```bash
pytest tests/ -v --cov=src
```

#### Formatear Código
```bash
# Auto-formatear con Black
black src/ tests/

# Ordenar imports
isort src/ tests/
```

#### Verificar Linting
```bash
flake8 src/ tests/
```

### 3. Usar Script de Pre-Push

**Windows (PowerShell):**
```powershell
.\scripts\pre-push.ps1
```

**Linux/Mac:**
```bash
chmod +x scripts/pre-push.sh
./scripts/pre-push.sh
```

## 🔧 Configurar GitHub Repository

### 1. Subir el Código

```bash
# Inicializar repositorio (si no existe)
git init

# Agregar archivos
git add .

# Commit
git commit -m "feat: Add CI/CD pipeline with GitHub Actions"

# Agregar remote (reemplaza con tu repo)
git remote add origin https://github.com/TU-USUARIO/bookme-api.git

# Push
git push -u origin main
```

### 2. Configurar Branch Protection

1. Ve a tu repositorio en GitHub
2. Settings → Branches
3. Add rule para `main`
4. Marca:
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
   - Selecciona: test, lint, security

### 3. Configurar Secrets (Opcional)

Para Codecov:
1. Settings → Secrets and variables → Actions
2. New repository secret
3. Nombre: `CODECOV_TOKEN`
4. Valor: Token de https://codecov.io

## 🐳 Docker

### Build Local
```bash
docker build -t bookme-api:latest .
```

### Run con Docker
```bash
# Solo la API
docker run -p 8000:8000 bookme-api:latest

# Con Docker Compose (API + Redis)
docker-compose up -d
```

### Ver Logs
```bash
docker-compose logs -f api
```

### Stop
```bash
docker-compose down
```

## 📊 Badges para README

Agrega estos badges a tu `README.md` principal:

```markdown
![CI Pipeline](https://github.com/TU-USUARIO/bookme-api/workflows/CI%20Pipeline/badge.svg)
![Deploy](https://github.com/TU-USUARIO/bookme-api/workflows/CD%20Pipeline%20-%20Deploy/badge.svg)
[![codecov](https://codecov.io/gh/TU-USUARIO/bookme-api/branch/main/graph/badge.svg)](https://codecov.io/gh/TU-USUARIO/bookme-api)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
```

## 🔄 Flujo de Trabajo Recomendado

### Para Features
```bash
# Crear branch
git checkout -b feature/nueva-funcionalidad

# Desarrollar y hacer commits
git add .
git commit -m "feat: agregar nueva funcionalidad"

# Antes de push, verificar localmente
.\scripts\pre-push.ps1  # Windows
./scripts/pre-push.sh   # Linux/Mac

# Push
git push origin feature/nueva-funcionalidad

# Crear Pull Request en GitHub
```

### Para Hotfixes
```bash
git checkout -b hotfix/corregir-bug
# ... desarrollar ...
git push origin hotfix/corregir-bug
```

## ✅ Checklist Pre-Push

Antes de hacer push, verifica:

- [ ] ✅ Tests pasan: `pytest tests/ -v`
- [ ] 🎨 Código formateado: `black src/ tests/`
- [ ] 📦 Imports ordenados: `isort src/ tests/`
- [ ] 🔍 Sin errores de linting: `flake8 src/ tests/`
- [ ] 📝 CHANGELOG.md actualizado (si aplica)
- [ ] 📄 Documentación actualizada (si aplica)

## 🐛 Troubleshooting

### Pipeline falla pero tests pasan localmente

**Problema:** Diferentes versiones de Python o dependencias.

**Solución:**
```bash
# Verifica tu versión de Python
python --version

# Reinstala dependencias
pip install -r requirements.txt --force-reinstall
```

### Error de permisos en scripts

**Windows:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Linux/Mac:**
```bash
chmod +x scripts/*.sh
```

### Docker build falla

```bash
# Limpia builds anteriores
docker system prune -a

# Rebuild sin cache
docker build --no-cache -t bookme-api:latest .
```

### Coverage muy bajo

```bash
# Ver reporte detallado
pytest tests/ -v --cov=src --cov-report=html

# Abre htmlcov/index.html en tu navegador
```

## 📚 Recursos Adicionales

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Docker Docs](https://docs.docker.com/)
- [pytest Docs](https://docs.pytest.org/)
- [Black Docs](https://black.readthedocs.io/)
- [Flake8 Docs](https://flake8.pycqa.org/)

## 🆘 Soporte

Si tienes problemas:
1. Revisa los logs del pipeline en GitHub Actions
2. Ejecuta el script de pre-push localmente para debug
3. Verifica que todas las dependencias estén instaladas
4. Consulta la documentación en `.github/workflows/README.md`

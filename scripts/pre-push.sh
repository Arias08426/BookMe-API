#!/bin/bash
# Script para ejecutar todas las validaciones antes de hacer push

echo "🚀 Ejecutando validaciones pre-push..."
echo ""

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contador de errores
ERRORS=0

# 1. Tests
echo "📝 Ejecutando tests..."
if pytest tests/ -v --cov=src --cov-report=term; then
    echo -e "${GREEN}✓ Tests passed${NC}"
else
    echo -e "${RED}✗ Tests failed${NC}"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# 2. Black
echo "🎨 Verificando formato con Black..."
if black --check src/ tests/; then
    echo -e "${GREEN}✓ Black check passed${NC}"
else
    echo -e "${YELLOW}⚠ Black encontró problemas. Ejecuta: black src/ tests/${NC}"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# 3. isort
echo "📦 Verificando imports con isort..."
if isort --check-only src/ tests/; then
    echo -e "${GREEN}✓ isort check passed${NC}"
else
    echo -e "${YELLOW}⚠ isort encontró problemas. Ejecuta: isort src/ tests/${NC}"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# 4. Flake8
echo "🔍 Analizando código con Flake8..."
if flake8 src/ tests/; then
    echo -e "${GREEN}✓ Flake8 check passed${NC}"
else
    echo -e "${RED}✗ Flake8 encontró problemas${NC}"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# 5. Safety (opcional)
echo "🔒 Verificando vulnerabilidades con Safety..."
if safety check --json > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Safety check passed${NC}"
else
    echo -e "${YELLOW}⚠ Safety encontró posibles vulnerabilidades${NC}"
    # No incrementar errores, solo advertencia
fi
echo ""

# Resumen
echo "================================"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ Todas las validaciones pasaron!${NC}"
    echo "Puedes hacer push con confianza 🎉"
    exit 0
else
    echo -e "${RED}✗ $ERRORS validación(es) fallaron${NC}"
    echo "Por favor corrige los errores antes de hacer push"
    exit 1
fi

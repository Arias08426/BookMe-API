# Script para ejecutar todas las validaciones antes de hacer push

Write-Host "🚀 Ejecutando validaciones pre-push..." -ForegroundColor Cyan
Write-Host ""

$ERRORS = 0

# 1. Tests
Write-Host "📝 Ejecutando tests..." -ForegroundColor Yellow
try {
    pytest tests/ -v --cov=src --cov-report=term
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Tests passed" -ForegroundColor Green
    } else {
        Write-Host "✗ Tests failed" -ForegroundColor Red
        $ERRORS++
    }
} catch {
    Write-Host "✗ Error ejecutando tests" -ForegroundColor Red
    $ERRORS++
}
Write-Host ""

# 2. Black
Write-Host "🎨 Verificando formato con Black..." -ForegroundColor Yellow
try {
    black --check src/ tests/
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Black check passed" -ForegroundColor Green
    } else {
        Write-Host "⚠ Black encontró problemas. Ejecuta: black src/ tests/" -ForegroundColor DarkYellow
        $ERRORS++
    }
} catch {
    Write-Host "⚠ Black no está instalado o falló" -ForegroundColor DarkYellow
}
Write-Host ""

# 3. isort
Write-Host "📦 Verificando imports con isort..." -ForegroundColor Yellow
try {
    isort --check-only src/ tests/
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ isort check passed" -ForegroundColor Green
    } else {
        Write-Host "⚠ isort encontró problemas. Ejecuta: isort src/ tests/" -ForegroundColor DarkYellow
        $ERRORS++
    }
} catch {
    Write-Host "⚠ isort no está instalado o falló" -ForegroundColor DarkYellow
}
Write-Host ""

# 4. Flake8
Write-Host "🔍 Analizando código con Flake8..." -ForegroundColor Yellow
try {
    flake8 src/ tests/
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Flake8 check passed" -ForegroundColor Green
    } else {
        Write-Host "✗ Flake8 encontró problemas" -ForegroundColor Red
        $ERRORS++
    }
} catch {
    Write-Host "⚠ Flake8 no está instalado o falló" -ForegroundColor DarkYellow
}
Write-Host ""

# 5. Safety
Write-Host "🔒 Verificando vulnerabilidades con Safety..." -ForegroundColor Yellow
try {
    $safetyOutput = safety check --json 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Safety check passed" -ForegroundColor Green
    } else {
        Write-Host "⚠ Safety encontró posibles vulnerabilidades" -ForegroundColor DarkYellow
    }
} catch {
    Write-Host "⚠ Safety no está instalado" -ForegroundColor DarkYellow
}
Write-Host ""

# Resumen
Write-Host "================================" -ForegroundColor Cyan
if ($ERRORS -eq 0) {
    Write-Host "✓ Todas las validaciones pasaron!" -ForegroundColor Green
    Write-Host "Puedes hacer push con confianza 🎉" -ForegroundColor Green
    exit 0
} else {
    Write-Host "✗ $ERRORS validación(es) fallaron" -ForegroundColor Red
    Write-Host "Por favor corrige los errores antes de hacer push" -ForegroundColor Red
    exit 1
}

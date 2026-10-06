# Desarrollo y publicación

## Instalación

```bash
pip install "robotframework-paylo[robot]"
```

Para Python puedes instalar `robotframework-paylo` sin las dependencias del adaptador de Robot.

## Desarrollo y publicación

```bash
python -m pip install -e ".[robot,dev]"
pytest
ruff check .
ruff format --check .
python docs/scripts/build_docs.py
poetry build
```

Los pull requests validan el código, los ejemplos del navegador, ambos idiomas y los paquetes.
La documentación se despliega desde `main`. Las versiones se publican mediante OIDC Trusted Publishing:
configura el repositorio `robotframework-paylo`, workflow `release.yml` y entorno `pypi`; publica el tag `v0.1.0`.
No se guardan tokens de API. El tag debe coincidir con la versión de `pyproject.toml`.

# Sistema para Generar Programas con SCL (Structured Control Language)

![SCL System Banner](https://img.shields.io/badge/Industry-4.0-blue?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

Este proyecto es una plataforma integral diseñada para facilitar la creación, validación y gestión de programas en **SCL (Structured Control Language)**, cumpliendo con el estándar internacional **IEC 61131-3**. Está optimizado para entornos industriales que utilizan PLCs de Siemens (TIA Portal).

## 🚀 Características Principales

- **Validador de Sintaxis en Tiempo Real:** Detecta errores comunes como falta de puntos y comas, bloques no cerrados (`IF` sin `END_IF`) y operadores de asignación incorrectos.
- **Generación Inteligente:** Plantillas preconfiguradas para componentes industriales comunes:
  - Control de Motores (Bloques de Función FB).
  - Escalado de Sensores Analógicos.
  - Procesamiento de Arrays y Cálculos Matemáticos.
- **Generación mediante IA:** Genera lógica SCL compleja a partir de descripciones en lenguaje natural.
- **Gestión de Proyectos:** Guarda y organiza tus bloques de código (FC, FB, DB) en una base de datos local.
- **Interfaz Moderna:** Dashboard intuitivo construido con React para una experiencia de usuario fluida.

## 🛠️ Arquitectura del Sistema

El sistema utiliza una arquitectura desacoplada para garantizar escalabilidad y facilidad de mantenimiento:

### Backend (Python/FastAPI)
- **API REST:** Procesa las solicitudes del frontend.
- **Motor de Validación:** Analiza el código SCL mediante expresiones regulares y lógica de bloques.
- **Persistencia:** SQLite con SQLAlchemy para el almacenamiento de datos.

### Frontend (React/Vite)
- **Editor de Código:** Interfaz optimizada para la escritura de SCL.
- **Visualización de Errores:** Feedback visual inmediato sobre la validez del código.
- **Componentes Modulares:** Estructura limpia y reactiva.

## 📂 Estructura del Proyecto

```text
├── backend/            # Lógica del servidor y API (FastAPI)
├── frontend/           # Interfaz de usuario (React + Vite)
├── docs/               # Documentación técnica e investigación
├── scripts/            # Scripts de utilidad
└── README.md           # Documentación principal
```

## ⚙️ Instalación y Configuración

### Requisitos Previos
- Python 3.8+
- Node.js 16+
- Git

### Configuración del Backend
1. Navega a la carpeta backend:
   ```bash
   cd backend
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Inicia el servidor:
   ```bash
   python main.py
   ```

### Configuración del Frontend
1. Navega a la carpeta frontend:
   ```bash
   cd frontend
   ```
2. Instala las dependencias:
   ```bash
   npm install
   ```
3. Inicia la aplicación:
   ```bash
   npm run dev
   ```

## 📚 Documentación
Para profundizar en el estándar IEC 61131-3 y cómo este sistema implementa las reglas de SCL, revisa el archivo de investigación en:
[Investigación IEC 61131-3](docs/investigacion_iec61131.md)

## 👤 Autor
**Luis Morato Canet**
- GitHub: [@luismoratocanet28-dev](https://github.com/luismoratocanet28-dev)

---
*Desarrollado para la modernización de la programación industrial.*

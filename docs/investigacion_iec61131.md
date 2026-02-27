# Investigación sobre el Estándar IEC 61131-3 y SCL para Siemens

## 1. Introducción al Estándar IEC 61131-3
El estándar IEC 61131-3 es una norma internacional que define los lenguajes de programación para Controladores Lógicos Programables (PLC). Su objetivo es estandarizar la forma en que se programan los sistemas de automatización industrial, permitiendo que los ingenieros utilicen lenguajes consistentes independientemente del fabricante.

El estándar define cinco lenguajes principales:
*   **LAD (Ladder Diagram):** Diagrama de contactos (gráfico).
*   **FBD (Function Block Diagram):** Diagrama de bloques de funciones (gráfico).
*   **SFC (Sequential Function Chart):** Gráfico de funciones secuenciales.
*   **IL (Instruction List):** Lista de instrucciones (texto de bajo nivel).
*   **ST (Structured Text):** Texto estructurado (texto de alto nivel).

## 2. Lenguaje SCL (Structured Control Language) de Siemens
SCL es la implementación específica de Siemens del lenguaje **Structured Text (ST)** definido en IEC 61131-3. Es un lenguaje de alto nivel basado en PASCAL, ideal para tareas que involucran cálculos matemáticos complejos, gestión de datos y algoritmos de control que serían difíciles de implementar en lenguajes gráficos como Ladder.

### Características Principales:
*   **Integración Total:** SCL está totalmente integrado en TIA Portal (Step 7), permitiendo llamar a bloques SCL desde LAD/FBD y viceversa.
*   **Potencia Algorítmica:** Excelente para manejar bucles (FOR, WHILE) y condiciones complejas (IF-THEN-ELSE).
*   **Legibilidad:** El código es compacto y fácil de documentar, facilitando el mantenimiento a largo plazo.

## 3. Sintaxis y Componentes en Siemens SCL
Siemens SCL sigue reglas estrictas para garantizar la compatibilidad y el rendimiento:

### Tipos de Datos:
*   **Simples:** BOOL, INT, REAL, DINT, TIME, DATE.
*   **Compuestos:** ARRAY, STRUCT, UDT (User Defined Types).

### Estructuras de Control:
*   **Condicionales:**
    ```scl
    IF #valor > 10 THEN
        #estado := TRUE;
    ELSIF #valor = 0 THEN
        #estado := FALSE;
    ELSE
        #estado := #estado_anterior;
    END_IF;
    ```
*   **Selección:**
    ```scl
    CASE #modo OF
        1: #accion := 10;
        2: #accion := 20;
    ELSE
        #accion := 0;
    END_CASE;
    ```
*   **Bucles:**
    ```scl
    FOR #i := 1 TO 10 BY 1 DO
        #suma := #suma + #array[#i];
    END_FOR;
    ```

## 4. Pasos seguidos en el Proyecto
Para cumplir con la solicitud del usuario, se han seguido los siguientes pasos:

1.  **Investigación Teórica:** Recopilación de información sobre el estándar IEC 61131-3 y la documentación técnica de Siemens para SCL.
2.  **Diseño de la Arquitectura:**
    *   **Backend:** Desarrollo de una API con FastAPI (Python) para procesar el código SCL y aplicar reglas de validación.
    *   **Dashboard/Frontend:** Creación de una interfaz moderna con React y Vite para la interacción del usuario.
    *   **Base de Datos:** Implementación de SQLite para almacenar programas generados y verificados.
3.  **Desarrollo del Validador:** Creación de un motor lógico que analiza la sintaxis (semicolons, bloques END_IF, etc.).
4.  **Generación de Plantillas:** Implementación de funciones para generar bloques de código base (FC/FB) automáticamente.
5.  **Documentación Final:** Generación de este reporte y el manual de uso del sistema.

---
*Este documento ha sido generado como parte de la solución integral para el sistema de generación y validación de programas SCL.*

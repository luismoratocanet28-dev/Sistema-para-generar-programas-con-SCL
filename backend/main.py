from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import datetime
import re

# Database Setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./scl_system.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    code = Column(Text)
    type = Column(String) # FC, FB, DB
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

# App Setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class CodeInput(BaseModel):
    code: str

class ProjectCreate(BaseModel):
    name: str
    code: str
    type: str

class PromptInput(BaseModel):
    prompt: str

# SCL Validation Logic
def validate_scl(code: str):
    errors = []
    lines = code.split('\n')
    
    # Check for semicolons
    for i, line in enumerate(lines):
        clean_line = line.strip()
        if not clean_line or clean_line.startswith('//') or clean_line.startswith('(*'):
            continue
            
        # Basic check for semicolon ending
        if not clean_line.endswith(';') and not clean_line.upper().startswith(('IF', 'CASE', 'FOR', 'WHILE', 'REPEAT', 'FUNCTION', 'DATA_BLOCK', 'ELSIF', 'ELSE', 'DO', 'THEN', 'OF')):
             # This is a very basic check, but works for common assignment errors
             if ':=' in clean_line:
                 errors.append({"line": i+1, "msg": "Falta punto y coma (;) al final de la instrucción."})
        
        # Check for wrong assignment operator (using = instead of :=)
        if '=' in clean_line and ':=' not in clean_line and not any(x in clean_line.upper() for x in ['IF', 'CASE', 'FOR', 'WHILE', 'UNTIL', 'VAR', 'CONST', 'END']):
            # This is a bit risky but common in SCL
            if re.search(r'\w+\s*=\s*\w+', clean_line):
                 errors.append({"line": i+1, "msg": "Posible error de sintaxis: Las asignaciones en SCL usan ':=' no '='."})

    # Check for unbalanced blocks
    blocks = {
        'IF': 'END_IF',
        'CASE': 'END_CASE',
        'FOR': 'END_FOR',
        'WHILE': 'END_WHILE',
        'REPEAT': 'UNTIL',
        'FUNCTION': 'END_FUNCTION',
        'FUNCTION_BLOCK': 'END_FUNCTION_BLOCK'
    }
    
    for start, end in blocks.items():
        starts = len(re.findall(rf'\b{start}\b', code, re.IGNORECASE))
        ends = len(re.findall(rf'\b{end}\b', code, re.IGNORECASE))
        if starts != ends:
            errors.append({"line": 0, "msg": f"Bloque {start} no está balanceado. Se encontraron {starts} aperturas y {ends} cierres."})

    return errors

# Endpoints
@app.post("/validate")
async def validate_code(input: CodeInput):
    errors = validate_scl(input.code)
    return {"valid": len(errors) == 0, "errors": errors}

@app.get("/generate/{type}")
async def generate_code(type: str):
    templates = {
        "motor": """// Bloque de control de Motor
FUNCTION_BLOCK "ControlMotor"
VAR_INPUT
    Start : BOOL;
    Stop : BOOL;
    Reset : BOOL;
END_VAR
VAR_OUTPUT
    Running : BOOL;
    Fault : BOOL;
END_VAR
VAR
    MotorState : BOOL;
END_VAR

BEGIN
    IF #Start AND NOT #Stop THEN
        #MotorState := TRUE;
    ELSIF #Stop OR #Fault THEN
        #MotorState := FALSE;
    END_IF;
    
    #Running := #MotorState;
END_FUNCTION_BLOCK""",
        "bucle": """// Ejemplo de bucle de suma
FUNCTION "SumArray" : VOID
VAR_INPUT
    Data : ARRAY[1..10] OF INT;
END_VAR
VAR_OUTPUT
    Result : INT;
END_VAR
VAR
    i : INT;
    temp_sum : INT;
END_VAR

BEGIN
    #temp_sum := 0;
    FOR #i := 1 TO 10 DO
        #temp_sum := #temp_sum + #Data[#i];
    END_FOR;
    #Result := #temp_sum;
END_FUNCTION""",
        "sensor": """// Escalado de sensor analógico
FUNCTION "ScaleSensor" : REAL
VAR_INPUT
    RawValue : INT;
    InMin : INT;
    InMax : INT;
    OutMin : REAL;
    OutMax : REAL;
END_VAR

BEGIN
    #ScaleSensor := (#RawValue - #InMin) * (#OutMax - #OutMin) / (#InMax - #InMin) + #OutMin;
END_FUNCTION"""
    }
    return {"code": templates.get(type, "// Template no encontrado")}

@app.post("/generate-ai")
async def generate_ai(input: PromptInput):
    p = input.prompt.lower()
    
    if "banda" in p or "conveyor" in p:
        code = """// Generado por prompt: Control de Banda Transportadora
FUNCTION_BLOCK "BandaControl"
VAR_INPUT
    Start : BOOL;
    Stop : BOOL;
    Sensor_Presencia : BOOL;
END_VAR
VAR_OUTPUT
    Motor_On : BOOL;
    Alarma : BOOL;
END_VAR
VAR
    timer_running : TON;
END_VAR

BEGIN
    IF #Start AND NOT #Stop THEN
        #Motor_On := TRUE;
    ELSIF #Stop OR NOT #Sensor_Presencia THEN
        #Motor_On := FALSE;
    END_IF;
    
    // Alarma si no hay presencia tras 5s
    #timer_running(IN:=#Motor_On AND NOT #Sensor_Presencia, PT:=T#5s);
    #Alarma := #timer_running.Q;
END_FUNCTION_BLOCK"""
    elif "tanque" in p or "nivel" in p:
        code = """// Generado por prompt: Control de Nivel de Tanque
FUNCTION_BLOCK "ControlNivel"
VAR_INPUT
    Nivel_Actual : REAL;
    Nivel_SetPoint : REAL;
    Histéresis : REAL;
END_VAR
VAR_OUTPUT
    Bomba_Llenado : BOOL;
END_VAR

BEGIN
    IF #Nivel_Actual < (#Nivel_SetPoint - #Histéresis) THEN
        #Bomba_Llenado := TRUE;
    ELSIF #Nivel_Actual > (#Nivel_SetPoint + #Histéresis) THEN
        #Bomba_Llenado := FALSE;
    END_IF;
END_FUNCTION_BLOCK"""
    elif "semaforo" in p or "luces" in p:
        code = """// Generado por prompt: Ciclo de Semáforo
FUNCTION_BLOCK "SemaforoControl"
VAR_INPUT
    Activar : BOOL;
END_VAR
VAR_OUTPUT
    Verde : BOOL;
    Ambar : BOOL;
    Rojo : BOOL;
END_VAR
VAR
    Paso : INT;
    Timer : TON;
END_VAR

BEGIN
    IF NOT #Activar THEN
        #Paso := 0;
    ELSIF #Paso = 0 THEN
        #Paso := 1;
    END_IF;

    CASE #Paso OF
        1: // Verde
            #Verde := TRUE; #Ambar := FALSE; #Rojo := FALSE;
            #Timer(IN:=TRUE, PT:=T#10s);
            IF #Timer.Q THEN #Paso := 2; #Timer(IN:=FALSE); END_IF;
        2: // Ambar
            #Verde := FALSE; #Ambar := TRUE; #Rojo := FALSE;
            #Timer(IN:=TRUE, PT:=T#3s);
            IF #Timer.Q THEN #Paso := 3; #Timer(IN:=FALSE); END_IF;
        3: // Rojo
            #Verde := FALSE; #Ambar := FALSE; #Rojo := TRUE;
            #Timer(IN:=TRUE, PT:=T#10s);
            IF #Timer.Q THEN #Paso := 1; #Timer(IN:=FALSE); END_IF;
    END_CASE;
END_FUNCTION_BLOCK"""
    else:
        code = f"""// Generado por prompt: {input.prompt}
// Nota: Plantilla genérica para su lógica personalizada
FUNCTION_BLOCK "Generado"
VAR_INPUT
    Entrada : BOOL;
END_VAR
VAR_OUTPUT
    Salida : BOOL;
END_VAR
BEGIN
    // Implementación basada en: {input.prompt}
    #Salida := #Entrada;
END_FUNCTION_BLOCK"""
    
    return {"code": code}

@app.get("/projects")
async def list_projects():
    db = SessionLocal()
    projects = db.query(Project).all()
    db.close()
    return projects

@app.post("/projects")
async def create_project(project: ProjectCreate):
    db = SessionLocal()
    db_project = Project(name=project.name, code=project.code, type=project.type)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    db.close()
    return db_project

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

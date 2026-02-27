import React, { useState, useEffect } from 'react'
import Editor from '@monaco-editor/react'
import axios from 'axios'
import {
  Play,
  Save,
  Terminal,
  CheckCircle2,
  AlertCircle,
  Plus,
  Cpu,
  Activity,
  Variable,
  FileCode,
  ArrowRight,
  Sparkles,
  Zap
} from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

const API_BASE = 'http://localhost:8000'

function App() {
  const [code, setCode] = useState('// Escribe tu código SCL aquí\nFUNCTION "MainBlock" : VOID\nBEGIN\n    \nEND_FUNCTION')
  const [results, setResults] = useState(null)
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(false)

  const [prompt, setPrompt] = useState('')

  useEffect(() => {
    fetchProjects()
  }, [])

  const fetchProjects = async () => {
    try {
      const res = await axios.get(`${API_BASE}/projects`)
      setProjects(res.data)
    } catch (err) {
      console.error("Error fetching projects", err)
    }
  }

  const handleValidate = async () => {
    setLoading(true)
    try {
      const res = await axios.post(`${API_BASE}/validate`, { code })
      setResults(res.data)
    } catch (err) {
      alert("Error al conectar con el servidor")
    } finally {
      setLoading(false)
    }
  }

  const handleGenerate = async (type) => {
    try {
      const res = await axios.get(`${API_BASE}/generate/${type}`)
      setCode(res.data.code)
      setResults(null)
    } catch (err) {
      alert("Error al generar código")
    }
  }

  const handleAIGenerate = async () => {
    if (!prompt) return
    setLoading(true)
    try {
      const res = await axios.post(`${API_BASE}/generate-ai`, { prompt })
      setCode(res.data.code)
      setResults(null)
      setPrompt('')
    } catch (err) {
      alert("Error en la generación por AI")
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    const name = prompt("Nombre del proyecto:")
    if (!name) return

    try {
      await axios.post(`${API_BASE}/projects`, {
        name,
        code,
        type: "SCL"
      })
      fetchProjects()
      alert("Proyecto guardado correctamente")
    } catch (err) {
      alert("Error al guardar")
    }
  }

  return (
    <div className="app-container">
      <header>
        <div className="logo-container">
          <Cpu size={32} color="#00a8ff" />
          <h1>Siemens SCL Studio</h1>
        </div>
        <div className="button-group">
          <button className="secondary" onClick={() => window.open('/docs/investigacion_iec61131.docx')}>
            <FileCode size={18} /> Ver Investigación
          </button>
          <button onClick={handleSave}>
            <Save size={18} /> Guardar Proyecto
          </button>
        </div>
      </header>

      <main className="main-layout">
        <section className="editor-section">
          <div className="editor-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Terminal size={18} color="#00a8ff" />
              <span style={{ fontWeight: 600 }}>Editor SCL IEC 61131-3</span>
            </div>
            <button onClick={handleValidate} disabled={loading}>
              {loading ? <Activity className="animate-spin" size={18} /> : <Play size={18} />}
              Comprobar Programa
            </button>
          </div>

          <div style={{ height: '600px', borderRadius: '12px', overflow: 'hidden', border: '1px solid rgba(255,255,255,0.05)' }}>
            <Editor
              height="100%"
              defaultLanguage="pascal" // Pascal is closest to SCL for highlighting
              theme="vs-dark"
              value={code}
              onChange={(value) => setCode(value)}
              options={{
                fontSize: 14,
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                lineNumbers: 'on',
                roundedSelection: true,
                padding: { top: 16 }
              }}
            />
          </div>
        </section>

        <aside className="sidebar">
          <div className="card" style={{ border: '1px solid var(--primary-glow)' }}>
            <h3><Sparkles size={18} color="#00a8ff" /> Generador AI</h3>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-dim)', marginBottom: '1rem' }}>
              Describe qué bloque necesitas (ej: "Banda transportadora", "Control de nivel").
            </p>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              <input
                type="text"
                placeholder="Ej: Control de tanque..."
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                style={{
                  background: 'rgba(255,255,255,0.05)',
                  border: '1px solid var(--border)',
                  borderRadius: '8px',
                  padding: '10px',
                  color: 'white',
                  outline: 'none'
                }}
              />
              <button onClick={handleAIGenerate} disabled={loading || !prompt}>
                {loading ? <Activity className="animate-spin" size={16} /> : <Zap size={16} />} Generar Código
              </button>
            </div>
          </div>

          <motion.div
            className="card"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <h3><Activity size={18} color="#00a8ff" /> Estado de Validación</h3>
            <AnimatePresence mode='wait'>
              {!results ? (
                <p style={{ color: 'var(--text-dim)', fontSize: '0.9rem' }}>
                  Pulsa "Comprobar Programa" para analizar la sintaxis.
                </p>
              ) : results.valid ? (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="status-badge status-valid"
                  style={{ display: 'flex', alignItems: 'center', gap: '8px' }}
                >
                  <CheckCircle2 size={16} /> Programa Válido
                </motion.div>
              ) : (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  <div className="status-badge status-invalid" style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <AlertCircle size={16} /> Errores Detectados
                  </div>
                  {results.errors.map((err, i) => (
                    <div key={i} className="result-item error-item">
                      {err.line > 0 && <span className="line-indicator">L{err.line}:</span>}
                      {err.msg}
                    </div>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>

          <div className="card">
            <h3><Plus size={18} color="#00a8ff" /> Generar Plantillas</h3>
            <div className="template-grid">
              <button className="secondary template-btn" onClick={() => handleGenerate('motor')}>
                <Cpu size={14} /> Control de Motor FB
              </button>
              <button className="secondary template-btn" onClick={() => handleGenerate('bucle')}>
                <Activity size={14} /> Suma Array con Bucle FOR
              </button>
              <button className="secondary template-btn" onClick={() => handleGenerate('sensor')}>
                <Variable size={14} /> Escalado Analógico FC
              </button>
            </div>
          </div>

          <div className="card">
            <h3><Save size={18} color="#00a8ff" /> Proyectos Guardados</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {projects.length === 0 ? (
                <p style={{ color: 'var(--text-dim)', fontSize: '0.85rem' }}>No hay proyectos guardados.</p>
              ) : (
                projects.map((p) => (
                  <div key={p.id} className="result-item" style={{ cursor: 'pointer', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }} onClick={() => setCode(p.code)}>
                    <span>{p.name}</span>
                    <ArrowRight size={14} />
                  </div>
                ))
              )}
            </div>
          </div>
        </aside>
      </main>
    </div>
  )
}

export default App

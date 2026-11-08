/**
 * Ágora Colombia — Aplicación React 18
 * Frontend de Alto Rendimiento, Inteligencia Ciudadana y Análisis de Sentimiento con IA
 */

const { useState, useEffect, useMemo, useRef, useCallback } = React;

// =========================================================
// 1. SISTEMA DE ICONOS VECTORIALES (Inline SVG para Cero Latencia)
// =========================================================
const Icons = {
  MessageSquare: ({ className = "w-4 h-4" }) => (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
    </svg>
  ),
  BarChart: ({ className = "w-4 h-4" }) => (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
    </svg>
  ),
  Flask: ({ className = "w-4 h-4" }) => (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
    </svg>
  ),
  CheckCircle: ({ className = "w-4 h-4" }) => (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  ),
  AlertCircle: ({ className = "w-4 h-4" }) => (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  ),
  Scale: ({ className = "w-4 h-4" }) => (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
    </svg>
  ),
  Sparkles: ({ className = "w-4 h-4" }) => (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
    </svg>
  ),
  Search: ({ className = "w-4 h-4" }) => (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
    </svg>
  ),
  Send: ({ className = "w-4 h-4" }) => (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
    </svg>
  ),
  Download: ({ className = "w-4 h-4" }) => (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
    </svg>
  ),
  Edit: ({ className = "w-4 h-4" }) => (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
    </svg>
  ),
  ShieldCheck: ({ className = "w-4 h-4" }) => (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
    </svg>
  ),
  Refresh: ({ className = "w-4 h-4" }) => (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
    </svg>
  ),
  X: ({ className = "w-4 h-4" }) => (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
    </svg>
  )
};

// =========================================================
// 2. BADGE DE SENTIMIENTO CON ESTILO IMPECCABLE
// =========================================================
function SentimentBadge({ sentimiento, size = "md" }) {
  const configs = {
    positivo: {
      label: "Positivo",
      icon: Icons.CheckCircle,
      bg: "bg-emeraldNeon/10",
      text: "text-emeraldNeon",
      border: "border-emeraldNeon/30",
      glow: "shadow-[0_0_12px_rgba(16,185,129,0.2)]"
    },
    negativo: {
      label: "Negativo",
      icon: Icons.AlertCircle,
      bg: "bg-crimsonNeon/10",
      text: "text-crimsonNeon",
      border: "border-crimsonNeon/30",
      glow: "shadow-[0_0_12px_rgba(239,68,68,0.2)]"
    },
    neutro: {
      label: "Neutro / Fáctico",
      icon: Icons.Scale,
      bg: "bg-slate-500/10",
      text: "text-slate-300",
      border: "border-slate-500/30",
      glow: ""
    },
    mixto: {
      label: "Mixto",
      icon: Icons.Sparkles,
      bg: "bg-amberNeon/10",
      text: "text-amberNeon",
      border: "border-amberNeon/30",
      glow: "shadow-[0_0_12px_rgba(245,158,11,0.2)]"
    }
  };

  const config = configs[sentimiento] || configs.neutro;
  const IconComponent = config.icon;
  const sizeClasses = size === "sm" ? "px-2 py-0.5 text-[11px]" : "px-2.5 py-1 text-xs";

  return (
    <span className={`inline-flex items-center gap-1.5 font-semibold rounded-full border ${config.bg} ${config.text} ${config.border} ${config.glow} ${sizeClasses} font-sans`}>
      <IconComponent className="w-3.5 h-3.5 shrink-0" />
      <span>{config.label}</span>
    </span>
  );
}

// =========================================================
// 3. COMPONENTE PRINCIPAL: APLICACIÓN ÁGORA COLOMBIA
// =========================================================
function App() {
  const [tab, setTab] = useState("chat"); // 'chat' | 'dashboard' | 'lab'
  const [catalogo, setCatalogo] = useState([]);
  const [politicoActivo, setPoliticoActivo] = useState(null);
  const [opiniones, setOpiniones] = useState([]);
  const [metricas, setMetricas] = useState({ total: 0, positivo: 0, negativo: 0, neutro: 0, mixto: 0 });
  const [busquedaPolitico, setBusquedaPolitico] = useState("");

  // Estado del formulario de chat
  const [textoOpinion, setTextoOpinion] = useState("");
  const [enviando, setEnviando] = useState(false);
  const [modoBenchmarking, setModoBenchmarking] = useState(false);
  const [chatFeed, setChatFeed] = useState([]);

  // Filtros de Auditoría
  const [filtroPoliticoId, setFiltroPoliticoId] = useState("todos");
  const [filtroSentimiento, setFiltroSentimiento] = useState("todos");
  const [filtroPalabraClave, setFiltroPalabraClave] = useState("");

  // Modal de Auditoría Humana (Human-in-the-Loop)
  const [modalOpinion, setModalOpinion] = useState(null);
  const [nuevoSentimiento, setNuevoSentimiento] = useState("positivo");
  const [justificacionCorreccion, setJustificacionCorreccion] = useState("");
  const [guardandoCorreccion, setGuardandoCorreccion] = useState(false);

  // Benchmarking Lab dedicado
  const [labPoliticoId, setLabPoliticoId] = useState("");
  const [labTexto, setLabTexto] = useState("");
  const [labResultado, setLabResultado] = useState(null);
  const [labCargando, setLabCargando] = useState(false);

  // Notificaciones Toast
  const [toast, setToast] = useState(null);

  const feedEndRef = useRef(null);

  const mostrarToast = useCallback((mensaje, tipo = "info") => {
    setToast({ mensaje, tipo });
    setTimeout(() => setToast(null), 4000);
  }, []);

  // Cargar Catálogo Oficial de Presidentes y Líderes
  useEffect(() => {
    async function cargarCatalogo() {
      try {
        const res = await fetch("/api/politicos");
        if (!res.ok) throw new Error("Error al consultar catálogo");
        const data = await res.json();
        setCatalogo(data.politicos || []);
        if (data.politicos && data.politicos.length > 0) {
          setPoliticoActivo(data.politicos[0]);
          setLabPoliticoId(data.politicos[0].id);
        }
      } catch (err) {
        mostrarToast("Fallo al conectar con el catálogo de mandatarios: " + err.message, "error");
      }
    }
    cargarCatalogo();
  }, [mostrarToast]);

  // Cargar Opiniones Persistidas y Métricas
  const refrescarOpiniones = useCallback(async () => {
    try {
      let url = `/api/opiniones?politico_id=${filtroPoliticoId}&sentimiento=${filtroSentimiento}`;
      if (filtroPalabraClave.trim()) {
        url += `&q=${encodeURIComponent(filtroPalabraClave.trim())}`;
      }
      const res = await fetch(url);
      if (!res.ok) throw new Error("Error al obtener opiniones");
      const data = await res.json();
      setOpiniones(data.opiniones || []);
      setMetricas(data.metricas || { total: 0, positivo: 0, negativo: 0, neutro: 0, mixto: 0 });
    } catch (err) {
      console.error("Fallo al actualizar telemetría:", err);
    }
  }, [filtroPoliticoId, filtroSentimiento, filtroPalabraClave]);

  useEffect(() => {
    refrescarOpiniones();
  }, [refrescarOpiniones]);

  // Desplazamiento automático al final del chat
  useEffect(() => {
    if (tab === "chat" && feedEndRef.current) {
      feedEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [chatFeed, tab]);

  // Filtrado de lista lateral de presidentes
  const politicosFiltrados = useMemo(() => {
    if (!busquedaPolitico.trim()) return catalogo;
    const q = busquedaPolitico.toLowerCase();
    return catalogo.filter(p =>
      p.nombre.toLowerCase().includes(q) ||
      (p.rol && p.rol.toLowerCase().includes(q)) ||
      p.id.toLowerCase().includes(q)
    );
  }, [catalogo, busquedaPolitico]);

  // Conteo de opiniones por político para el sidebar
  const conteoPorPolitico = useMemo(() => {
    const mapa = {};
    opiniones.forEach(op => {
      const id = op.jugador_id;
      mapa[id] = (mapa[id] || 0) + 1;
    });
    return mapa;
  }, [opiniones]);

  // Manejo de envío de opinión con Inferencia IA
  const handleEnviarOpinion = async (e) => {
    if (e) e.preventDefault();
    if (!politicoActivo) return;

    const textoLimpio = textoOpinion.trim();
    if (textoLimpio.length < 5) {
      mostrarToast("La opinión debe tener al menos 5 caracteres.", "error");
      return;
    }
    if (textoLimpio.length > 1000) {
      mostrarToast("La opinión excede el límite máximo de 1000 caracteres.", "error");
      return;
    }

    setEnviando(true);

    // Agregar mensaje del usuario al feed visual
    const userMsg = {
      tipo: "user",
      autor: "Ciudadano",
      politico: politicoActivo.nombre,
      texto: textoLimpio,
      fecha: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    setChatFeed(prev => [...prev, userMsg]);
    setTextoOpinion("");

    try {
      if (modoBenchmarking) {
        // Ejecutar inferencia dual (Benchmarking)
        const resDual = await fetch("/api/opiniones/comparar", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            politico_id: politicoActivo.id,
            opinion: textoLimpio
          })
        });
        const dataDual = await resDual.json();

        // Registrar también en persistencia atómica estándar
        const resPersist = await fetch("/api/opiniones", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ politico_id: politicoActivo.id, opinion: textoLimpio })
        });
        const dataPersist = await resPersist.json();

        const aiMsg = {
          tipo: "ai",
          esPertinente: dataPersist.es_pertinente,
          sentimiento: dataPersist.sentimiento,
          razon: dataPersist.razon,
          guardado: dataPersist.guardado,
          benchmarking: dataDual,
          fecha: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };
        setChatFeed(prev => [...prev, aiMsg]);

        if (dataPersist.sentimiento === "positivo" && window.confetti) {
          window.confetti({ particleCount: 50, spread: 60, origin: { y: 0.8 } });
        }
      } else {
        // Inferencia normal con persistencia
        const res = await fetch("/api/opiniones", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            politico_id: politicoActivo.id,
            opinion: textoLimpio
          })
        });

        if (!res.ok) {
          const errData = await res.json();
          throw new Error(errData.detail || "Fallo en la inferencia");
        }

        const data = await res.json();
        const aiMsg = {
          tipo: "ai",
          esPertinente: data.es_pertinente,
          sentimiento: data.sentimiento,
          razon: data.razon,
          guardado: data.guardado,
          fecha: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };
        setChatFeed(prev => [...prev, aiMsg]);

        if (data.sentimiento === "positivo" && window.confetti) {
          window.confetti({ particleCount: 60, spread: 70, origin: { y: 0.8 } });
        }
      }

      refrescarOpiniones();
    } catch (err) {
      mostrarToast("Error en inferencia: " + err.message, "error");
      // Restaurar el texto en el textarea para que el usuario no pierda lo escrito
      setTextoOpinion(textoLimpio);
    } finally {
      setEnviando(false);
    }
  };

  // Manejo de Human-in-the-Loop (Reclasificación Manual)
  const handleGuardarCorreccion = async () => {
    if (!modalOpinion) return;
    setGuardandoCorreccion(true);

    try {
      const res = await fetch(`/api/opiniones/${modalOpinion.id}/corregir`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          nuevo_sentimiento: nuevoSentimiento,
          justificacion: justificacionCorreccion.trim()
        })
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Error al actualizar");
      }

      mostrarToast("¡Reclasificación guardada con éxito! Registro auditado.", "success");
      setModalOpinion(null);
      setJustificacionCorreccion("");
      refrescarOpiniones();
    } catch (err) {
      mostrarToast("Fallo al guardar auditoría: " + err.message, "error");
    } finally {
      setGuardandoCorreccion(false);
    }
  };

  // Ejecutar prueba de Benchmarking en el Laboratorio
  const handleEjecutarLab = async () => {
    if (!labTexto.trim() || labTexto.trim().length < 5) {
      mostrarToast("Ingresa al menos 5 caracteres para contrastar modelos.", "error");
      return;
    }
    setLabCargando(true);
    setLabResultado(null);

    try {
      const res = await fetch("/api/opiniones/comparar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          politico_id: labPoliticoId,
          opinion: labTexto.trim()
        })
      });
      if (!res.ok) throw new Error("Fallo en la prueba dual");
      const data = await res.json();
      setLabResultado(data);
    } catch (err) {
      mostrarToast("Error en prueba de laboratorio: " + err.message, "error");
    } finally {
      setLabCargando(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-pitch text-slate-100">

      {/* ========================================================= */}
      {/* HEADER SUPERIOR IMPECCABLE */}
      {/* ========================================================= */}
      <header className="sticky top-0 z-40 glass-surface border-b border-white/10 px-6 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3.5">
          <div className="w-10 h-10 rounded-xl bg-emeraldNeon/10 border border-emeraldNeon/30 flex items-center justify-center text-xl shadow-[0_0_15px_rgba(16,185,129,0.25)]">
            🇨🇴
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-outfit font-extrabold text-xl text-white tracking-tight">Ágora Colombia</span>
              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emeraldNeon/10 text-emeraldNeon border border-emeraldNeon/30 font-mono">
                REACT 18 SPA
              </span>
            </div>
            <p className="text-xs text-slate-400 font-sans hidden sm:block">
              Barómetro de Percepción sobre Presidentes & Liderazgo Político
            </p>
          </div>
        </div>

        {/* NAVEGACIÓN SEGMENTADA */}
        <nav className="flex items-center bg-pitch/80 p-1 rounded-xl border border-white/10 text-xs font-semibold">
          <button
            onClick={() => setTab("chat")}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg transition-all ${
              tab === "chat"
                ? "bg-surfaceElevated text-emeraldNeon border border-emeraldNeon/40 shadow-glow-emerald"
                : "text-slate-400 hover:text-white"
            }`}
          >
            <Icons.MessageSquare className="w-3.5 h-3.5" />
            <span>Tribuna de Opinión</span>
          </button>

          <button
            onClick={() => setTab("dashboard")}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg transition-all ${
              tab === "dashboard"
                ? "bg-surfaceElevated text-cyanNeon border border-cyanNeon/40 shadow-glow-cyan"
                : "text-slate-400 hover:text-white"
            }`}
          >
            <Icons.BarChart className="w-3.5 h-3.5" />
            <span>Barómetro & Métricas</span>
          </button>

          <button
            onClick={() => setTab("lab")}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg transition-all ${
              tab === "lab"
                ? "bg-surfaceElevated text-amberNeon border border-amberNeon/40 shadow-[0_0_15px_rgba(245,158,11,0.25)]"
                : "text-slate-400 hover:text-white"
            }`}
          >
            <Icons.Flask className="w-3.5 h-3.5" />
            <span>Lab Benchmarking</span>
          </button>
        </nav>

        {/* INDICADOR DE TELEMETRÍA */}
        <div className="hidden lg:flex items-center gap-3 text-xs font-mono">
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-pitch/60 border border-white/10">
            <span className="w-2 h-2 rounded-full bg-emeraldNeon animate-pulse"></span>
            <span className="text-slate-300">Gemini 2.5 Flash Activo</span>
          </div>
        </div>
      </header>

      {/* ========================================================= */}
      {/* CUERPO PRINCIPAL CON SIDEBAR & VISTAS */}
      {/* ========================================================= */}
      <div className="flex-1 flex flex-col md:flex-row h-[calc(100vh-65px)] overflow-hidden">

        {/* BARRA LATERAL: CATÁLOGO DE MANDATARIOS */}
        <aside className="w-full md:w-80 glass-surface border-r border-white/10 flex flex-col shrink-0 overflow-hidden">
          <div className="p-4 border-b border-white/10">
            <div className="flex items-center justify-between mb-2.5">
              <span className="font-outfit font-bold text-sm text-slate-200">Mandatarios & Líderes</span>
              <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-cyanNeon/10 text-cyanNeon border border-cyanNeon/30">
                20 Figuras
              </span>
            </div>

            {/* Buscador de políticos */}
            <div className="relative">
              <Icons.Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-slate-500" />
              <input
                type="text"
                value={busquedaPolitico}
                onChange={(e) => setBusquedaPolitico(e.target.value)}
                placeholder="Buscar presidente o líder..."
                className="w-full bg-pitch/90 border border-white/10 rounded-lg pl-8 pr-3 py-1.5 text-xs text-slate-200 placeholder:text-slate-500 focus:outline-none focus:border-cyanNeon transition-colors"
              />
              {busquedaPolitico && (
                <button
                  onClick={() => setBusquedaPolitico("")}
                  className="absolute right-2.5 top-2 text-slate-500 hover:text-slate-300"
                >
                  <Icons.X className="w-3.5 h-3.5" />
                </button>
              )}
            </div>
          </div>

          {/* Lista scrolleable de candidatos */}
          <div className="flex-1 overflow-y-auto custom-scroll p-3 space-y-1.5">
            {politicosFiltrados.map((p) => {
              const activo = politicoActivo && politicoActivo.id === p.id;
              const count = conteoPorPolitico[p.id] || 0;

              return (
                <button
                  key={p.id}
                  onClick={() => setPoliticoActivo(p)}
                  className={`w-full text-left p-2.5 rounded-xl border transition-all flex items-center justify-between ${
                    activo
                      ? "bg-surfaceElevated border-emeraldNeon/40 shadow-glow-emerald"
                      : "bg-surface/50 border-white/5 hover:border-white/15 hover:bg-surface"
                  }`}
                >
                  <div className="min-w-0 pr-2">
                    <div className="flex items-center gap-1.5">
                      <span className="text-xs">🇨🇴</span>
                      <p className={`text-xs font-bold truncate ${activo ? "text-emeraldNeon" : "text-slate-200"}`}>
                        {p.nombre}
                      </p>
                    </div>
                    <p className="text-[10px] text-slate-400 truncate mt-0.5 font-sans">
                      {p.rol || "Presidente de Colombia"}
                    </p>
                  </div>

                  <span className={`text-[10px] font-mono px-2 py-0.5 rounded-full shrink-0 ${
                    count > 0 ? "bg-white/10 text-white" : "text-slate-500"
                  }`}>
                    {count} {count === 1 ? "op." : "ops."}
                  </span>
                </button>
              );
            })}
          </div>

          {/* Footer de la barra lateral */}
          <div className="p-3 border-t border-white/10 bg-pitch/40 text-[11px] font-mono text-slate-400 flex items-center justify-between">
            <span>Persistencia Atómica:</span>
            <span className="text-emeraldNeon flex items-center gap-1">
              <Icons.ShieldCheck className="w-3.5 h-3.5" /> opiniones.json
            </span>
          </div>
        </aside>

        {/* CONTENIDO PRINCIPAL POR PESTAÑA */}
        <main className="flex-1 flex flex-col overflow-hidden bg-pitch/40">

          {/* ========================================================= */}
          {/* VISTA 1: TRIBUNA DE OPINIÓN & CHAT CON LANGCHAIN */}
          {/* ========================================================= */}
          {tab === "chat" && (
            <div className="flex-1 flex flex-col h-full overflow-hidden">

              {/* Banner del mandatario seleccionado */}
              {politicoActivo && (
                <div className="px-6 py-3.5 glass-surface border-b border-white/10 flex items-center justify-between shrink-0">
                  <div className="flex items-center gap-3">
                    <div className="w-11 h-11 rounded-xl bg-pitch border border-cyanNeon/30 flex items-center justify-center text-xl shadow-[0_0_15px_rgba(6,182,212,0.15)]">
                      🇨🇴
                    </div>
                    <div>
                      <span className="text-[10px] font-mono uppercase tracking-wider text-cyanNeon font-bold">
                        Mandatario Activo • ID: {politicoActivo.id}
                      </span>
                      <h2 className="font-outfit font-extrabold text-lg text-white leading-tight">
                        {politicoActivo.nombre}
                      </h2>
                      <p className="text-xs text-slate-400 font-sans">
                        {politicoActivo.rol || "Figura de Estado"}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <label className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-surface border border-white/10 text-xs font-mono cursor-pointer hover:border-amberNeon/40 transition-colors">
                      <input
                        type="checkbox"
                        checked={modoBenchmarking}
                        onChange={(e) => setModoBenchmarking(e.target.checked)}
                        className="rounded text-amberNeon focus:ring-0"
                      />
                      <span className="text-amberNeon font-bold">🔬 Modo Dual (Sección 12)</span>
                    </label>
                  </div>
                </div>
              )}

              {/* Feed de conversación */}
              <div className="flex-1 overflow-y-auto custom-scroll p-6 space-y-4">
                {chatFeed.length === 0 && (
                  <div className="glass-surface rounded-2xl p-6 border border-white/10 max-w-2xl mx-auto text-center mt-6">
                    <div className="w-12 h-12 rounded-2xl bg-cyanNeon/10 border border-cyanNeon/30 flex items-center justify-center text-cyanNeon mx-auto mb-3">
                      <Icons.MessageSquare className="w-6 h-6" />
                    </div>
                    <h3 className="font-outfit font-bold text-base text-white">Tribuna de Opinión Ciudadana</h3>
                    <p className="text-xs text-slate-300 mt-1.5 leading-relaxed max-w-md mx-auto">
                      Expresa tu evaluación sobre <strong>{politicoActivo?.nombre}</strong> (5 a 1000 caracteres). El sistema analizará objetivamente el sentimiento con Google Gemini, previniendo inyecciones de instrucciones y persistiendo atómicamente en disco.
                    </p>
                  </div>
                )}

                {chatFeed.map((msg, idx) => (
                  <div key={idx} className="animate-fadeIn">
                    {msg.tipo === "user" ? (
                      <div className="glass-surface-elevated rounded-2xl p-4 border border-cyanNeon/20 max-w-3xl ml-auto">
                        <div className="flex justify-between items-center mb-1 text-xs">
                          <span className="font-semibold text-cyanNeon">👤 Opinión Ciudadana sobre {msg.politico}</span>
                          <span className="font-mono text-[10px] text-slate-400">{msg.fecha}</span>
                        </div>
                        <p className="text-sm text-slate-100 italic leading-relaxed">
                          “{msg.texto}”
                        </p>
                      </div>
                    ) : (
                      <div className={`glass-surface rounded-2xl p-4 border max-w-3xl mr-auto ${
                        msg.esPertinente ? "border-emeraldNeon/20" : "border-crimsonNeon/30"
                      }`}>
                        <div className="flex justify-between items-center mb-2.5">
                          <span className="font-outfit font-bold text-xs text-emeraldNeon flex items-center gap-1.5">
                            <Icons.ShieldCheck className="w-4 h-4" /> Clasificación de Inferencia AI
                          </span>
                          {msg.esPertinente ? (
                            <SentimentBadge sentimiento={msg.sentimiento} />
                          ) : (
                            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-crimsonNeon/10 text-crimsonNeon border border-crimsonNeon/30">
                              No Pertinente
                            </span>
                          )}
                        </div>

                        {/* Justificación del modelo */}
                        <div className="bg-pitch/60 rounded-xl p-3 border border-white/5 text-xs text-slate-200">
                          <span className="text-[10px] font-mono uppercase text-slate-400 font-bold block mb-1">
                            Fundamentación Técnica (Tercera Persona):
                          </span>
                          <p className="leading-relaxed">{msg.razon}</p>
                        </div>

                        {/* Panel de Benchmarking Dual si fue activado */}
                        {msg.benchmarking && (
                          <div className="mt-3 p-3 rounded-xl bg-amberNeon/5 border border-amberNeon/25 text-xs font-mono">
                            <div className="flex items-center justify-between mb-1.5">
                              <span className="text-amberNeon font-bold flex items-center gap-1">
                                <Icons.Flask className="w-3.5 h-3.5" /> Benchmarking Dual (Sección 12):
                              </span>
                              <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                                msg.benchmarking.consenso
                                  ? "bg-emeraldNeon/10 text-emeraldNeon border border-emeraldNeon/30"
                                  : "bg-amberNeon/10 text-amberNeon border border-amberNeon/30"
                              }`}>
                                {msg.benchmarking.consenso ? "🟢 Consenso Total" : "🟡 Discrepancia"}
                              </span>
                            </div>
                            <div className="grid grid-cols-2 gap-2 text-[11px] text-slate-300">
                              <div>• {msg.benchmarking.modelo_a}: <code className="text-emeraldNeon">{msg.benchmarking.sentimiento_a}</code></div>
                              <div>• {msg.benchmarking.modelo_b}: <code className="text-cyanNeon">{msg.benchmarking.sentimiento_b}</code></div>
                            </div>
                          </div>
                        )}

                        <div className="flex justify-between items-center text-[10px] font-mono text-slate-500 mt-2.5 pt-2 border-t border-white/5">
                          <span>{msg.guardado ? "💾 Persistido atómicamente en opiniones.json" : "⚠️ Registro omitido"}</span>
                          <span>{msg.fecha}</span>
                        </div>
                      </div>
                    )}
                  </div>
                ))}
                <div ref={feedEndRef} />
              </div>

              {/* Formulario de entrada con medidor de longitud */}
              <div className="p-4 glass-surface border-t border-white/10 shrink-0">
                <form onSubmit={handleEnviarOpinion} className="max-w-4xl mx-auto">
                  <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
                    <span className="font-sans">Escribe tu opinión objetiva, crítica o elogio:</span>
                    <span className={`font-mono font-bold text-xs ${
                      textoOpinion.trim().length >= 5 && textoOpinion.trim().length <= 1000
                        ? "text-emeraldNeon"
                        : "text-slate-500"
                    }`}>
                      {textoOpinion.trim().length} / 1000 caracteres (Mín. 5)
                    </span>
                  </div>

                  <div className="relative">
                    <textarea
                      value={textoOpinion}
                      onChange={(e) => setTextoOpinion(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === "Enter" && !e.shiftKey) {
                          e.preventDefault();
                          handleEnviarOpinion();
                        }
                      }}
                      disabled={enviando}
                      rows="2"
                      placeholder={`Opina sobre las políticas, trayectoria o liderazgo de ${politicoActivo?.nombre}... (Presiona Enter para enviar)`}
                      className="w-full bg-pitch/90 border border-white/15 rounded-xl px-4 py-3 text-xs text-slate-100 placeholder:text-slate-500 focus:outline-none focus:border-emeraldNeon custom-scroll resize-none transition-colors"
                    />

                    <button
                      type="submit"
                      disabled={enviando || textoOpinion.trim().length < 5}
                      className="absolute right-3 bottom-3.5 px-4 py-2 rounded-lg bg-emeraldNeon hover:bg-emeraldGlow text-pitch font-bold text-xs flex items-center gap-1.5 transition-all shadow-glow-emerald disabled:opacity-40 disabled:pointer-events-none"
                    >
                      {enviando ? (
                        <>
                          <Icons.Refresh className="w-3.5 h-3.5 animate-spin" />
                          <span>Analizando...</span>
                        </>
                      ) : (
                        <>
                          <Icons.Send className="w-3.5 h-3.5" />
                          <span>Enviar</span>
                        </>
                      )}
                    </button>
                  </div>
                </form>
              </div>

            </div>
          )}

          {/* ========================================================= */}
          {/* VISTA 2: BARÓMETRO ANALÍTICO & AUDITORÍA EN TIEMPO REAL   */}
          {/* ========================================================= */}
          {tab === "dashboard" && (
            <div className="flex-1 overflow-y-auto custom-scroll p-6 space-y-6">

              {/* Encabezado del Barómetro */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <h2 className="font-outfit font-extrabold text-2xl text-white">Barómetro de Percepción Ciudadana</h2>
                  <p className="text-xs text-slate-400 font-sans mt-0.5">
                    Telemetría en memoria sincronizada • Cero consumo de tokens en consultas analíticas
                  </p>
                </div>

                <button
                  onClick={() => {
                    const url = `/api/exportar?politico_id=${filtroPoliticoId}&sentimiento=${filtroSentimiento}`;
                    window.location.href = url;
                  }}
                  className="px-4 py-2 rounded-xl bg-cyanNeon/10 hover:bg-cyanNeon/20 text-cyanNeon border border-cyanNeon/30 text-xs font-bold font-sans flex items-center gap-2 transition-all shadow-glow-cyan shrink-0"
                >
                  <Icons.Download className="w-4 h-4" />
                  <span>Descargar Telemetría (JSON)</span>
                </button>
              </div>

              {/* 5 Tarjetas KPI */}
              <div className="grid grid-cols-2 sm:grid-cols-5 gap-3.5">
                <div className="glass-surface rounded-xl p-4 border border-white/10">
                  <span className="text-[10px] uppercase font-mono text-slate-400 font-bold block">Total Base</span>
                  <div className="font-outfit font-extrabold text-2xl text-white mt-1 tabular-nums">
                    {metricas.total}
                  </div>
                  <span className="text-[10px] text-slate-500 font-sans">Opiniones filtradas</span>
                </div>

                <div className="glass-surface rounded-xl p-4 border border-emeraldNeon/30 shadow-[0_0_15px_rgba(16,185,129,0.1)]">
                  <span className="text-[10px] uppercase font-mono text-emeraldNeon font-bold block">🟢 Positivas</span>
                  <div className="font-outfit font-extrabold text-2xl text-emeraldNeon mt-1 tabular-nums">
                    {metricas.positivo}
                  </div>
                  <span className="text-[10px] text-emeraldNeon/70 font-sans">
                    {metricas.total > 0 ? ((metricas.positivo / metricas.total) * 100).toFixed(0) : 0}% del total
                  </span>
                </div>

                <div className="glass-surface rounded-xl p-4 border border-crimsonNeon/30 shadow-[0_0_15px_rgba(239,68,68,0.1)]">
                  <span className="text-[10px] uppercase font-mono text-crimsonNeon font-bold block">🔴 Negativas</span>
                  <div className="font-outfit font-extrabold text-2xl text-crimsonNeon mt-1 tabular-nums">
                    {metricas.negativo}
                  </div>
                  <span className="text-[10px] text-crimsonNeon/70 font-sans">
                    {metricas.total > 0 ? ((metricas.negativo / metricas.total) * 100).toFixed(0) : 0}% del total
                  </span>
                </div>

                <div className="glass-surface rounded-xl p-4 border border-slate-500/30">
                  <span className="text-[10px] uppercase font-mono text-slate-400 font-bold block">⚪ Neutras</span>
                  <div className="font-outfit font-extrabold text-2xl text-slate-300 mt-1 tabular-nums">
                    {metricas.neutro}
                  </div>
                  <span className="text-[10px] text-slate-400 font-sans">
                    {metricas.total > 0 ? ((metricas.neutro / metricas.total) * 100).toFixed(0) : 0}% del total
                  </span>
                </div>

                <div className="glass-surface rounded-xl p-4 border border-amberNeon/30 shadow-[0_0_15px_rgba(245,158,11,0.1)]">
                  <span className="text-[10px] uppercase font-mono text-amberNeon font-bold block">🟡 Mixtas</span>
                  <div className="font-outfit font-extrabold text-2xl text-amberNeon mt-1 tabular-nums">
                    {metricas.mixto}
                  </div>
                  <span className="text-[10px] text-amberNeon/70 font-sans">
                    {metricas.total > 0 ? ((metricas.mixto / metricas.total) * 100).toFixed(0) : 0}% del total
                  </span>
                </div>
              </div>

              {/* Barra de Filtros y Búsqueda Libre (Mejora 4) */}
              <div className="glass-surface rounded-xl p-4 border border-white/10 flex flex-wrap items-center gap-3">
                <div className="flex-1 min-w-[200px]">
                  <label className="block text-[10px] font-mono text-slate-400 mb-1 uppercase font-bold">
                    Filtrar por Mandatario:
                  </label>
                  <select
                    value={filtroPoliticoId}
                    onChange={(e) => setFiltroPoliticoId(e.target.value)}
                    className="w-full bg-pitch border border-white/15 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-cyanNeon"
                  >
                    <option value="todos">Todos los Mandatarios</option>
                    {catalogo.map(p => (
                      <option key={p.id} value={p.id}>{p.nombre}</option>
                    ))}
                  </select>
                </div>

                <div className="min-w-[160px]">
                  <label className="block text-[10px] font-mono text-slate-400 mb-1 uppercase font-bold">
                    Filtrar por Sentimiento:
                  </label>
                  <select
                    value={filtroSentimiento}
                    onChange={(e) => setFiltroSentimiento(e.target.value)}
                    className="w-full bg-pitch border border-white/15 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-cyanNeon"
                  >
                    <option value="todos">Todos los Sentimientos</option>
                    <option value="positivo">🟢 Positivo</option>
                    <option value="negativo">🔴 Negativo</option>
                    <option value="neutro">⚪ Neutro</option>
                    <option value="mixto">🟡 Mixto</option>
                  </select>
                </div>

                <div className="flex-1 min-w-[240px]">
                  <label className="block text-[10px] font-mono text-slate-400 mb-1 uppercase font-bold">
                    Búsqueda por Palabra Clave:
                  </label>
                  <div className="relative">
                    <Icons.Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-slate-500" />
                    <input
                      type="text"
                      value={filtroPalabraClave}
                      onChange={(e) => setFiltroPalabraClave(e.target.value)}
                      placeholder="Ej: paz, reforma, seguridad, economía..."
                      className="w-full bg-pitch border border-white/15 rounded-lg pl-8 pr-3 py-1.5 text-xs text-slate-200 placeholder:text-slate-500 focus:outline-none focus:border-cyanNeon"
                    />
                  </div>
                </div>
              </div>

              {/* Tabla de Auditoría & Human-in-the-Loop */}
              <div className="glass-surface rounded-xl border border-white/10 overflow-hidden">
                <div className="px-5 py-3 border-b border-white/10 flex items-center justify-between">
                  <span className="font-outfit font-bold text-sm text-slate-200">
                    Registros Persistidos ({opiniones.length})
                  </span>
                  <span className="text-[11px] font-mono text-emeraldNeon">
                    Preservación Atómica Garantizada
                  </span>
                </div>

                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs font-sans">
                    <thead className="bg-pitch/80 text-slate-400 uppercase tracking-wider font-mono border-b border-white/10 text-[10px]">
                      <tr>
                        <th className="py-3 px-4">Fecha (UTC)</th>
                        <th className="py-3 px-4">Mandatario</th>
                        <th className="py-3 px-4">Opinión Ciudadana</th>
                        <th className="py-3 px-4">Sentimiento</th>
                        <th className="py-3 px-4">Justificación IA</th>
                        <th className="py-3 px-4 text-center">Auditoría Humana</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-white/5 text-slate-200">
                      {opiniones.length === 0 ? (
                        <tr>
                          <td colSpan="6" className="py-8 text-center text-slate-500 font-sans">
                            No se encontraron registros que coincidan con los filtros seleccionados.
                          </td>
                        </tr>
                      ) : (
                        opiniones.slice().reverse().map((op) => (
                          <tr key={op.id} className="hover:bg-surfaceElevated/40 transition-colors">
                            <td className="py-3 px-4 font-mono text-[11px] text-slate-400 whitespace-nowrap">
                              {(op.fecha_utc || "").slice(0, 19).replace("T", " ")}
                            </td>
                            <td className="py-3 px-4 font-bold text-white whitespace-nowrap">
                              {op.jugador_nombre}
                            </td>
                            <td className="py-3 px-4 italic text-slate-300 max-w-xs truncate" title={op.opinion_original}>
                              “{op.opinion_original}”
                            </td>
                            <td className="py-3 px-4 whitespace-nowrap">
                              <SentimentBadge sentimiento={op.sentimiento} size="sm" />
                              {op.sentimiento_corregido && (
                                <span className="block text-[9px] font-mono text-cyanNeon mt-1">
                                  ✏️ Auditado (Orig: {op.sentimiento_original})
                                </span>
                              )}
                            </td>
                            <td className="py-3 px-4 text-slate-300 text-[11px] max-w-sm">
                              {op.razon}
                            </td>
                            <td className="py-3 px-4 text-center whitespace-nowrap">
                              <button
                                onClick={() => {
                                  setModalOpinion(op);
                                  setNuevoSentimiento(op.sentimiento || "positivo");
                                  setJustificacionCorreccion(op.justificacion_correccion || "");
                                }}
                                className="px-2.5 py-1 rounded-lg bg-cyanNeon/10 hover:bg-cyanNeon/25 text-cyanNeon border border-cyanNeon/30 font-mono text-[11px] transition-all"
                              >
                                ✏️ Auditar
                              </button>
                            </td>
                          </tr>
                        ))
                      )}
                    </tbody>
                  </table>
                </div>
              </div>

            </div>
          )}

          {/* ========================================================= */}
          {/* VISTA 3: LABORATORIO DE BENCHMARKING DUAL (SECCIÓN 12)    */}
          {/* ========================================================= */}
          {tab === "lab" && (
            <div className="flex-1 overflow-y-auto custom-scroll p-6 space-y-6">
              <div>
                <h2 className="font-outfit font-extrabold text-2xl text-amberNeon flex items-center gap-2">
                  <Icons.Flask className="w-6 h-6" /> Laboratorio de Benchmarking Dual
                </h2>
                <p className="text-xs text-slate-400 font-sans mt-0.5">
                  Desafío de Ampliación de la Sección 12: Inferencia comparativa en paralelo entre configuraciones de modelos de IA.
                </p>
              </div>

              <div className="glass-surface rounded-2xl p-6 border border-white/10 max-w-3xl">
                <div className="space-y-4">
                  <div>
                    <label className="block text-xs font-mono text-slate-400 uppercase font-bold mb-1">
                      Mandatario a contrastar:
                    </label>
                    <select
                      value={labPoliticoId}
                      onChange={(e) => setLabPoliticoId(e.target.value)}
                      className="w-full bg-pitch border border-white/15 rounded-xl px-4 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-amberNeon"
                    >
                      {catalogo.map(p => (
                        <option key={p.id} value={p.id}>{p.nombre} ({p.rol})</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-mono text-slate-400 uppercase font-bold mb-1">
                      Opinión o Enunciado a evaluar:
                    </label>
                    <textarea
                      rows="3"
                      value={labTexto}
                      onChange={(e) => setLabTexto(e.target.value)}
                      placeholder="Escribe un comentario ambiguo, irónico o descriptivo para probar el consenso entre modelos..."
                      className="w-full bg-pitch border border-white/15 rounded-xl p-3 text-xs text-slate-200 focus:outline-none focus:border-amberNeon custom-scroll resize-none"
                    />
                  </div>

                  <button
                    onClick={handleEjecutarLab}
                    disabled={labCargando || labTexto.trim().length < 5}
                    className="w-full py-2.5 rounded-xl bg-amberNeon hover:bg-amber-400 text-pitch font-bold text-xs font-mono flex items-center justify-center gap-2 transition-all shadow-[0_0_15px_rgba(245,158,11,0.3)] disabled:opacity-50"
                  >
                    {labCargando ? (
                      <>
                        <Icons.Refresh className="w-4 h-4 animate-spin" />
                        <span>Ejecutando Inferencia Dual Paralela...</span>
                      </>
                    ) : (
                      <>
                        <Icons.Flask className="w-4 h-4" />
                        <span>Ejecutar Benchmarking Comparativo</span>
                      </>
                    )}
                  </button>
                </div>

                {/* Resultados del Benchmarking */}
                {labResultado && (
                  <div className="mt-6 pt-6 border-t border-white/10 space-y-4 animate-fadeIn">
                    <div className="flex items-center justify-between">
                      <span className="font-outfit font-bold text-sm text-white">Resultados de Consenso:</span>
                      <span className={`px-3 py-1 rounded-full text-xs font-bold font-mono ${
                        labResultado.consenso
                          ? "bg-emeraldNeon/10 text-emeraldNeon border border-emeraldNeon/30"
                          : "bg-amberNeon/10 text-amberNeon border border-amberNeon/30"
                      }`}>
                        {labResultado.consenso ? "🟢 100% Consenso Semántico" : "🟡 Discrepancia Detectada"}
                      </span>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="p-4 rounded-xl bg-pitch/80 border border-emeraldNeon/30">
                        <span className="text-[10px] font-mono uppercase text-emeraldNeon font-bold block mb-1">
                          Configuración A ({labResultado.modelo_a})
                        </span>
                        <div className="mb-2">
                          <SentimentBadge sentimiento={labResultado.sentimiento_a} size="sm" />
                        </div>
                        <p className="text-xs text-slate-300 leading-relaxed">{labResultado.razon_a}</p>
                      </div>

                      <div className="p-4 rounded-xl bg-pitch/80 border border-cyanNeon/30">
                        <span className="text-[10px] font-mono uppercase text-cyanNeon font-bold block mb-1">
                          Configuración B ({labResultado.modelo_b})
                        </span>
                        <div className="mb-2">
                          <SentimentBadge sentimiento={labResultado.sentimiento_b} size="sm" />
                        </div>
                        <p className="text-xs text-slate-300 leading-relaxed">{labResultado.razon_b}</p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

        </main>
      </div>

      {/* ========================================================= */}
      {/* MODAL DE AUDITORÍA HUMANA (HUMAN-IN-THE-LOOP)             */}
      {/* ========================================================= */}
      {modalOpinion && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm animate-fadeIn">
          <div className="glass-surface-elevated rounded-2xl p-6 border border-white/20 max-w-lg w-full shadow-glass">
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-outfit font-bold text-base text-white flex items-center gap-2">
                <Icons.Edit className="w-4 h-4 text-cyanNeon" />
                Auditoría Humana (Human-in-the-Loop)
              </h3>
              <button
                onClick={() => setModalOpinion(null)}
                className="text-slate-400 hover:text-white"
              >
                <Icons.X className="w-4 h-4" />
              </button>
            </div>

            <p className="text-xs text-slate-300 mb-3">
              Reclasifica la etiqueta de sentimiento asignada por la IA preservando el valor original para trazabilidad de MLOps (Sección 12 Rúbrica):
            </p>

            <div className="bg-pitch/60 p-3 rounded-xl border border-white/5 mb-4 text-xs italic text-slate-200">
              “{modalOpinion.opinion_original}”
            </div>

            <div className="space-y-3.5">
              <div>
                <label className="block text-xs font-mono text-cyanNeon uppercase font-bold mb-1">
                  Nuevo Sentimiento Asignado:
                </label>
                <select
                  value={nuevoSentimiento}
                  onChange={(e) => setNuevoSentimiento(e.target.value)}
                  className="w-full bg-pitch border border-white/20 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-cyanNeon"
                >
                  <option value="positivo">🟢 Positivo</option>
                  <option value="negativo">🔴 Negativo</option>
                  <option value="neutro">⚪ Neutro</option>
                  <option value="mixto">🟡 Mixto</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-mono text-cyanNeon uppercase font-bold mb-1">
                  Justificación de la Reclasificación:
                </label>
                <input
                  type="text"
                  value={justificacionCorreccion}
                  onChange={(e) => setJustificacionCorreccion(e.target.value)}
                  placeholder="Ej: Se detectó ironía o ambigüedad fáctica que la IA evaluó literal..."
                  className="w-full bg-pitch border border-white/20 rounded-xl px-3 py-2 text-xs text-white placeholder:text-slate-500 focus:outline-none focus:border-cyanNeon"
                />
              </div>

              <div className="flex justify-end gap-2.5 pt-3 border-t border-white/10">
                <button
                  type="button"
                  onClick={() => setModalOpinion(null)}
                  className="px-4 py-2 rounded-xl bg-surface border border-white/10 text-xs font-semibold text-slate-300 hover:text-white transition-colors"
                >
                  Cancelar
                </button>
                <button
                  type="button"
                  onClick={handleGuardarCorreccion}
                  disabled={guardandoCorreccion}
                  className="px-4 py-2 rounded-xl bg-emeraldNeon hover:bg-emeraldGlow text-pitch font-bold text-xs flex items-center gap-1.5 transition-all shadow-glow-emerald"
                >
                  {guardandoCorreccion ? "Guardando..." : "Guardar Corrección"}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================= */}
      {/* NOTIFICACIÓN TOAST FLOTANTE                               */}
      {/* ========================================================= */}
      {toast && (
        <div className={`fixed bottom-5 right-5 z-50 px-4 py-3 rounded-xl border text-xs font-sans shadow-glass flex items-center gap-2 animate-bounce ${
          toast.tipo === "error"
            ? "bg-crimsonNeon/15 border-crimsonNeon/40 text-crimsonNeon"
            : toast.tipo === "success"
            ? "bg-emeraldNeon/15 border-emeraldNeon/40 text-emeraldNeon"
            : "bg-cyanNeon/15 border-cyanNeon/40 text-cyanNeon"
        }`}>
          {toast.tipo === "error" ? <Icons.AlertCircle className="w-4 h-4" /> : <Icons.CheckCircle className="w-4 h-4" />}
          <span>{toast.mensaje}</span>
        </div>
      )}

    </div>
  );
}

// Renderizar la Aplicación React en el DOM
const rootElement = document.getElementById("root");
const root = ReactDOM.createRoot(rootElement);
root.render(<App />);

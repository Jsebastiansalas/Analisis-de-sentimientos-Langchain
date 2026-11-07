/**
 * Ágora Colombia - Lógica de Frontend con JavaScript ES6+
 * Consume la API REST de FastAPI con Fetch API asíncrono
 * Maneja gráficos interactivos con Chart.js y alertas con SweetAlert2
 */

let catalogoPoliticos = [];
let politicoActivo = null;
let chartSentimientosInstance = null;
let chartBarrasInstance = null;

// Inicialización cuando carga el DOM
document.addEventListener("DOMContentLoaded", async () => {
  await inicializarCatalogo();
  configurarContadorCaracteres();
  await cargarAuditoria();
});

/**
 * Carga el catálogo de 20 figuras políticas desde la API REST
 */
async function inicializarCatalogo() {
  try {
    const res = await fetch("/api/politicos");
    if (!res.ok) throw new Error("Error al consultar catálogo");
    const data = await res.json();
    catalogoPoliticos = data.politicos || [];

    if (catalogoPoliticos.length > 0) {
      politicoActivo = catalogoPoliticos[0];
      actualizarPoliticoActivoUI();
      renderizarListaPoliticos(catalogoPoliticos);
      poblarSelectoresFiltro();
    }
  } catch (error) {
    console.error("Fallo al inicializar catálogo:", error);
    Swal.fire({
      icon: "error",
      title: "Error de Conexión",
      text: "No se pudo conectar con la API de Ágora Colombia.",
      background: "#0E1726",
      color: "#d4e4fa"
    });
  }
}

/**
 * Renderiza los elementos de la barra lateral
 */
function renderizarListaPoliticos(lista) {
  const contenedor = document.getElementById("lista-politicos");
  contenedor.innerHTML = "";

  lista.forEach((p) => {
    const esActivo = politicoActivo && politicoActivo.id === p.id;
    const card = document.createElement("div");
    card.className = `p-3 rounded-xl cursor-pointer transition-all border ${
      esActivo
        ? "bg-floodlight/90 border-emeraldNeon shadow-[0_0_12px_rgba(0,245,155,0.2)]"
        : "bg-carbon/40 hover:bg-carbon border-white/5 text-slate-300"
    }`;

    card.onclick = () => seleccionarPolitico(p);

    card.innerHTML = `
      <div class="flex items-center justify-between">
        <div class="font-outfit font-bold text-sm ${esActivo ? "text-emeraldNeon" : "text-slate-200"}">
          ${p.nombre}
        </div>
        <span class="text-[10px] font-mono font-bold px-1.5 py-0.5 rounded bg-pitch border border-white/10 ${esActivo ? "text-emeraldNeon" : "text-slate-400"}">
          ${p.id}
        </span>
      </div>
      <p class="text-[11px] text-slate-400 font-inter mt-1 truncate">${p.rol || p.pais}</p>
    `;

    contenedor.appendChild(card);
  });
}

/**
 * Filtra los políticos en la barra lateral mientras el usuario escribe
 */
function filtrarListaPoliticos() {
  const query = document.getElementById("filtro-lateral-politicos").value.toLowerCase();
  const filtrados = catalogoPoliticos.filter(
    (p) =>
      p.nombre.toLowerCase().includes(query) ||
      (p.rol && p.rol.toLowerCase().includes(query)) ||
      p.id.toLowerCase().includes(query)
  );
  renderizarListaPoliticos(filtrados);
}

/**
 * Cambia el político activo
 */
function seleccionarPolitico(p) {
  politicoActivo = p;
  actualizarPoliticoActivoUI();
  renderizarListaPoliticos(catalogoPoliticos);
}

/**
 * Actualiza los nombres y roles en la cabecera del chat
 */
function actualizarPoliticoActivoUI() {
  if (!politicoActivo) return;
  document.getElementById("politico-activo-nombre").textContent = politicoActivo.nombre;
  document.getElementById("politico-activo-rol").textContent = politicoActivo.rol || politicoActivo.pais;
}

/**
 * Llena el selector de filtro en la pestaña de auditoría
 */
function poblarSelectoresFiltro() {
  const select = document.getElementById("filtro-analytics-politico");
  select.innerHTML = '<option value="todos">Todas las Figuras Políticas</option>';
  catalogoPoliticos.forEach((p) => {
    const opt = document.createElement("option");
    opt.value = p.id;
    opt.textContent = p.nombre;
    select.appendChild(opt);
  });
}

/**
 * Contador de caracteres interactivo (5 a 1000)
 */
function configurarContadorCaracteres() {
  const textarea = document.getElementById("input-opinion");
  const contador = document.getElementById("contador-caracteres");

  textarea.addEventListener("input", (e) => {
    const len = e.target.value.trim().length;
    contador.textContent = `${len} / 1000 caracteres (Mín. 5)`;

    if (len < 5) {
      contador.className = "font-mono text-crimsonNeon font-bold";
    } else if (len > 1000) {
      contador.className = "font-mono text-crimsonNeon font-bold";
    } else {
      contador.className = "font-mono text-emeraldNeon font-bold";
    }
  });
}

/**
 * Cambia entre las pestañas "Emitir Opinión" y "Métricas"
 */
function cambiarTab(tab) {
  const vistaChat = document.getElementById("vista-chat");
  const vistaAnalytics = document.getElementById("vista-analytics");
  const btnChat = document.getElementById("btn-tab-chat");
  const btnAnalytics = document.getElementById("btn-tab-analytics");

  if (tab === "chat") {
    vistaChat.classList.remove("hidden");
    vistaAnalytics.classList.add("hidden");
    btnChat.className = "px-4 py-1.5 rounded-lg font-semibold transition-all bg-floodlight text-emeraldNeon border border-emeraldNeon/40 shadow-[0_0_10px_rgba(0,245,155,0.2)]";
    btnAnalytics.className = "px-4 py-1.5 rounded-lg font-semibold text-slate-400 hover:text-white transition-all";
  } else {
    vistaChat.classList.add("hidden");
    vistaAnalytics.classList.remove("hidden");
    btnAnalytics.className = "px-4 py-1.5 rounded-lg font-semibold transition-all bg-floodlight text-emeraldNeon border border-emeraldNeon/40 shadow-[0_0_10px_rgba(0,245,155,0.2)]";
    btnChat.className = "px-4 py-1.5 rounded-lg font-semibold text-slate-400 hover:text-white transition-all";
    cargarAuditoria();
  }
}

/**
 * Envía la opinión ciudadana a la API REST para análisis con LangChain y guardado
 */
async function enviarOpinion() {
  const textarea = document.getElementById("input-opinion");
  const texto = textarea.value.trim();
  const btn = document.getElementById("btn-enviar-opinion");

  if (texto.length < 5) {
    Swal.fire({
      icon: "warning",
      title: "Opinión muy corta",
      text: "La opinión debe contener al menos 5 caracteres significativos.",
      background: "#0E1726",
      color: "#d4e4fa"
    });
    return;
  }

  if (texto.length > 1000) {
    Swal.fire({
      icon: "warning",
      title: "Opinión muy larga",
      text: "La opinión supera el límite de 1000 caracteres.",
      background: "#0E1726",
      color: "#d4e4fa"
    });
    return;
  }

  // Congelar la figura activa al momento del envío
  const politicoEnvio = { ...politicoActivo };

  // Deshabilitar botón durante inferencia
  btn.disabled = true;
  btn.innerHTML = `<span>Analizando...</span> <span class="animate-spin">🔄</span>`;

  // Renderizar mensaje del usuario inmediatamente en el feed
  agregarMensajeUsuarioChat(politicoEnvio.nombre, texto);
  textarea.value = "";
  document.getElementById("contador-caracteres").textContent = "0 / 1000 caracteres (Mín. 5)";

  try {
    const res = await fetch("/api/opiniones", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        politico_id: politicoEnvio.id,
        opinion: texto
      })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Error al procesar la opinión");

    if (!data.es_pertinente) {
      // Mensaje no pertinente
      agregarMensajeNoPertinenteChat(data.razon);
      Swal.fire({
        icon: "info",
        title: "Comentario No Pertinente",
        text: data.razon,
        background: "#0E1726",
        color: "#d4e4fa"
      });
    } else {
      // Mensaje analizado y guardado con éxito
      agregarMensajeAsistenteChat(data.sentimiento, data.razon, data.registro?.id);
      Swal.fire({
        icon: "success",
        title: "¡Opinión Analizada y Persistida!",
        text: `Clasificada como ${data.sentimiento.toUpperCase()}. Guardada en opiniones.json.`,
        timer: 3000,
        showConfirmButton: false,
        background: "#0E1726",
        color: "#d4e4fa"
      });
    }
  } catch (error) {
    console.error("Fallo al enviar opinión:", error);
    Swal.fire({
      icon: "error",
      title: "Error de Inferencia",
      text: error.message || "No se pudo comunicar con el modelo de IA.",
      background: "#0E1726",
      color: "#d4e4fa"
    });
    // Restaurar texto en textarea para que el usuario no lo pierda
    textarea.value = texto;
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<span>Enviar</span> <span>🚀</span>`;
  }
}

/**
 * Inserta la tarjeta del usuario en el chat
 */
function agregarMensajeUsuarioChat(politicoNombre, texto) {
  const feed = document.getElementById("chat-feed");
  const card = document.createElement("div");
  card.className = "glass-card rounded-xl p-4 border-l-4 border-cyanNeon animate-fadeIn";
  card.innerHTML = `
    <div class="flex justify-between items-center text-xs text-slate-400 mb-1">
      <span class="font-outfit font-bold text-cyanNeon">👤 Opinión Ciudadana sobre <strong>${politicoNombre}</strong></span>
      <span class="font-mono text-[10px]">Justo ahora</span>
    </div>
    <p class="text-sm text-slate-100 italic">“${texto}”</p>
  `;
  feed.appendChild(card);
  feed.scrollTop = feed.scrollHeight;
}

/**
 * Inserta la respuesta de IA con la píldora neón
 */
function agregarMensajeAsistenteChat(sentimiento, razon, uuid) {
  const feed = document.getElementById("chat-feed");
  const card = document.createElement("div");
  card.className = "glass-card rounded-xl p-4 border-l-4 border-emeraldNeon animate-fadeIn";

  const badges = {
    positivo: `<span class="px-3 py-1 rounded-full text-xs font-bold font-inter bg-emeraldNeon/10 text-emeraldNeon border border-emeraldNeon/30 shadow-[0_0_10px_rgba(0,245,155,0.2)]">🟢 POSITIVO</span>`,
    negativo: `<span class="px-3 py-1 rounded-full text-xs font-bold font-inter bg-crimsonNeon/10 text-crimsonNeon border border-crimsonNeon/30 shadow-[0_0_10px_rgba(255,59,87,0.2)]">🔴 NEGATIVO</span>`,
    mixto: `<span class="px-3 py-1 rounded-full text-xs font-bold font-inter bg-amberNeon/10 text-amberNeon border border-amberNeon/30 shadow-[0_0_10px_rgba(255,183,3,0.2)]">🟡 MIXTO</span>`,
    neutro: `<span class="px-3 py-1 rounded-full text-xs font-bold font-inter bg-slate-500/10 text-slate-300 border border-slate-500/30">⚪ NEUTRO</span>`
  };

  card.innerHTML = `
    <div class="flex justify-between items-center mb-2">
      <span class="font-outfit font-bold text-xs text-emeraldNeon flex items-center gap-1.5">
        🤖 Clasificación de Inferencia AI
      </span>
      ${badges[sentimiento] || sentimiento}
    </div>
    <div class="bg-pitch/60 rounded-lg p-2.5 border border-white/5 text-xs text-slate-200">
      <strong class="text-cyanNeon">Justificación Técnica:</strong> ${razon}
    </div>
    <div class="flex justify-between items-center text-[10px] text-slate-400 font-mono mt-2 pt-2 border-t border-white/5">
      <span>💾 Persistido en opiniones.json</span>
      <span>UUID: ${uuid ? uuid.slice(0, 8) + "..." : "Generado"}</span>
    </div>
  `;
  feed.appendChild(card);
  feed.scrollTop = feed.scrollHeight;
}

/**
 * Inserta el rechazo de opinión no pertinente
 */
function agregarMensajeNoPertinenteChat(razon) {
  const feed = document.getElementById("chat-feed");
  const card = document.createElement("div");
  card.className = "glass-card rounded-xl p-4 border-l-4 border-crimsonNeon animate-fadeIn";
  card.innerHTML = `
    <div class="flex justify-between items-center text-xs font-bold text-crimsonNeon mb-1">
      <span>⚠️ Comentario No Pertinente Rechazado</span>
      <span class="px-2 py-0.5 rounded bg-crimsonNeon/10 border border-crimsonNeon/30 text-[10px]">NO GUARDADO</span>
    </div>
    <p class="text-xs text-slate-300">${razon}</p>
    <p class="text-[10px] text-slate-500 mt-1 font-inter">ℹ️ El comentario no guarda relación con la figura seleccionada. No se ha persistido en disco.</p>
  `;
  feed.appendChild(card);
  feed.scrollTop = feed.scrollHeight;
}

/**
 * Carga las opiniones y actualiza métricas y gráficos de Chart.js
 */
async function cargarAuditoria() {
  const politicoId = document.getElementById("filtro-analytics-politico")?.value || "todos";
  const sentimiento = document.getElementById("filtro-analytics-sentimiento")?.value || "todos";
  const texto = document.getElementById("filtro-analytics-texto")?.value || "";

  try {
    let url = `/api/opiniones?politico_id=${politicoId}&sentimiento=${sentimiento}`;
    if (texto.trim()) {
      url += `&q=${encodeURIComponent(texto.trim())}`;
    }
    const res = await fetch(url);
    if (!res.ok) throw new Error("Fallo al obtener opiniones");
    const data = await res.json();

    const metricas = data.metricas || {};
    const opiniones = data.opiniones || [];

    // Actualizar contadores numéricos
    document.getElementById("metric-total").textContent = metricas.total || 0;
    document.getElementById("metric-positivo").textContent = metricas.positivo || 0;
    document.getElementById("metric-negativo").textContent = metricas.negativo || 0;
    document.getElementById("metric-neutro").textContent = metricas.neutro || 0;
    document.getElementById("metric-mixto").textContent = metricas.mixto || 0;

    // Actualizar gráficos interactivos con Chart.js
    renderizarGraficoSentimientos(metricas);
    renderizarGraficoBarras(opiniones);

    // Actualizar tabla
    renderizarTablaAuditoria(opiniones);
  } catch (error) {
    console.error("Error al cargar auditoría:", error);
  }
}

/**
 * Gráfico de Dona con Chart.js
 */
function renderizarGraficoSentimientos(metricas) {
  const ctx = document.getElementById("chart-sentimientos");
  if (!ctx) return;

  if (chartSentimientosInstance) {
    chartSentimientosInstance.destroy();
  }

  chartSentimientosInstance = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Positivo", "Negativo", "Neutro", "Mixto"],
      datasets: [
        {
          data: [
            metricas.positivo || 0,
            metricas.negativo || 0,
            metricas.neutro || 0,
            metricas.mixto || 0
          ],
          backgroundColor: ["#00F59B", "#FF3B57", "#94A3B8", "#FFB703"],
          borderWidth: 2,
          borderColor: "#0E1726"
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "bottom",
          labels: { color: "#d4e4fa", font: { family: "Inter", size: 11 } }
        }
      }
    }
  });
}

/**
 * Gráfico de Barras con Chart.js
 */
function renderizarGraficoBarras(opiniones) {
  const ctx = document.getElementById("chart-barras");
  if (!ctx) return;

  if (chartBarrasInstance) {
    chartBarrasInstance.destroy();
  }

  // Agrupar por político
  const conteoPorPolitico = {};
  opiniones.forEach((op) => {
    const nom = op.jugador_nombre || "Desconocido";
    if (!conteoPorPolitico[nom]) {
      conteoPorPolitico[nom] = { pos: 0, neg: 0 };
    }
    if (op.sentimiento === "positivo") conteoPorPolitico[nom].pos++;
    if (op.sentimiento === "negativo") conteoPorPolitico[nom].neg++;
  });

  const nombres = Object.keys(conteoPorPolitico).slice(0, 5); // Top 5
  const positivos = nombres.map((n) => conteoPorPolitico[n].pos);
  const negativos = nombres.map((n) => conteoPorPolitico[n].neg);

  chartBarrasInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: nombres.map((n) => (n.length > 15 ? n.slice(0, 15) + "..." : n)),
      datasets: [
        {
          label: "Positivas",
          data: positivos,
          backgroundColor: "#00F59B"
        },
        {
          label: "Negativas",
          data: negativos,
          backgroundColor: "#FF3B57"
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { ticks: { color: "#94a3b8" }, grid: { color: "rgba(255,255,255,0.05)" } },
        y: { ticks: { color: "#94a3b8" }, grid: { color: "rgba(255,255,255,0.05)" } }
      },
      plugins: {
        legend: { labels: { color: "#d4e4fa", font: { family: "Inter", size: 11 } } }
      }
    }
  });
}

/**
 * Renderiza la tabla HTML de auditoría
 */
function renderizarTablaAuditoria(opiniones) {
  const tbody = document.getElementById("tabla-auditoria-cuerpo");
  if (!tbody) return;
  tbody.innerHTML = "";

  if (opiniones.length === 0) {
    tbody.innerHTML = `<tr><td colspan="6" class="py-6 text-center text-slate-500 font-inter">No se encontraron opiniones para los filtros seleccionados.</td></tr>`;
    return;
  }

  const badges = {
    positivo: `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emeraldNeon/10 text-emeraldNeon border border-emeraldNeon/30">Positivo</span>`,
    negativo: `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-crimsonNeon/10 text-crimsonNeon border border-crimsonNeon/30">Negativo</span>`,
    mixto: `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amberNeon/10 text-amberNeon border border-amberNeon/30">Mixto</span>`,
    neutro: `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-500/10 text-slate-300 border border-slate-500/30">Neutro</span>`
  };

  opiniones.slice(-20).reverse().forEach((op) => {
    const tr = document.createElement("tr");
    tr.className = "hover:bg-carbon/50 transition-colors";
    const fecha = (op.fecha_utc || "").slice(0, 19).replace("T", " ");

    const badgeHumano = op.sentimiento_corregido
      ? `<span class="block text-[9px] text-cyanNeon font-mono mt-1">✏️ Auditado (Orig: ${op.sentimiento_original})</span>`
      : "";

    tr.innerHTML = `
      <td class="py-2.5 px-4 font-mono text-[11px] text-slate-400">${fecha}</td>
      <td class="py-2.5 px-4 font-semibold text-white">${op.jugador_nombre || ""}</td>
      <td class="py-2.5 px-4 italic text-slate-300 max-w-xs truncate" title="${op.opinion_original}">“${op.opinion_original}”</td>
      <td class="py-2.5 px-4">
        ${badges[op.sentimiento] || op.sentimiento}
        ${badgeHumano}
      </td>
      <td class="py-2.5 px-4 text-slate-300 text-[11px]">${op.razon || ""}</td>
      <td class="py-2.5 px-4 text-center">
        <button onclick="abrirModalCorreccion('${op.id}', '${op.sentimiento}')" class="px-2 py-1 rounded bg-cyanNeon/10 hover:bg-cyanNeon/25 text-cyanNeon border border-cyanNeon/30 text-[11px] font-mono transition-all">
          ✏️ Auditar
        </button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

/**
 * Modal SweetAlert2 para Human-in-the-Loop
 */
async function abrirModalCorreccion(id, sentimientoActual) {
  const { value: formValues } = await Swal.fire({
    title: "Auditoría Humana (Human-in-the-Loop)",
    background: "#0E1726",
    color: "#d4e4fa",
    html: `
      <p class="text-xs text-slate-400 mb-3 text-left">Corrige la etiqueta del sentimiento asignada por la IA preservando el valor original (Sección 12 Rúbrica):</p>
      <label class="block text-xs text-cyanNeon text-left mb-1 font-bold">Nuevo Sentimiento:</label>
      <select id="swal-sentimiento" class="w-full bg-[#051424] text-white p-2 rounded border border-white/20 mb-3 text-xs">
        <option value="positivo" ${sentimientoActual === "positivo" ? "selected" : ""}>🟢 Positivo</option>
        <option value="negativo" ${sentimientoActual === "negativo" ? "selected" : ""}>🔴 Negativo</option>
        <option value="neutro" ${sentimientoActual === "neutro" ? "selected" : ""}>⚪ Neutro</option>
        <option value="mixto" ${sentimientoActual === "mixto" ? "selected" : ""}>🟡 Mixto</option>
      </select>
      <label class="block text-xs text-cyanNeon text-left mb-1 font-bold">Justificación de la corrección:</label>
      <input id="swal-justificacion" placeholder="Ej: Se identificó ironía o doble sentido..." class="w-full bg-[#051424] text-white p-2 rounded border border-white/20 text-xs">
    `,
    focusConfirm: false,
    showCancelButton: true,
    confirmButtonText: "Guardar Corrección",
    cancelButtonText: "Cancelar",
    confirmButtonColor: "#00F59B",
    cancelButtonColor: "#FF3B57",
    preConfirm: () => {
      return {
        nuevo_sentimiento: document.getElementById("swal-sentimiento").value,
        justificacion: document.getElementById("swal-justificacion").value
      };
    }
  });

  if (formValues) {
    try {
      const res = await fetch(`/api/opiniones/${id}/corregir`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formValues)
      });
      if (!res.ok) throw new Error("Fallo al guardar corrección");
      Swal.fire({
        icon: "success",
        title: "¡Corrección Guardada!",
        text: "Se actualizó la opinión preservando el historial original.",
        background: "#0E1726",
        color: "#d4e4fa",
        confirmButtonColor: "#00F59B"
      });
      cargarAuditoria();
    } catch (e) {
      Swal.fire({
        icon: "error",
        title: "Error",
        text: e.message,
        background: "#0E1726",
        color: "#d4e4fa"
      });
    }
  }
}

/**
 * Descarga el archivo JSON filtrado desde el endpoint REST
 */
function descargarJSON() {
  const politicoId = document.getElementById("filtro-analytics-politico")?.value || "todos";
  const sentimiento = document.getElementById("filtro-analytics-sentimiento")?.value || "todos";
  window.location.href = `/api/exportar?politico_id=${politicoId}&sentimiento=${sentimiento}`;
}

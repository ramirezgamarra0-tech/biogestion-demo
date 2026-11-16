"""BioGestión 9 — vitrina comercial y demo aislada, con datos enteramente ficticios.
No utiliza Supabase, credenciales, ni almacena contactos en el servidor.
"""
from datetime import date, timedelta
from urllib.parse import urlparse
import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="BioGestión | Gestión biomédica", page_icon="🏥", layout="wide", initial_sidebar_state="expanded")
st.markdown("""<style>
[data-testid="stAppViewContainer"]{background:#f2f6fb}
[data-testid="stSidebar"]{background:#112c44}
[data-testid="stSidebar"] *{color:#f3f7fb}
[data-testid="stMetric"]{background:white;border:1px solid #dae5ef;border-radius:14px;padding:18px}
h1,h2,h3{color:#15354f}
.hero{background:linear-gradient(115deg,#102d46,#116b78);border-radius:20px;padding:28px;color:white;margin-bottom:16px}
.hero h1{color:white;margin:0 0 10px 0;font-size:2.2rem}
.hero p{color:#e0eff2;margin:0}
.note{font-size:.87rem;color:#5c6c7c}
</style>""", unsafe_allow_html=True)


def _form_link():
    """URL configurable sin dejar datos personales en GitHub."""
    url = os.getenv("BIOGESTION_FORM_URL", "").strip()
    if not url:
        try:
            url = str(st.secrets.get("BIOGESTION_FORM_URL", "")).strip()
        except (FileNotFoundError, KeyError, AttributeError):
            url = ""
    if not url:
        return ""
    parts = urlparse(url)
    if parts.scheme != "https" or parts.hostname not in {"docs.google.com", "forms.gle"}:
        return ""
    return url

FORM_URL = _form_link()
TODAY = date.today()
EQUIPOS = [
    dict(codigo="DEMO-001", nombre="Monitor multiparámetro", marca="Marca ficticia A", modelo="MP-100", ubicacion="Consultorio A", estado="Operativo"),
    dict(codigo="DEMO-002", nombre="Electrocardiógrafo", marca="Marca ficticia B", modelo="ECG-200", ubicacion="Consultorio B", estado="Operativo"),
    dict(codigo="DEMO-003", nombre="Bomba de infusión", marca="Marca ficticia C", modelo="BI-300", ubicacion="Almacén", estado="En mantenimiento"),
    dict(codigo="DEMO-004", nombre="Desfibrilador", marca="Marca ficticia D", modelo="DF-400", ubicacion="Emergencia", estado="Operativo"),
    dict(codigo="DEMO-005", nombre="Oxímetro de pulso", marca="Marca ficticia E", modelo="OX-500", ubicacion="Consultorio A", estado="Inoperativo"),
]
MANTENIMIENTOS = [
    dict(equipo="DEMO-001", tipo="Preventivo", fecha=(TODAY + timedelta(days=12)).isoformat(), responsable="Técnico de ejemplo", estado="Programado"),
    dict(equipo="DEMO-003", tipo="Correctivo", fecha=(TODAY - timedelta(days=3)).isoformat(), responsable="Técnico de ejemplo", estado="Programado"),
    dict(equipo="DEMO-004", tipo="Preventivo", fecha=(TODAY + timedelta(days=28)).isoformat(), responsable="Técnico de ejemplo", estado="Programado"),
]
PAGES = ["🏠 Inicio", "📊 Panel general", "📋 Inventario", "🛠️ Mantenimientos", "📁 Documentos", "💳 Planes", "💬 Solicitar demostración"]
with st.sidebar:
    st.title("🏥 BioGestión")
    st.caption("Gestión de equipamiento biomédico")
    page = st.radio("Explorar", PAGES)
    st.divider()
    st.caption("VERSIÓN 9.0 · DEMO PÚBLICA")
    st.info("Solo datos ficticios. Sin acceso a tu PostgreSQL privado.")

# Protección pedagógica: nunca se aceptan datos reales en las pantallas demo.
if page == "🏠 Inicio":
    st.markdown('<div class="hero"><h1>BioGestión</h1><p>Organiza inventario, mantenimientos y documentación de equipamiento biomédico en una sola plataforma.</p></div>', unsafe_allow_html=True)
    st.warning("Versión de demostración: funciones mostradas con datos simulados. No introduzcas datos personales o de instituciones.")
    st.subheader("¿Qué problemas ayuda a organizar?")
    cols = st.columns(3)
    for col, title, body in zip(cols, ["📋 Inventario centralizado", "🛠️ Seguimiento de mantenimiento", "📁 Documentación vinculada"], ["Busca equipos por código, estado y ubicación.", "Consulta intervenciones programadas y alertas dentro de la plataforma.", "Relaciona fichas y reportes con el equipo correspondiente."]):
        with col:
            with st.container(border=True):
                st.markdown("**" + title + "**")
                st.write(body)
    st.subheader("Pensado para")
    st.write("Consultorios, pequeños laboratorios, empresas de mantenimiento e iniciativas de ingeniería clínica que necesiten ordenar sus registros.")
    st.info("La plataforma privada continúa en evaluación técnica. Esta web no ofrece cuentas comerciales ni procesamiento de información real.")
    st.markdown("**Explora las secciones del menú lateral para conocer el prototipo.**")

elif page == "📊 Panel general":
    st.title("Panel de demostración")
    st.caption("Indicadores calculados sobre cinco equipos ficticios.")
    df = pd.DataFrame(EQUIPOS)
    a, b, c, d = st.columns(4)
    a.metric("Equipos", len(df))
    b.metric("Operativos", int((df.estado == "Operativo").sum()))
    c.metric("En mantenimiento", int((df.estado == "En mantenimiento").sum()))
    d.metric("Inoperativos", int((df.estado == "Inoperativo").sum()))
    left, right = st.columns(2)
    with left:
        st.subheader("Equipos por estado")
        st.bar_chart(df.estado.value_counts(), horizontal=True)
    with right:
        st.subheader("Próximos mantenimientos")
        md = pd.DataFrame(MANTENIMIENTOS)
        md["alerta"] = md.fecha.map(lambda x: "Vencido" if date.fromisoformat(x) < TODAY else "Próximo")
        st.dataframe(md, hide_index=True, use_container_width=True)
    st.subheader("Últimos equipos")
    st.dataframe(df[["codigo", "nombre", "ubicacion", "estado"]], hide_index=True, use_container_width=True)

elif page == "📋 Inventario":
    st.title("Inventario biomédico")
    st.caption("Búsqueda y filtros sobre registros ficticios; aquí no se guardan modificaciones.")
    df = pd.DataFrame(EQUIPOS)
    query = st.text_input("Buscar equipo o código")
    states = st.multiselect("Estado", sorted(df.estado.unique()), default=sorted(df.estado.unique()))
    filtered = df[df.estado.isin(states)]
    if query:
        mask = filtered[["codigo", "nombre"]].apply(lambda s: s.str.contains(query, case=False, regex=False)).any(axis=1)
        filtered = filtered[mask]
    st.dataframe(filtered, hide_index=True, use_container_width=True)
    st.download_button("📥 Descargar CSV ficticio", filtered.to_csv(index=False).encode("utf-8-sig"), "inventario_demo.csv", "text/csv")
    st.info("La versión privada permite registrar, editar y administrar equipos. Esas acciones no están disponibles públicamente.")

elif page == "🛠️ Mantenimientos":
    st.title("Gestión de mantenimientos")
    df = pd.DataFrame(MANTENIMIENTOS)
    df["alerta"] = df.fecha.map(lambda x: "Vencido" if date.fromisoformat(x) < TODAY else "Próximo" if (date.fromisoformat(x) - TODAY).days <= 30 else "Programado")
    st.dataframe(df, hide_index=True, use_container_width=True)
    st.info("Vista de ejemplo. La versión privada permite programar y registrar ejecuciones; los avisos no se envían por correo automáticamente.")

elif page == "📁 Documentos":
    st.title("Documentación técnica")
    st.dataframe(pd.DataFrame([
        dict(equipo="DEMO-001", tipo="Ficha técnica", documento="Ejemplo sin archivo descargable"),
        dict(equipo="DEMO-004", tipo="Reporte", documento="Ejemplo sin archivo descargable"),
    ]), hide_index=True, use_container_width=True)
    st.info("Esta página no permite subir ni almacenar archivos. Solo ilustra la organización de documentos.")

elif page == "💳 Planes":
    st.title("Planes propuestos para una futura etapa piloto")
    st.warning("Precios orientativos para validar interés; no se aceptan pagos ni se contratan suscripciones en esta demostración.")
    offers = [
        ("Inicial", "S/39 / mes", "Pensado para consultorios pequeños", "Inventario y reportes básicos"),
        ("Profesional", "S/79 / mes", "Pensado para laboratorios y pequeñas clínicas", "Inventario, mantenimiento y documentación"),
        ("Organizaciones", "Desde S/149 / mes", "Pensado para equipos de trabajo", "Usuarios y necesidades a definir en una prueba piloto"),
    ]
    for col, (name, amount, who, features) in zip(st.columns(3), offers):
        with col:
            with st.container(border=True):
                st.subheader(name)
                st.markdown("### " + amount)
                st.write(who)
                st.caption(features)
                st.caption("Propuesta, no oferta contractual")
    st.subheader("Preguntas frecuentes")
    with st.expander("¿Puedo registrar pacientes o información confidencial?"):
        st.write("No. La demostración y la plataforma privada siguen en fase de evaluación de seguridad y respaldo.")
    with st.expander("¿Esta web permite pagar o abrir cuentas comerciales?"):
        st.write("No. Los precios son propuestas para conversar con interesados, sin checkout ni cobro.")
    with st.expander("¿Los archivos y cambios de esta demo se guardan?"):
        st.write("No. Todos los datos de esta demo son ficticios y permanecen como ejemplos en el código.")

else:
    st.title("Solicitar una demostración")
    st.write("BioGestión está en desarrollo y se están recopilando comentarios sobre las funciones de gestión de equipamiento biomédico.")
    st.info("Una solicitud no garantiza acceso inmediato a una versión privada ni constituye una contratación.")
    if FORM_URL:
        st.write("Puedes abrir un formulario externo de Google Forms para expresar interés. El formulario, y no esta aplicación, gestionará los datos que decidas compartir.")
        st.link_button("📝 Abrir formulario de interés", FORM_URL, type="primary")
        st.caption("Comparte solo datos de contacto necesarios; evita información de pacientes, registros de equipos o documentos privados.")
    else:
        st.warning("Formulario de contacto pendiente de configurar. El desarrollador todavía no ha habilitado la recepción de solicitudes.")
        st.write("Para activarlo: crea un Google Form, publícalo, copia el enlace para responder y configúralo como BIOGESTION_FORM_URL en Secrets de Streamlit Community Cloud.")

st.divider()
st.caption("BioGestión · V9 · Demostración pública sin conexión con Supabase · Material de presentación, no sistema de atención clínica.")

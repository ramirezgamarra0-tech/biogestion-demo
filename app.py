"""BioGestión V10 — demostración pública, totalmente aislada y con datos ficticios.
No usa PostgreSQL, guarda datos personales ni requiere secretos.
"""
from datetime import date, timedelta
import pandas as pd
import streamlit as st

st.set_page_config(page_title="BioGestión | Demo V10", page_icon="🏥", layout="wide", initial_sidebar_state="expanded")
st.markdown("""<style>
[data-testid="stAppViewContainer"]{background:#f2f6fb}
[data-testid="stSidebar"]{background:#102b43}
[data-testid="stSidebar"] label,[data-testid="stSidebar"] p,[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,[data-testid="stSidebar"] span{color:#f6fbff!important}
[data-testid="stSidebar"] [data-testid="stAlert"]{background:#21445a!important;border:1px solid #3d657b!important}
[data-testid="stSidebar"] [data-testid="stAlert"] p{color:#f6fbff!important}
[data-testid="stMetric"]{background:white;border:1px solid #dbe6ee;border-radius:14px;padding:17px}
h1,h2,h3{color:#16354e}
.hero{background:linear-gradient(110deg,#102d46,#0f7782);border-radius:18px;padding:30px;color:#fff;margin-bottom:18px}
.hero h1{color:#fff!important;margin:0 0 12px}.hero p{color:#eaf9fb;margin:0}
.small-note{color:#586b79;font-size:.9rem}
</style>""", unsafe_allow_html=True)

HOY = date.today()
EQUIPOS = [
 dict(codigo="DEMO-001",nombre="Monitor multiparámetro",marca="Marca ficticia A",modelo="MP-100",ubicacion="Consultorio A",estado="Operativo"),
 dict(codigo="DEMO-002",nombre="Electrocardiógrafo",marca="Marca ficticia B",modelo="ECG-200",ubicacion="Consultorio B",estado="Operativo"),
 dict(codigo="DEMO-003",nombre="Bomba de infusión",marca="Marca ficticia C",modelo="BI-300",ubicacion="Almacén",estado="En mantenimiento"),
 dict(codigo="DEMO-004",nombre="Desfibrilador",marca="Marca ficticia D",modelo="DF-400",ubicacion="Emergencia",estado="Operativo"),
 dict(codigo="DEMO-005",nombre="Oxímetro de pulso",marca="Marca ficticia E",modelo="OX-500",ubicacion="Consultorio A",estado="Inoperativo"),
]
BASE_MANT = [
 dict(equipo="DEMO-001",tipo="Preventivo",fecha=HOY+timedelta(days=12),responsable="Técnico de ejemplo",estado="Programado"),
 dict(equipo="DEMO-003",tipo="Correctivo",fecha=HOY-timedelta(days=3),responsable="Técnico de ejemplo",estado="Programado"),
 dict(equipo="DEMO-004",tipo="Preventivo",fecha=HOY+timedelta(days=28),responsable="Técnico de ejemplo",estado="Programado"),
]
if "mantenimientos_demo" not in st.session_state:
    st.session_state.mantenimientos_demo = [dict(x) for x in BASE_MANT]
if "equipos_demo" not in st.session_state:
    st.session_state.equipos_demo = [dict(x) for x in EQUIPOS]

PAGES=["🏠 Inicio","📊 Panel general","📋 Inventario","🛠️ Mantenimientos","📁 Documentos","💳 Planes"]
with st.sidebar:
    st.title("🏥 BioGestión")
    st.caption("Gestión de equipamiento biomédico")
    page=st.radio("Explorar",PAGES)
    st.divider()
    st.caption("VERSIÓN 10.0 · DEMO PÚBLICA")
    st.info("Datos 100 % ficticios. No se conecta a Supabase ni guarda información privada.")
    if st.button("↺ Reiniciar datos de prueba",use_container_width=True):
        st.session_state.mantenimientos_demo=[dict(x) for x in BASE_MANT]
        st.session_state.equipos_demo=[dict(x) for x in EQUIPOS]
        st.rerun()

ed=pd.DataFrame(st.session_state.equipos_demo)
md=pd.DataFrame(st.session_state.mantenimientos_demo)
def alert_status(d):
    days=(d-HOY).days
    return "🔴 Vencido" if days<0 else "🟠 Próximo (30 días)" if days<=30 else "🟢 Programado"

if page=="🏠 Inicio":
    st.markdown('<div class="hero"><h1>BioGestión</h1><p>Inventario, mantenimiento y documentos de equipos biomédicos, en una plataforma organizada.</p></div>', unsafe_allow_html=True)
    st.warning("DEMO PÚBLICA: las acciones solo modifican datos ficticios de esta sesión. No introduzcas datos de personas, empresas ni pacientes.")
    st.subheader("¿Qué puedes explorar?")
    cols=st.columns(3)
    for col,title,body in zip(cols,["📋 Inventario centralizado","🛠️ Mantenimientos y alertas","📁 Documentación vinculada"],["Busca, filtra y exporta equipos ficticios.","Programa mantenimientos de prueba y revisa sus vencimientos.","Visualiza cómo se organizarían manuales y fichas por equipo."]):
        with col:
            with st.container(border=True):
                st.markdown(f"**{title}**")
                st.write(body)
    st.subheader("Orientado a")
    st.write("Consultorios, laboratorios pequeños y empresas de servicio técnico que necesitan organizar información de equipamiento.")
    st.info("Esta demostración es independiente de la versión privada. No acepta usuarios comerciales ni pagos.")

elif page=="📊 Panel general":
    st.title("Panel general")
    st.caption("Resumen interactivo calculado con datos ficticios.")
    a,b,c,d=st.columns(4)
    a.metric("Equipos",len(ed));b.metric("Operativos",int((ed.estado=="Operativo").sum()))
    c.metric("En mantenimiento",int((ed.estado=="En mantenimiento").sum()))
    d.metric("Inoperativos",int((ed.estado=="Inoperativo").sum()))
    x,y=st.columns(2)
    with x:
        st.subheader("Equipos por estado")
        st.bar_chart(ed.estado.value_counts(),horizontal=True)
    with y:
        st.subheader("Estado de mantenimientos")
        if len(md):
            m=md.copy();m["alerta"]=m.fecha.map(alert_status)
            v=int((m.alerta=="🔴 Vencido").sum());p=int((m.alerta=="🟠 Próximo (30 días)").sum())
            st.metric("Vencidos",v);st.metric("Próximos 30 días",p)
            st.dataframe(m[["equipo","tipo","fecha","alerta"]],hide_index=True,use_container_width=True)
    st.subheader("Equipos recientes")
    st.dataframe(ed[["codigo","nombre","ubicacion","estado"]],hide_index=True,use_container_width=True)

elif page=="📋 Inventario":
    st.title("Inventario")
    st.caption("Vista de consulta con búsqueda, filtros y exportación CSV de demostración.")
    a,b=st.columns([2,1]);busqueda=a.text_input("Buscar por código, equipo, marca o ubicación")
    estado=b.multiselect("Filtrar por estado",sorted(ed.estado.unique()),default=sorted(ed.estado.unique()))
    mask=ed.estado.isin(estado)
    if busqueda:
        mask &= ed[["codigo","nombre","marca","ubicacion"]].astype(str).apply(lambda s:s.str.contains(busqueda,case=False,regex=False)).any(axis=1)
    filtered=ed.loc[mask]
    st.caption(f"{len(filtered)} de {len(ed)} equipos")
    st.dataframe(filtered,hide_index=True,use_container_width=True)
    st.download_button("📥 Exportar inventario ficticio (CSV)",filtered.to_csv(index=False).encode("utf-8-sig"),"inventario_demo.csv","text/csv")
    st.info("Las funciones de alta, edición y eliminación reales pertenecen a la aplicación privada; no están conectadas a esta demo.")

elif page=="🛠️ Mantenimientos":
    st.title("Mantenimiento biomédico · simulador")
    st.caption("Puedes programar intervenciones ficticias. Los cambios desaparecen al cerrar la sesión o reiniciar la demo.")
    with st.expander("➕ Programar un mantenimiento de prueba",expanded=True):
        with st.form("nuevo_mantenimiento_demo",clear_on_submit=True):
            c1,c2=st.columns(2)
            equipo=c1.selectbox("Equipo ficticio",ed.codigo.tolist())
            tipo=c2.selectbox("Tipo",["Preventivo","Correctivo"])
            c3,c4=st.columns(2)
            fecha=c3.date_input("Fecha programada",value=HOY+timedelta(days=15))
            responsable=c4.selectbox("Responsable ficticio",["Técnico de ejemplo","Área de mantenimiento"])
            if st.form_submit_button("Guardar mantenimiento de prueba",type="primary"):
                st.session_state.mantenimientos_demo.append(dict(equipo=equipo,tipo=tipo,fecha=fecha,responsable=responsable,estado="Programado"))
                st.success("Mantenimiento ficticio agregado solo a esta sesión.")
                st.rerun()
    df=pd.DataFrame(st.session_state.mantenimientos_demo)
    df["alerta"]=df.fecha.map(alert_status)
    filtro=st.selectbox("Ver mantenimientos",["Todos","🔴 Vencido","🟠 Próximo (30 días)","🟢 Programado"])
    if filtro!="Todos":df=df[df.alerta==filtro]
    st.dataframe(df,hide_index=True,use_container_width=True)
    st.download_button("📥 Exportar mantenimientos ficticios",df.to_csv(index=False).encode("utf-8-sig"),"mantenimientos_demo.csv","text/csv")

elif page=="📁 Documentos":
    st.title("Documentación técnica")
    st.caption("Ejemplo de cómo se vinculan documentos a los equipos. No se aceptan archivos reales.")
    docs=pd.DataFrame([dict(equipo="DEMO-001",tipo="Ficha técnica",documento="Ficha de ejemplo (no descargable)"),dict(equipo="DEMO-004",tipo="Reporte",documento="Reporte de ejemplo (no descargable)")])
    st.dataframe(docs,hide_index=True,use_container_width=True)
    st.info("La gestión documental con archivos reales solo se utiliza en el entorno privado de prueba y requiere controles de seguridad adicionales antes de ofrecerse comercialmente.")

elif page=="💳 Planes":
    st.title("Planes preliminares")
    st.warning("Precios hipotéticos para validar el interés del mercado; todavía no se venden suscripciones.")
    ofertas=[("Inicial","S/39 al mes","Inventario y consultas"),("Profesional","S/79 al mes","Mantenimiento y documentos"),("Organizaciones","Desde S/149 al mes","Varias cuentas, a definir en piloto")]
    for col,(nombre,precio,beneficio) in zip(st.columns(3),ofertas):
        with col:
            with st.container(border=True):
                st.subheader(nombre);st.markdown(f"### {precio}");st.write(beneficio);st.caption("Propuesta no contractual")
    st.info("La aplicación comercial necesita pruebas de seguridad, respaldos y restauración, soporte y condiciones de servicio antes de permitir contrataciones.")

st.divider()
st.caption("BioGestión · V10 · Demo pública aislada, sin Google Forms ni acceso a la base PostgreSQL privada.")

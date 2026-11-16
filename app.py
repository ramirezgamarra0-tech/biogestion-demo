"""BioGestión 8 · demostración pública sin base de datos ni credenciales."""
from datetime import date, timedelta
from io import BytesIO
import pandas as pd
import streamlit as st

st.set_page_config(page_title='BioGestión | Demostración', page_icon='🏥', layout='wide')
st.markdown('''<style>
[data-testid="stAppViewContainer"]{background:#f3f7fb}
[data-testid="stSidebar"]{background:#102b43}
[data-testid="stSidebar"] *{color:#f0f5fb}
[data-testid="stMetric"]{background:white;border-radius:13px;padding:17px;border:1px solid #dce6ee}
h1,h2,h3{color:#14344d}
</style>''',unsafe_allow_html=True)

today = date.today()
EQUIPOS = [
    dict(codigo='DEMO-001', nombre='Monitor multiparámetro', marca='Marca ficticia A', modelo='MP-100', ubicacion='Consultorio A', estado='Operativo'),
    dict(codigo='DEMO-002', nombre='Electrocardiógrafo', marca='Marca ficticia B', modelo='ECG-200', ubicacion='Consultorio B', estado='Operativo'),
    dict(codigo='DEMO-003', nombre='Bomba de infusión', marca='Marca ficticia C', modelo='BI-300', ubicacion='Almacén', estado='En mantenimiento'),
    dict(codigo='DEMO-004', nombre='Desfibrilador', marca='Marca ficticia D', modelo='DF-400', ubicacion='Emergencia', estado='Operativo'),
    dict(codigo='DEMO-005', nombre='Oxímetro de pulso', marca='Marca ficticia E', modelo='OX-500', ubicacion='Consultorio A', estado='Inoperativo'),
]
MANTENIMIENTOS = [
    dict(equipo='DEMO-001', tipo='Preventivo', fecha=(today + timedelta(days=12)).isoformat(), responsable='Técnico de ejemplo', estado='Programado'),
    dict(equipo='DEMO-003', tipo='Correctivo', fecha=(today - timedelta(days=3)).isoformat(), responsable='Técnico de ejemplo', estado='Programado'),
    dict(equipo='DEMO-004', tipo='Preventivo', fecha=(today + timedelta(days=28)).isoformat(), responsable='Técnico de ejemplo', estado='Programado'),
]
with st.sidebar:
    st.title('🏥 BioGestión')
    st.caption('Gestión de equipamiento biomédico')
    page=st.radio('Explorar la demostración', ['📊 Panel general','📋 Inventario','🛠️ Mantenimientos','📁 Documentos','💬 Solicitar demostración'])
    st.divider()
    st.caption('VERSIÓN 8.0 · DEMO PÚBLICA')
    st.info('Datos 100 % ficticios. Esta web no accede a ninguna base de datos ni guarda cambios.')

st.title('BioGestión · Demostración')
st.caption('Presentación interactiva para explorar el sistema sin información real de clínicas ni pacientes.')
st.warning('DEMO PÚBLICA · Datos simulados. No ingreses información personal ni de instituciones.')

df=pd.DataFrame(EQUIPOS)
if page.startswith('📊'):
    a,b,c,d=st.columns(4)
    a.metric('Equipos',len(df))
    b.metric('Operativos',int((df.estado=='Operativo').sum()))
    c.metric('En mantenimiento',int((df.estado=='En mantenimiento').sum()))
    d.metric('Inoperativos',int((df.estado=='Inoperativo').sum()))
    left,right=st.columns(2)
    with left:
        st.subheader('Equipos por estado')
        st.bar_chart(df.estado.value_counts(),horizontal=True)
    with right:
        st.subheader('Próximos mantenimientos')
        st.dataframe(pd.DataFrame(MANTENIMIENTOS),hide_index=True,use_container_width=True)
    st.subheader('Últimos equipos')
    st.dataframe(df[['codigo','nombre','ubicacion','estado']],hide_index=True,use_container_width=True)
elif page.startswith('📋'):
    st.header('Inventario biomédico')
    query=st.text_input('Buscar por equipo o código')
    states=st.multiselect('Filtrar por estado', sorted(df.estado.unique()),default=sorted(df.estado.unique()))
    filtered=df[df.estado.isin(states)]
    if query:
        mask=filtered[['codigo','nombre']].apply(lambda s:s.str.contains(query,case=False,regex=False)).any(axis=1)
        filtered=filtered[mask]
    st.dataframe(filtered,hide_index=True,use_container_width=True)
    st.download_button('📥 Descargar inventario de demostración (CSV)',filtered.to_csv(index=False).encode('utf-8-sig'),file_name='inventario_demo.csv',mime='text/csv')
    with st.expander('¿Qué permite la versión privada?'):
        st.write('Registro, edición, búsqueda y exportación de equipos; estas operaciones no están activadas en la demo pública.')
elif page.startswith('🛠️'):
    st.header('Programación de mantenimientos')
    md=pd.DataFrame(MANTENIMIENTOS)
    md['dias_hasta_fecha']=(pd.to_datetime(md['fecha']).dt.date.map(lambda x:(x-today).days))
    md['alerta']=md['dias_hasta_fecha'].map(lambda n:'Vencido' if n<0 else ('Próximo' if n<=30 else 'Programado'))
    st.dataframe(md[['equipo','tipo','fecha','responsable','estado','alerta']],hide_index=True,use_container_width=True)
    st.info('El módulo privado permite registrar y cerrar órdenes. La demo solo muestra datos ficticios.')
elif page.startswith('📁'):
    st.header('Documentación técnica')
    st.dataframe(pd.DataFrame([dict(equipo='DEMO-001',tipo='Ficha técnica',nombre='Ficha de ejemplo (no disponible)'),dict(equipo='DEMO-004',tipo='Reporte',nombre='Reporte de ejemplo (no disponible)')]),hide_index=True,use_container_width=True)
    st.info('Esta demostración no permite subir archivos y no contiene documentos reales.')
else:
    st.header('¿Te interesa utilizar BioGestión?')
    st.write('Esta página es una demostración técnica. Las funciones de gestión privada, gestión de cuentas y soporte requieren validaciones adicionales antes de su uso con clientes.')
    st.write('Para conocer el proyecto, solicita una demostración directamente al desarrollador por los medios que él indique fuera de esta versión.')
    st.caption('No se recopilan formularios, correos ni información personal desde esta página.')

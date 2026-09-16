import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(
    page_title="Gestor de Capacitación 70/20/10",
    page_icon="🎯",
    layout="wide"
)

# 2. Definición del Key User / Administrador
KEY_USER_EMAIL = "antonio.armendariz@innodep.com.mx"

# 3. Inicialización del Estado de Sesión (Session State)
if 'df_estructura' not in st.session_state:
    st.session_state['df_estructura'] = None

if 'df_recursos' not in st.session_state:
    st.session_state['df_recursos'] = None

if 'df_competencias' not in st.session_state:
    st.session_state['df_competencias'] = None

if 'user_email' not in st.session_state:
    st.session_state['user_email'] = ""

# 4. Barra Lateral: Identificación de Usuario y Logo
st.sidebar.title("👤 Identificación de Usuario")

user_email_input = st.sidebar.text_input(
    "Ingresa tu correo corporativo:", 
    value=st.session_state['user_email'],
    placeholder="ejemplo@empresa.com"
).strip().lower()

st.session_state['user_email'] = user_email_input

# Verificación de Rol
is_key_user = (user_email_input == KEY_USER_EMAIL.lower())

if user_email_input:
    if is_key_user:
        st.sidebar.success("🔑 Perfil: Key User (Antonio Armendariz)")
    else:
        st.sidebar.info("👤 Perfil: Usuario General")

# Carga de Logo (Visible para todos)
logo_file = st.sidebar.file_uploader("🖼️ Cargar Logo de la Empresa", type=["png", "jpg", "jpeg"])
if logo_file:
    st.sidebar.image(logo_file, use_container_width=True)

st.sidebar.markdown("---")

# 5. Sección de Parametrización (Carga de Plantillas - RESTRINGIDA SOLO AL KEY USER)
if is_key_user:
    st.sidebar.subheader("⚙️ Parametrización y Carga (Exclusivo Key User)")

    # Carga 1: Estructura
    file_est = st.sidebar.file_uploader("1. Plantilla de Estructura", type=["xlsx", "csv"], key="uploader_est")
    if file_est is not None:
        try:
            st.session_state['df_estructura'] = pd.read_excel(file_est) if file_est.name.endswith('.xlsx') else pd.read_csv(file_est)
            st.sidebar.success("✅ Estructura cargada")
        except Exception as e:
            st.sidebar.error(f"Error en Estructura: {e}")

    # Carga 2: Recursos 70/20/10
    file_rec = st.sidebar.file_uploader("2. Plantilla de Recursos 70/20/10", type=["xlsx", "csv"], key="uploader_rec")
    if file_rec is not None:
        try:
            st.session_state['df_recursos'] = pd.read_excel(file_rec) if file_rec.name.endswith('.xlsx') else pd.read_csv(file_rec)
            st.sidebar.success("✅ Recursos cargados")
        except Exception as e:
            st.sidebar.error(f"Error en Recursos: {e}")

    # Carga 3: Competencias
    file_comp = st.sidebar.file_uploader("3. Plantilla de Competencias", type=["xlsx", "csv"], key="uploader_comp")
    if file_comp is not None:
        try:
            st.session_state['df_competencias'] = pd.read_excel(file_comp) if file_comp.name.endswith('.xlsx') else pd.read_csv(file_comp)
            st.sidebar.success("✅ Competencias cargadas")
        except Exception as e:
            st.sidebar.error(f"Error en Competencias: {e}")

    # Botón para reiniciar datos cargados
    if st.sidebar.button("🔄 Reiniciar Datos"):
        st.session_state['df_estructura'] = None
        st.session_state['df_recursos'] = None
        st.session_state['df_competencias'] = None
        st.rerun()

elif user_email_input != "":
    st.sidebar.warning("🔒 La sección de Carga y Parametrización está restringida exclusivamente al Key User.")

# 6. Encabezado Principal y Visualización de Información
st.title("🎯 Sistema Integrado de Capacitación y Competencias")

if not user_email_input:
    st.warning("👈 Por favor, ingresa tu correo corporativo en el menú lateral para acceder al sistema.")
else:
    # Indicador de avance de carga
    c1, c2, c3 = st.columns(3)
    with c1:
        status_est = "🟢 Cargado" if st.session_state['df_estructura'] is not None else "🔴 Pendiente"
        st.metric("Plantilla Estructura", status_est)
    with c2:
        status_rec = "🟢 Cargado" if st.session_state['df_recursos'] is not None else "🔴 Pendiente"
        st.metric("Plantilla Recursos 70/20/10", status_rec)
    with c3:
        status_comp = "🟢 Cargado" if st.session_state['df_competencias'] is not None else "🔴 Pendiente"
        st.metric("Plantilla Competencias", status_comp)

    st.markdown("---")

    # Pestañas para visualizar cada plantilla almacenada
    tab_resumen, tab_est, tab_rec, tab_comp = st.tabs([
        "📊 Resumen Consolidado", 
        "🏗️ Estructura", 
        "📚 Recursos 70/20/10", 
        "💡 Competencias"
    ])

    # TAB 1: RESUMEN CONSOLIDADO
    with tab_resumen:
        st.subheader("📌 Vista General del Programa")
        if all([st.session_state['df_estructura'] is not None, 
                st.session_state['df_recursos'] is not None, 
                st.session_state['df_competencias'] is not None]):
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Total de Roles / Puestos", len(st.session_state['df_estructura']))
            m2.metric("Total de Recursos 70/20/10", len(st.session_state['df_recursos']))
            m3.metric("Total de Competencias", len(st.session_state['df_competencias']))
            
            st.success("🎉 Las tres plantillas han sido cargadas exitosamente y se encuentran consolidadas en memoria.")
        else:
            st.info("El Key User debe realizar la carga de las tres plantillas desde el menú lateral para ver el resumen consolidado.")

    # TAB 2: ESTRUCTURA
    with tab_est:
        st.subheader("🏗️ Datos de Estructura Organizacional")
        if st.session_state['df_estructura'] is not None:
            df_est = st.session_state['df_estructura']
            
            # Si no es Key User, filtrar solo sus datos o sus colaboradores a cargo
            if not is_key_user:
                df_filtered = df_est[
                    (df_est['correo_corporativo'].str.lower() == user_email_input) | 
                    (df_est['correo_gerente'].str.lower() == user_email_input)
                ]
                if not df_filtered.empty:
                    st.info(f"Mostrando datos correspondientes a: **{user_email_input}**")
                    st.dataframe(df_filtered, use_container_width=True)
                else:
                    st.warning("No se encontraron registros vinculados a este correo corporativo.")
            else:
                st.dataframe(df_est, use_container_width=True)
        else:
            st.warning("Aún no se ha cargado la plantilla de Estructura.")

    # TAB 3: RECURSOS
    with tab_rec:
        st.subheader("📚 Catálogo de Recursos 70/20/10")
        if st.session_state['df_recursos'] is not None:
            st.dataframe(st.session_state['df_recursos'], use_container_width=True)
        else:
            st.warning("Aún no se ha cargado la plantilla de Recursos.")

    # TAB 4: COMPETENCIAS
    with tab_comp:
        st.subheader("💡 Modelo de Competencias")
        if st.session_state['df_competencias'] is not None:
            st.dataframe(st.session_state['df_competencias'], use_container_width=True)
        else:
            st.warning("Aún no se ha cargado la plantilla de Competencias.")
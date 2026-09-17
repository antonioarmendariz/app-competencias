import pandas as pd
import streamlit as st

# Configuración inicial de la página
st.set_page_config(
    page_title='Gestor de Capacitación 70/20/10 y Competencias',
    page_icon='🎯',
    layout='wide',
)

# Constantes de configuración
KEY_USER_EMAIL = 'antonio.armendariz@innodep.com.mx'

# Inicializar estados en memoria si no existen
if 'df_estructura' not in st.session_state:
  st.session_state.df_estructura = None
if 'df_recursos' not in st.session_state:
  st.session_state.df_recursos = None
if 'df_competencias' not in st.session_state:
  st.session_state.df_competencias = None
if 'respuestas_usuario' not in st.session_state:
  st.session_state.respuestas_usuario = {}

# --- BARRA LATERAL: IDENTIFICACIÓN Y CONFIGURACIÓN ---
st.sidebar.markdown('## 👤 Identificación de Usuario')
email_ingresado = st.sidebar.text_input(
    'Ingresa tu correo corporativo:', value='antonio.armendariz@innodep.com.mx'
)

# Validación de roles
es_key_user = (
    email_ingresado.strip().lower() == KEY_USER_EMAIL.lower()
    if email_ingresado
    else False
)

if es_key_user:
  st.sidebar.success(f'Perfil: Key User (Antonio Armendariz)')
else:
  st.sidebar.info('Perfil: Usuario General')

st.sidebar.markdown('---')
st.sidebar.markdown('🖼️ Cargar Logo de la Empresa')
logo_file = st.sidebar.file_uploader(
    '', type=['png', 'jpg', 'jpeg'], key='logo_uploader'
)
if logo_file:
  st.sidebar.image(logo_file, width=150)

st.sidebar.markdown('---')

# --- PANEL DE CARGA (EXCLUSIVO KEY USER) ---
if es_key_user:
  st.sidebar.markdown('### ⚙️ Parametrización y Carga')
  st.sidebar.markdown('*Exclusivo Key User*')

  file_estructura = st.sidebar.file_uploader(
      '1. Plantilla de Estructura', type=['xlsx', 'xls']
  )
  if file_estructura:
    st.session_state.df_estructura = pd.read_excel(file_estructura)

  file_recursos = st.sidebar.file_uploader(
      '2. Plantilla Recursos 70/20/10', type=['xlsx', 'xls']
  )
  if file_recursos:
    st.session_state.df_recursos = pd.read_excel(file_recursos)

  file_competencias = st.sidebar.file_uploader(
      '3. Plantilla Competencias', type=['xlsx', 'xls']
  )
  if file_competencias:
    st.session_state.df_competencias = pd.read_excel(file_competencias)
else:
  st.sidebar.markdown(
      '🔒 *La sección de Carga y Parametrización está restringida'
      ' exclusivamente al Key User.*'
  )

# --- VERIFICACIÓN DE DATOS CARGADOS ---
archivos_cargados = (
    st.session_state.df_estructura is not None
    and st.session_state.df_recursos is not None
    and st.session_state.df_competencias is not None
)

# --- CUERPO PRINCIPAL ---
st.markdown(
    '# 🎯 Sistema Integrado de Capacitación y Competencias'
    ' #s'
)

if not archivos_cargados:
  st.warning(
      '⚠️ Por favor, espera a que el Key User cargue las plantillas maestras'
      ' correspondientes en el sistema para habilitar las vistas y el'
      ' diagnóstico #s.'
  )
else:
  # Indicadores visuales de estado de archivos
  col_s1, col_s2, col_s3 = st.columns(3)
  with col_s1:
    st.success('✅ Plantilla Estructura: Cargada')
  with col_s2:
    st.success('✅ Plantilla Recursos: Cargada')
  with col_s3:
    st.success('✅ Plantilla Competencias: Cargada')

  st.markdown('---')

  if es_key_user:
    # --- VISTA DE KEY USER / ADMINISTRACIÓN ---
    tab_resumen, tab_est, tab_rec, tab_comp = st.tabs([
        '📊 Resumen Consolidado',
        '🏢 Estructura',
        '📈 Recursos 70/20/10',
        '💡 Competencias',
    ])

    with tab_resumen:
      st.markdown('### 📌 Vista General del Programa')
      c1, c2, c3 = st.columns(3)
      c1.metric(
          'Total de Roles / Puestos',
          len(st.session_state.df_estructura),
      )
      c2.metric(
          'Total de Recursos 70/20/10',
          len(st.session_state.df_recursos),
      )
      c3.metric(
          'Total de Competencias',
          len(st.session_state.df_competencias),
      )
      st.success(
          '🎉 Las tres plantillas han sido cargadas exitosamente y se'
          ' encuentran consolidadas en memoria #s.'
      )

    with tab_est:
      st.markdown('### 🏢 Estructura Organizacional')
      st.dataframe(st.session_state.df_estructura, use_container_width=True)

    with tab_rec:
      st.markdown('### 📈 Recursos de Capacitación 70/20/10')
      st.dataframe(st.session_state.df_recursos, use_container_width=True)

    with tab_comp:
      st.markdown('### 💡 Modelo de Competencias')
      st.dataframe(st.session_state.df_competencias, use_container_width=True)

  else:
    # --- VISTA DE USUARIO GENERAL / AUTODIAGNÓSTICO Y GRÁFICOS ---
    tab_diag, tab_res = st.tabs(
        ['📝 Realizar Autodiagnóstico', '📊 Mis Resultados y Gráficos']
    )

    with tab_diag:
      st.markdown(
          '### 📝 Evaluación de Competencias'
          ' #s'
      )
      st.write(
          'Selecciona tu nivel actual de dominio para cada una de las'
          ' competencias establecidas en tu perfil #s.'
      )

      df_comp = st.session_state.df_competencias
      # Iterar sobre las competencias para el formulario
      respuestas_temp = {}
      for idx, row in df_comp.iterrows():
        comp_nombre = (
            row.get('Competencia')
            or row.get('Nombre')
            or f'Competencia {idx+1}'
        )
        desc = row.get('Descriptor general', 'Sin descripción')

        st.markdown(f'**{idx+1}. {comp_nombre}**')
        st.caption(f'*{desc}*')

        # Selector de nivel (Escala del 1 al 4 o descriptiva)
        nivel_seleccionado = st.radio(
            f'Nivel de dominio para: {comp_nombre}',
            options=[
                '1 - En Desarrollo',
                '2 - Básico',
                '3 - Competente',
                '4 - Avanzado / Expert',
            ],
            key=f'resp_{idx}',
            horizontal=True,
        )
        respuestas_temp[comp_nombre] = int(nivel_seleccionado[0])
        st.markdown('---')

      if st.button('💾 Guardar y Enviar Autodiagnóstico', type='primary'):
        st.session_state.respuestas_usuario = respuestas_temp
        st.success(
            '¡Tus respuestas han sido guardadas exitosamente en memoria! Ve a'
            ' la pestaña "Mis Resultados y Gráficos" para visualizar tu'
            ' reporte.'
        )

    with tab_res:
      st.markdown('### 📊 Reporte Visual de Resultados')

      if not st.session_state.respuestas_usuario:
        st.info(
            '⚠️ Aún no has completado tu autodiagnóstico. Por favor ve a la'
            ' pestaña anterior, responde la evaluación y haz clic en guardar.'
        )
      else:
        # Convertir respuestas a DataFrame para graficar
        df_resultados = pd.DataFrame(
            list(st.session_state.respuestas_usuario.items()),
            columns=['Competencia', 'Nivel'],
        )

        col_g1, col_g2 = st.columns([1, 1])

        with col_g1:
          st.markdown('#### Detalle de Puntuaciones')
          st.dataframe(df_resultados, use_container_width=True)

        with col_g2:
          st.markdown('#### Gráfica de Dominio por Competencia')
          # Gráfico de barras nativo de Streamlit
          st.bar_chart(
              df_resultados.set_index('Competencia'),
              color='#1f77b4',
          )

        st.metric(
            'Promedio General de Competencias',
            f"{df_resultados['Nivel'].mean():.2f} / 4.0",
        )
        st.success(
            '✨ Diagnóstico completado y analizado gráficamente con éxito.'
        )

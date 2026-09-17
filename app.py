import pandas as pd
import plotly.express as px
import streamlit as st

# Configuración inicial de la página
st.set_page_config(
    page_title='Sistema Integrado de Capacitación 70/20/10 y Competencias',
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
if 'journey_firmado' not in st.session_state:
  st.session_state.journey_firmado = False

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
  st.sidebar.success(
      'Perfil: Key User (Antonio Armendariz)'
      ' #s'
  )
else:
  st.sidebar.info('Perfil: Usuario General #s')

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
  st.sidebar.markdown('*Exclusivo Key User* #s')

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
      ' exclusivamente al Key User.* #s'
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
    st.success('✅ Plantilla Estructura: Cargada #s')
  with col_s2:
    st.success('✅ Plantilla Recursos: Cargada #s')
  with col_s3:
    st.success('✅ Plantilla Competencias: Cargada #s')

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
      st.markdown('### 📌 Vista General del Programa #s')
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
      st.markdown('### 🏢 Estructura Organizacional #s')
      st.dataframe(st.session_state.df_estructura, use_container_width=True)

    with tab_rec:
      st.markdown('### 📈 Recursos de Capacitación 70/20/10 #s')
      st.dataframe(st.session_state.df_recursos, use_container_width=True)

    with tab_comp:
      st.markdown('### 💡 Modelo de Competencias #s')
      st.dataframe(st.session_state.df_competencias, use_container_width=True)

  else:
    # --- VISTA DE USUARIO GENERAL / AUTODIAGNÓSTICO, JOURNEY Y RESULTADOS ---
    tab_diag, tab_journey, tab_res = st.tabs([
        '📝 Autodiagnóstico de Competencias',
        '🚀 Journey de Desarrollo Visual y Firma',
        '📊 Mis Resultados y Gráfico Spider',
    ])

    with tab_diag:
      st.markdown('### 📝 Evaluación y Autodiagnóstico #s')
      st.write(
          'Completa los datos de identificación y evalúa tu nivel de dominio'
          ' basándote en los descriptores de cada nivel #s.'
      )

      # Campos de identificación del colaborador y su gerente
      col_id1, col_id2 = st.columns(2)
      with col_id1:
        nombre_colaborador = st.text_input(
            'Nombre del Colaborador:', value='Antonio Armendariz'
        )
      with col_id2:
        nombre_gerente = st.text_input(
            'Nombre del Gerente / Líder:', value='Gerente Directo'
        )

      st.markdown('---')

      df_comp = st.session_state.df_competencias
      respuestas_temp = {}

      for idx, row in df_comp.iterrows():
        comp_nombre = (
            row.get('Competencia')
            or row.get('Nombre')
            or f'Competencia {idx+1}'
        )
        desc_gral = row.get(
            'Descriptor general', 'Sin descripción general disponible'
        )

        nivel_basico = row.get(
            'Nivel Básico', row.get('Básico', 'Describir nivel básico...')
        )
        nivel_intermedio = row.get(
            'Nivel Intermedio',
            row.get('Intermedio', 'Describir nivel intermedio...'),
        )
        nivel_avanzado = row.get(
            'Nivel Avanzado',
            row.get('Avanzado', 'Describir nivel avanzado...'),
        )

        st.markdown(f'#### {idx+1}. {comp_nombre}')
        st.info(f'**Descriptor General:** {desc_gral}')

        with st.expander(
            f'📖 Ver detalles de niveles para: {comp_nombre}'
            ' #s'
        ):
          st.markdown(f'- **Nivel 1 (Básico):** {nivel_basico}')
          st.markdown(f'- **Nivel 2 (Intermedio):** {nivel_intermedio}')
          st.markdown(f'- **Nivel 3 (Avanzado):** {nivel_avanzado}')

        nivel_evaluado = st.radio(
            f'Selecciona tu nivel alcanzado en: {comp_nombre}',
            options=[
                '1 - Básico',
                '2 - Intermedio',
                '3 - Avanzado / Experto',
            ],
            key=f'resp_comp_{idx}',
            horizontal=True,
        )

        respuestas_temp[comp_nombre] = int(nivel_evaluado[0])
        st.markdown('---')

      if st.button('💾 Guardar Autodiagnóstico y Generar Reporte', type='primary'):
        st.session_state.respuestas_usuario = respuestas_temp
        st.session_state.nombre_colaborador = nombre_colaborador
        st.session_state.nombre_gerente = nombre_gerente
        st.success(
            '¡Evaluación guardada con éxito! Ya puedes revisar tu Journey y el'
            ' Gráfico Spider en las pestañas superiores #s.'
        )

    with tab_journey:
      st.markdown('### 🚀 Journey de Desarrollo 70/20/10 (Ruta Visual) #s')
      st.write(
          'Este es tu plan de desarrollo interactivo estructurado bajo el'
          ' modelo 70/20/10 para potenciar tus competencias #s.'
      )

      colab = st.session_state.get(
          'nombre_colaborador', 'Antonio Armendariz'
      )
      ger = st.session_state.get('nombre_gerente', 'Gerente Asignado')
      st.info(
          f'👤 **Colaborador:** {colab} &nbsp;&nbsp;|&nbsp;&nbsp; 👔'
          f' **Gerente Responsable:** {ger}'
      )
      st.markdown('---')

      # Renderizado visual en tarjetas por pilar 70/20/10
      c70, c20, c10 = st.columns(3)

      with c70:
        st.markdown('#### 🛠️ 70% Experiencia en el Puesto')
        st.markdown(
            'Acciones prácticas, asignación de proyectos complejos, retos y'
            ' aprendizaje on-the-job.'
        )
        st.success(
            '• Liderar iniciativa clave en área.\n• Rotación de funciones'
            ' operativas.'
        )

      with c20:
        st.markdown('#### 👥 20% Exposición y Mentoría')
        st.markdown(
            'Feedback continuo, sesiones de coaching con tu gerente y redes de'
            ' colaboración.'
        )
        st.warning(
            '• Sesiones de retroalimentación 1o1.\n• Mentoría con Key User o'
            ' experto.'
        )

      with c10:
        st.markdown('#### 📚 10% Formación Estructurada')
        st.markdown(
            'Cursos formales, lectura de marcos teóricos, certificaciones y'
            ' talleres especializados.'
        )
        st.info(
            '• Cursos de especialización técnica.\n• Lectura de guías y'
            ' normativas.'
        )

      st.markdown('---')
      st.markdown('### ✍️ Validación y Firma Digital del Journey')

      col_f1, col_f2 = st.columns(2)
      with col_f1:
        firma_colab = st.checkbox(
            f'Acepto y valido mi plan de desarrollo ({colab})',
            value=st.session_state.journey_firmado,
        )
      with col_f2:
        firma_gerente = st.checkbox(
            f'Aprobar plan de desarrollo como líder/gerente ({ger})',
            value=st.session_state.journey_firmado,
        )

      if firma_colab and firma_gerente:
        st.session_state.journey_firmado = True
        st.success(
            '✅ **¡Journey Firmado y Validado Exitosamente por Ambas Partes!**'
            ' El plan está oficialmente activo en el sistema.'
        )
      else:
        st.warning(
            '⚠️ Ambas partes (Colaborador y Gerente) deben marcar la casilla'
            ' de aceptación para formalizar la firma del Journey.'
        )

    with tab_res:
      st.markdown('### 📊 Reporte de Resultados y Gráfico Spider #s')

      if not st.session_state.respuestas_usuario:
        st.warning(
            '⚠️ Aún no has completado tu autodiagnóstico en la primera pestaña.'
        )
      else:
        colab = st.session_state.get(
            'nombre_colaborador', 'Colaborador General'
        )
        ger = st.session_state.get('nombre_gerente', 'Gerente Asignado')

        st.markdown(
            f'**Evaluación de:** {colab} &nbsp;&nbsp;|&nbsp;&nbsp; **Revisado'
            f' por:** {ger}'
        )
        st.markdown('---')

        df_resultados = pd.DataFrame(
            list(st.session_state.respuestas_usuario.items()),
            columns=['Competencia', 'Nivel'],
        )

        col_r1, col_r2 = st.columns([1, 1.2])

        with col_r1:
          st.markdown('#### Detalle de Puntuaciones #s')
          st.dataframe(df_resultados, use_container_width=True)
          promedio = df_resultados['Nivel'].mean()
          st.metric('Promedio General de Dominio', f'{promedio:.2f} / 3.0')
          if st.session_state.journey_firmado:
            st.success('🔒 Estatus: Journey Firmado y Validado')
          else:
            st.warning('🔓 Estatus: Pendiente de Firmar Journey')

        with col_r2:
          st.markdown('#### 🕸️ Gráfico Spider (Radar de Competencias) #s')
          fig = px.line_polar(
              df_resultados,
              r='Nivel',
              theta='Competencia',
              line_close=True,
              range_r=[0, 3],
          )
          fig.update_traces(fill='toself', line_color='#1f77b4')
          fig.update_layout(
              polar=dict(radialaxis=dict(visible=True, range=[0, 3])),
              showlegend=False,
          )
          st.plotly_chart(fig, use_container_width=True)

        st.success(
            '✨ Gráfico Spider generado correctamente con base en tus'
            ' respuestas evaluadas #s.'
        )

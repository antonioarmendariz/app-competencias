import pandas as pd
import plotly.express as px
import streamlit as st

# Configuración inicial de la página
st.set_page_config(
    page_title='Sistema de Gestión De Desarrollo de Talento INNODEP SC',
    page_icon='🎯',
    layout='wide',
)

# --- APLICACIÓN DE PALETA DE COLORES CORPORATIVA CON ALTO CONTRASTE ---
st.markdown(
    """
    <style>
    /* Estilos globales y tipografía de alto contraste */
    .stApp {
        background-color: #FFFFFF;
        color: #2F3F47;
    }
    
    /* Encabezados y títulos principales */
    h1, h2, h3, h4, h5, h6 {
        color: #2F3F47 !important;
        font-weight: 700;
    }
    
    /* Texto general, párrafos y etiquetas en el cuerpo */
    p, span, label, .stMarkdown, div {
        color: #2F3F47;
    }
    
    /* Botones principales de acción */
    .stButton>button {
        background-color: #62D5B1 !important;
        color: #2F3F47 !important;
        font-weight: bold;
        border: none;
        border-radius: 6px;
    }
    .stButton>button:hover {
        background-color: #FF7600 !important;
        color: #FFFFFF !important;
    }
    
    /* Estilo limpio para los cargadores de archivos en el Sidebar */
    [data-testid="stSidebar"] [data-testid="stFileUploader"] section {
        background-color: #62D5B1 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px !important;
    }
    [data-testid="stSidebar"] [data-testid="stFileUploader"] section * {
        color: #2F3F47 !important;
    }
    [data-testid="stSidebar"] [data-testid="stFileUploader"] button {
        background-color: #FFFFFF !important;
        color: #2F3F47 !important;
        border: none !important;
        font-weight: bold !important;
        border-radius: 4px !important;
    }
    [data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="stUploadedFile"] {
        background-color: #FFFFFF !important;
        border-radius: 6px !important;
    }
    [data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="stUploadedFile"] span,
    [data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="stUploadedFile"] small {
        color: #2F3F47 !important;
    }
    
    /* Sidebar: Fondo oscuro institucional con forzado estricto de texto blanco */
    [data-testid="stSidebar"] {
        background-color: #2F3F47;
    }
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] div {
        color: #FFFFFF !important;
    }
    
    /* Inputs de texto en sidebar para asegurar legibilidad */
    [data-testid="stSidebar"] input {
        color: #2F3F47 !important;
        background-color: #FFFFFF !important;
    }
    
    /* Métricas y tarjetas de estado */
    [data-testid="stMetricValue"] {
        color: #FF7600 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #2F3F47 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Credenciales de acceso y gestión en session_state para permitir cambios
KEY_USER_EMAIL = 'antonio.armendariz@innodep.com.mx'
if 'key_user_password' not in st.session_state:
  st.session_state.key_user_password = 'admin2026'

# Control de sesión activa
if 'sesion_iniciada' not in st.session_state:
  st.session_state.sesion_iniciada = False
if 'es_key_user' not in st.session_state:
  st.session_state.es_key_user = False
if 'email_actual' not in st.session_state:
  st.session_state.email_actual = ''

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


# Función auxiliar para extraer Nombre y Apellido desde el correo o texto
def obtener_nombre_apellido(email):
  try:
    nombre_base = email.split('@')[0]
    partes = nombre_base.replace('.', ' ').replace('_', ' ').split()
    if len(partes) >= 2:
      return f'{partes[0].capitalize()} {partes[1].capitalize()}'
    elif len(partes) == 1:
      return partes[0].capitalize()
    return email
  except Exception:
    return email


# --- BARRA LATERAL: IDENTIFICACIÓN Y ACCESO ORDENADO ---
st.sidebar.markdown('## 👤 Acceso al Sistema')

if st.session_state.sesion_iniciada:
  nombre_formateado = obtener_nombre_apellido(st.session_state.email_actual)
  st.sidebar.success(f'Sesión activa como: **{nombre_formateado}**')
  if st.sidebar.button('🚪 Cerrar sesión'):
    st.session_state.sesion_iniciada = False
    st.session_state.es_key_user = False
    st.session_state.email_actual = ''
    st.rerun()
  st.sidebar.markdown('---')
else:
  email_ingresado = st.sidebar.text_input(
      'Correo corporativo:',
      value='antonio.armendariz@innodep.com.mx',
      key='email_ingresado_temp',
  )
  password_ingresado = st.sidebar.text_input(
      'Contraseña:', type='password', value='', key='password_ingresado_temp'
  )

  if st.sidebar.button('🔑 Ingresar al Sistema'):
    email_limpio = email_ingresado.strip().lower()
    if email_limpio == KEY_USER_EMAIL.lower():
      if password_ingresado == st.session_state.key_user_password:
        st.session_state.sesion_iniciada = True
        st.session_state.es_key_user = True
        st.session_state.email_actual = email_ingresado
        st.sidebar.success('¡Acceso concedido como Key User!')
        st.rerun()
      else:
        st.sidebar.error('Contraseña de Key User incorrecta.')
    else:
      if len(email_limpio) > 5 and len(password_ingresado) > 0:
        st.session_state.sesion_iniciada = True
        st.session_state.es_key_user = False
        st.session_state.email_actual = email_ingresado
        st.sidebar.success('¡Acceso concedido como Usuario General!')
        st.rerun()
      else:
        st.sidebar.warning(
            'Ingresa un correo válido y una contraseña para continuar.'
        )

  st.sidebar.markdown('---')

# Asignar variables de control actuales
es_key_user = st.session_state.es_key_user
acceso_concedido = st.session_state.sesion_iniciada

# --- PANEL DE PERSONALIZACIÓN Y CARGA (EXCLUSIVO KEY USER) ---
if acceso_concedido and es_key_user:
  st.sidebar.markdown('### 🖼️ Identidad Visual')

  logo_file = st.sidebar.file_uploader(
      'Cargar Logo Empresa', type=['png', 'jpg', 'jpeg'], key='logo_upload'
  )
  if logo_file:
    st.sidebar.image(logo_file, width=160, caption='Logotipo de la Empresa')
  else:
    st.sidebar.markdown(
        '🏢 *Logo por defecto:* **INNODEP S.C. / DECIDO** (Sube una imagen para'
        ' reemplazarlo)'
    )

  st.sidebar.markdown('---')
  st.sidebar.markdown('### ⚙️ Parametrización y Carga')
  st.sidebar.markdown('*Exclusivo Key User*')

  file_estructura = st.sidebar.file_uploader(
      '1. Plantilla de Estructura', type=['xlsx', 'xls'], key='f_est'
  )
  file_recursos = st.sidebar.file_uploader(
      '2. Plantilla Recursos 70/20/10', type=['xlsx', 'xls'], key='f_rec'
  )
  file_competencias = st.sidebar.file_uploader(
      '3. Plantilla Competencias', type=['xlsx', 'xls'], key='f_comp'
  )

  if st.sidebar.button('💾 Guardar Cambios de Plantillas'):
    cambios_realizados = False
    if file_estructura is not None:
      st.session_state.df_estructura = pd.read_excel(file_estructura)
      cambios_realizados = True
    if file_recursos is not None:
      st.session_state.df_recursos = pd.read_excel(file_recursos)
      cambios_realizados = True
    if file_competencias is not None:
      st.session_state.df_competencias = pd.read_excel(file_competencias)
      cambios_realizados = True

    if cambios_realizados:
      st.sidebar.success('¡Plantillas guardadas y actualizadas con éxito!')
    else:
      st.sidebar.warning(
          'Por favor selecciona al menos un archivo para guardar cambios.'
      )

  st.sidebar.markdown('---')
  with st.sidebar.expander('⚙️ Settings / Cambiar Contraseña'):
    pass_actual = st.text_input(
        'Contraseña Actual:', type='password', key='p_act'
    )
    pass_nuevo = st.text_input(
        'Nueva Contraseña:', type='password', key='p_new'
    )
    if st.button('Actualizar Contraseña'):
      if pass_actual == st.session_state.key_user_password:
        if len(pass_nuevo) >= 4:
          st.session_state.key_user_password = pass_nuevo
          st.sidebar.success(
              '¡Contraseña actualizada con éxito! Úsala en tu próximo acceso.'
          )
        else:
          st.sidebar.error(
              'La nueva contraseña debe tener al menos 4 caracteres.'
          )
      else:
        st.sidebar.error('La contraseña actual es incorrecta.')
elif acceso_concedido and not es_key_user:
  st.sidebar.markdown('🔒 *Sección de administración restringida al Key User.*')
else:
  st.sidebar.markdown(
      '🔒 *Inicia sesión con tus credenciales para habilitar los paneles.*'
  )

# --- VERIFICACIÓN DE DATOS CARGADOS ---
archivos_cargados = (
    st.session_state.df_estructura is not None
    and st.session_state.df_recursos is not None
    and st.session_state.df_competencias is not None
)

# --- CUERPO PRINCIPAL ---
st.markdown('# 🎯 Sistema de Gestión De Desarrollo de Talento INNODEP SC')

if not acceso_concedido:
  st.warning(
      '⚠️ Por favor, ingresa tu correo y contraseña en la barra lateral y'
      ' presiona **"Ingresar al Sistema"** para comenzar.'
  )
elif not archivos_cargados:
  st.warning(
      '⚠️ El acceso es correcto, pero espera a que el Key User cargue y'
      ' guarde las plantillas maestras en el sistema para habilitar las'
      ' vistas y el diagnóstico.'
  )
else:
  estilo_caja_verde = (
      'background-color: #E6F8F2; padding: 16px; border-radius: 8px;'
      ' border: 1px solid #62D5B1; min-height: 90px; display: flex;'
      ' align-items: center;'
  )

  col_s1, col_s2, col_s3 = st.columns(3)
  with col_s1:
    st.markdown(
        f'<div style="{estilo_caja_verde}">✅ <b>Plantilla Estructura:</b>'
        ' Cargada</div>',
        unsafe_allow_html=True,
    )
  with col_s2:
    st.markdown(
        f'<div style="{estilo_caja_verde}">✅ <b>Plantilla Recursos:</b>'
        ' Cargada</div>',
        unsafe_allow_html=True,
    )
  with col_s3:
    st.markdown(
        f'<div style="{estilo_caja_verde}">✅ <b>Plantilla Competencias:</b>'
        ' Cargada</div>',
        unsafe_allow_html=True,
    )

  st.markdown('<br>', unsafe_allow_html=True)

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
          'Total de Roles / Puestos', len(st.session_state.df_estructura)
      )
      c2.metric(
          'Total de Recursos 70/20/10', len(st.session_state.df_recursos)
      )
      c3.metric(
          'Total de Competencias', len(st.session_state.df_competencias)
      )
      st.success(
          '🎉 Las tres plantillas han sido cargadas exitosamente y se'
          ' encuentran consolidadas en memoria.'
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
    # --- VISTA DE USUARIO GENERAL / AUTODIAGNÓSTICO, RUTA Y RESULTADOS ---
    tab_diag, tab_journey, tab_res = st.tabs([
        '📝 Autodiagnóstico de Competencias',
        '🚀 Ruta de Desarrollo 70/20/10',
        '📊 Mis Resultados y Gráfico Spider',
    ])

    with tab_diag:
      st.markdown('### 📝 Evaluación y Autodiagnóstico')
      st.write(
          'Completa los datos de identificación y evalúa tu nivel de dominio'
          ' basándote en los descriptores de cada nivel.'
      )

      col_id1, col_id2 = st.columns(2)
      with col_id1:
        nombre_colaborador = st.text_input(
            'Nombre del Colaborador:',
            value=obtener_nombre_apellido(st.session_state.email_actual),
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
            'Nivel Avanzado', row.get('Avanzado', 'Describir nivel avanzado...')
        )

        st.markdown(f'#### {idx+1}. {comp_nombre}')
        st.info(f'**Descriptor General:** {desc_gral}')

        with st.expander(f'📖 Ver detalles de niveles para: {comp_nombre}'):
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

      if st.button(
          '💾 Guardar Autodiagnóstico y Generar Reporte', type='primary'
      ):
        st.session_state.respuestas_usuario = respuestas_temp
        st.session_state.nombre_colaborador = nombre_colaborador
        st.session_state.nombre_gerente = nombre_gerente
        st.success(
            '¡Evaluación guardada con éxito! Ya puedes revisar tu Ruta de'
            ' Desarrollo y el Gráfico Spider en las pestañas superiores.'
        )

    with tab_journey:
      st.markdown('### 🚀 Ruta de Desarrollo 70/20/10')
      st.write(
          'Matriz estructurada de acciones de desarrollo para tus áreas de'
          ' oportunidad. Puedes revisar y editar los objetivos de 70%,'
          ' 20% y 10% antes de validar y firmar el plan definitivo.'
      )

      colab = st.session_state.get(
          'nombre_colaborador',
          obtener_nombre_apellido(st.session_state.email_actual),
      )
      ger = st.session_state.get('nombre_gerente', 'Gerente Asignado')
      st.info(
          f'👤 **Colaborador:** {colab} &nbsp;&nbsp;|&nbsp;&nbsp; 👔'
          f' **Gerente Responsable:** {ger}'
      )
      st.markdown('---')

      if not st.session_state.respuestas_usuario:
        st.warning(
            '⚠️ Para configurar la Ruta de Desarrollo, por favor completa'
            ' primero tu **Autodiagnóstico de Competencias** en la primera'
            ' pestaña y haz clic en Guardar.'
        )
      else:
        competencias_a_desarrollar = [
            comp
            for comp, nivel in st.session_state.respuestas_usuario.items()
            if nivel < 3
        ]

        if not competencias_a_desarrollar:
          st.success(
              '🎉 ¡Felicidades! Has alcanzado el nivel avanzado en todas tus'
              ' competencias evaluadas. Tu enfoque se centrará en mentoría'
              ' avanzada y proyectos de innovación.'
          )
        else:
          if 'acciones_matriz' not in st.session_state:
            st.session_state.acciones_matriz = {}

          datos_matriz = []
          for comp in competencias_a_desarrollar:
            nivel_actual = st.session_state.respuestas_usuario[comp]
            nivel_texto = (
                'Básico (Nivel 1)'
                if nivel_actual == 1
                else 'Intermedio (Nivel 2)'
            )

            # Recuperar o inicializar valores en memoria
            defaults = st.session_state.acciones_matriz.get(
                comp,
                {
                    '70': (
                        f'Liderar proyecto o reto práctico on-the-job en'
                        f' {comp}.'
                    ),
                    '20': f'Sesión de mentoría y feedback 1o1 con {ger}.',
                    '10': f'Revisión de guías técnicas o curso digital sobre {comp}.',
                },
            )

            st.markdown(
                f'#### 🎯 {comp} &nbsp;&nbsp;|&nbsp;&nbsp; Nivel Actual:'
                f' **{nivel_texto}**'
            )
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
              obj_70 = st.text_area(
                  f'🛠️ 70% Experiencia ({comp}):',
                  value=defaults['70'],
                  key=f'mat_70_{comp}',
                  height=80,
              )
            with col_m2:
              obj_20 = st.text_area(
                  f'👥 20% Exposición ({comp}):',
                  value=defaults['20'],
                  key=f'mat_20_{comp}',
                  height=80,
              )
            with col_m3:
              obj_10 = st.text_area(
                  f'📚 10% Formación ({comp}):',
                  value=defaults['10'],
                  key=f'mat_10_{comp}',
                  height=80,
              )

            st.session_state.acciones_matriz[comp] = {
                '70': obj_70,
                '20': obj_20,
                '10': obj_10,
            }
            st.markdown('---')

      st.markdown('### ✍️ Validación y Firma Digital del Plan')

      col_f1, col_f2 = st.columns(2)
      with col_f1:
        firma_colab = st.checkbox(
            f'Acepto y valido mi ruta de desarrollo ({colab})',
            value=st.session_state.journey_firmado,
        )
      with col_f2:
        firma_gerente = st.checkbox(
            f'Aprobar ruta como líder/gerente ({ger})',
            value=st.session_state.journey_firmado,
        )

      if firma_colab and firma_gerente:
        st.session_state.journey_firmado = True
        st.success(
            '✅ **¡Ruta de Desarrollo Validada y Firmada Exitosamente por'
            ' Ambas Partes!**'
        )
      else:
        st.warning(
            '⚠️ Ambas partes deben marcar la casilla de aceptación para'
            ' formalizar la firma definitiva.'
        )

    with tab_res:
      st.markdown(
          '### 📊 Reporte de Resultados, Matriz Consolidada y Gráfico Spider'
      )

      if not st.session_state.respuestas_usuario:
        st.warning(
            '⚠️ Aún no has completado tu autodiagnóstico en la primera pestaña.'
        )
      else:
        colab = st.session_state.get(
            'nombre_colaborador',
            obtener_nombre_apellido(st.session_state.email_actual),
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

        # 1. MATRIZ CONSOLIDADA ARRIBA
        st.markdown('#### 📋 Matriz Consolidada de Puntuaciones y Estatus')
        promedio = df_resultados['Nivel'].mean()
        col_m_info1, col_m_info2 = st.columns(2)
        with col_m_info1:
          st.metric(
              'Promedio General de Dominio', f'{promedio:.2f} / 3.0'
          )
        with col_m_info2:
          if st.session_state.journey_firmado:
            st.success('🔒 Estatus: Ruta Validada y Firmada')
          else:
            st.warning('🔓 Estatus: Pendiente de Validar y Firmar')

        st.dataframe(df_resultados, use_container_width=True)
        st.markdown('---')

        # 2. SELECTOR TIPO LISTBOX PARA COMPETENCIAS EN EL GRÁFICO
        st.markdown('#### 🕸️ Gráfico Spider (Radar de Competencias)')
        todas_competencias = df_resultados['Competencia'].tolist()
        competencias_seleccionadas = st.multiselect(
            'Selecciona las competencias a visualizar en el gráfico de'
            ' radar:',
            options=todas_competencias,
            default=todas_competencias,
        )

        if competencias_seleccionadas:
          df_filtrado = df_resultados[
              df_resultados['Competencia'].isin(competencias_seleccionadas)
          ]
          fig = px.line_polar(
              df_filtrado,
              r='Nivel',
              theta='Competencia',
              line_close=True,
              range_r=[0, 3],
          )
          fig.update_traces(
              fill='toself',
              line_color='#FF7600',
              fillcolor='rgba(98, 213, 177, 0.4)',
          )
          fig.update_layout(
              polar=dict(
                  radialaxis=dict(visible=True, range=[0, 3], color='#2F3F47'),
                  bgcolor='#FFFFFF',
              ),
              paper_bgcolor='#FFFFFF',
              plot_bgcolor='#FFFFFF',
              font=dict(color='#2F3F47'),
              showlegend=False,
          )
          st.plotly_chart(fig, use_container_width=True)
        else:
          st.warning(
              '⚠️ Selecciona al menos una competencia para mostrar el gráfico'
              ' de radar.'
          )

        st.success('✨ Reporte y matriz generados correctamente.')

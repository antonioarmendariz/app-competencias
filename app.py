import streamlit as st

# 1. Configuración inicial de la página
st.set_page_config(
    page_title="Skala - Sistema de Gestión de Desarrollo de Talento",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Inicialización del State (Base de datos simulada en memoria)
if "empresas" not in st.session_state:
    st.session_state.empresas = {
        "INNODEP": {
            "logo": "🎯",
            "plantillas": [
                "Plantilla_Estructura",
                "Plantilla_Modelo_Competencias",
                "Plantilla_Recursos_70_20_10",
            ],
            "admin": "antonio.armendariz@innodep.com.mx",
        }
    }

if "usuarios" not in st.session_state:
    st.session_state.usuarios = {
        "antonio.armendariz@innodep.com.mx": {
            "password": "admin2026",
            "rol": "KeyUserGlobal",
            "empresa": "INNODEP",
        }
    }

if "datos_plantillas" not in st.session_state:
    st.session_state.datos_plantillas = []

# Control de sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = ""
    st.session_state.user_rol = ""
    st.session_state.user_empresa = ""

# 3. Barra Lateral - Autenticación y Accesos
st.sidebar.markdown("## 🔐 Acceso al Sistema")

if not st.session_state.logged_in:
    correo = st.sidebar.text_input(
        "Correo corporativo:", value="antonio.armendariz@innodep.com.mx"
    )
    password = st.sidebar.text_input("Contraseña:", type="password")

    if st.sidebar.button("🔑 Ingresar al Sistema", use_container_width=True):
        # Validar usuarios registrados en la plataforma (incluyendo Key Users globales adicionales)
        if (
            correo in st.session_state.usuarios
            and st.session_state.usuarios[correo]["password"] == password
        ):
            st.session_state.logged_in = True
            st.session_state.user_email = correo
            st.session_state.user_rol = st.session_state.usuarios[correo]["rol"]
            st.session_state.user_empresa = st.session_state.usuarios[correo][
                "empresa"
            ]
            st.rerun()
        else:
            st.sidebar.error("Credenciales incorrectas.")

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "*Inicia sesión con tus credenciales para habilitar los paneles.*"
    )

else:
    st.sidebar.success(f"Sesión activa:\n**{st.session_state.user_email}**")
    st.sidebar.info(
        f"Rol: **{st.session_state.user_rol}**\nEmpresa:"
        f" **{st.session_state.user_empresa}**"
    )
    if st.sidebar.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.session_state.user_rol = ""
        st.session_state.user_empresa = ""
        st.rerun()

# 4. Cuerpo Principal de la Aplicación
if not st.session_state.logged_in:
    # Portada Comercial
    st.markdown(
        """
        <h1 style='color: #2F3F47; font-size: 3rem; margin-bottom: 0px;'>
            🎯 Skala
        </h1>
        <p style='color: #666666; font-size: 1.2rem; margin-top: 0px; font-weight: 500;'>
            Sistema de Gestión de Desarrollo de Talento &nbsp;|&nbsp; <span style='font-size: 1rem; color: #888888;'>Diseñado por INNODEP</span>
        </p>
    """,
        unsafe_allow_html=True,
    )

    st.warning(
        'Por favor, ingresa tu correo y contraseña en la barra lateral y'
        ' presiona "Ingresar al Sistema" para comenzar.'
    )

else:
    # Encabezado dentro del sistema
    st.markdown(f"# 🎯 Skala - Panel de Control ({st.session_state.user_empresa})")
    st.markdown("---")

    # ----------------------------------------------------
    # VISTA 1: KEY USER GLOBAL (Antonio y otros Key Users)
    # ----------------------------------------------------
    if st.session_state.user_rol == "KeyUserGlobal":
        st.markdown(
            "### ⚙️ Módulo Global de Key User (Gestión de Empresas y Usuarios"
            " Globales)"
        )

        tab1, tab2 = st.tabs(
            [
                "🏢 Alta de Empresas (Plantillas Base)",
                "👥 Gestión de Key Users & Admins",
            ]
        )

        with tab1:
            st.markdown(
                "Registra una nueva empresa cliente. Por defecto se asignan las"
                " tres plantillas base estándar."
            )
            with st.form("form_nueva_empresa"):
                nombre_empresa = st.text_input("Nombre de la Empresa:")
                logo_empresa = st.text_input(
                    "Icono o Logo (Emoji o URL corta):", value="📊"
                )

                st.markdown("#### Plantillas Base del Sistema")
                p1 = st.text_input(
                    "Plantilla 1:", value="Plantilla_Estructura"
                )
                p2 = st.text_input(
                    "Plantilla 2:", value="Plantilla_Modelo_Competencias"
                )
                p3 = st.text_input(
                    "Plantilla 3:", value="Plantilla_Recursos_70_20_10"
                )

                admin_correo = st.text_input(
                    "Correo del Administrador de la Empresa:"
                )
                admin_pass = st.text_input(
                    "Contraseña temporal del Administrador:", type="password"
                )

                submit_empresa = st.form_submit_button(
                    "💾 Registrar Empresa en Skala"
                )

                if submit_empresa:
                    if nombre_empresa and admin_correo:
                        st.session_state.empresas[nombre_empresa] = {
                            "logo": logo_empresa,
                            "plantillas": [p1, p2, p3],
                            "admin": admin_correo,
                        }
                        st.session_state.usuarios[admin_correo] = {
                            "password": admin_pass,
                            "rol": "AdminEmpresa",
                            "empresa": nombre_empresa,
                        }
                        st.success(
                            f"¡Empresa {nombre_empresa} dada de alta con éxito!"
                        )
                    else:
                        st.error(
                            "Por favor completa el nombre de la empresa y el"
                            " correo del administrador."
                        )

            st.markdown("### Empresas Activas en el Sistema")
            for emp, info in st.session_state.empresas.items():
                st.info(
                    f"**{info['logo']} {emp}** — Plantillas: "
                    f"{', '.join(info['plantillas'])} — Admin: {info['admin']}"
                )

        with tab2:
            st.markdown(
                "### 👤 Gestión de Key Users Globales y Administradores de"
                " Empresa"
            )
            with st.form("form_gestion_usuarios"):
                u_correo = st.text_input("Correo del Usuario:")
                u_pass = st.text_input("Contraseña:", type="password")
                u_rol = st.selectbox(
                    "Rol en el Sistema:",
                    ["KeyUserGlobal", "AdminEmpresa", "Gerente"],
                )
                u_empresa = st.selectbox(
                    "Empresa Asociada:", list(st.session_state.empresas.keys())
                )

                col_a, col_b = st.columns(2)
                crear_u = col_a.form_submit_button("➕ Guardar / Actualizar")
                eliminar_u = col_b.form_submit_button("🗑️ Dar de Baja Usuario")

                if crear_u:
                    st.session_state.usuarios[u_correo] = {
                        "password": u_pass,
                        "rol": u_rol,
                        "empresa": u_empresa,
                    }
                    st.success(f"Usuario {u_correo} actualizado correctamente.")
                if eliminar_u:
                    if u_correo in st.session_state.usuarios:
                        del st.session_state.usuarios[u_correo]
                        st.warning(
                            f"Usuario {u_correo} dado de baja del sistema."
                        )

            st.markdown("### 📋 Usuarios Registrados en el Sistema")
            for mail, u_info in st.session_state.usuarios.items():
                st.write(
                    f"- **{mail}** | Rol: `{u_info['rol']}` | Empresa:"
                    f" `{u_info['empresa']}`"
                )

    # ----------------------------------------------------
    # VISTA 2: ADMINISTRADOR DE EMPRESA
    # ----------------------------------------------------
    elif st.session_state.user_rol == "AdminEmpresa":
        emp_actual = st.session_state.user_empresa
        config_emp = st.session_state.empresas.get(
            emp_actual,
            {
                "plantillas": [
                    "Plantilla_Estructura",
                    "Plantilla_Modelo_Competencias",
                    "Plantilla_Recursos_70_20_10",
                ],
                "logo": "📊",
            },
        )

        st.markdown(
            f"### 🛠️ Panel de Administración - {config_emp['logo']}"
            f" {emp_actual}"
        )
        st.markdown(
            "Administra los registros manuales o reemplaza la información de"
            " las tres plantillas oficiales de tu empresa."
        )

        plantilla_seleccionada = st.selectbox(
            "Selecciona la Plantilla a Gestionar:",
            config_emp["plantillas"],
        )

        with st.form("form_datos_plantilla"):
            st.markdown(
                f"#### Editando registros para: *{plantilla_seleccionada}*"
            )
            col1, col2 = st.columns(2)
            item_nombre = col1.text_input("Nombre / Elemento del Registro:")
            item_valor = col2.text_input(
                "Valor o Detalle (Ej. Calificación, Estatus, Avance):"
            )

            guardar_item = st.form_submit_button(
                "➕ Agregar / Reemplazar Información"
            )

            if guardar_item and item_nombre:
                st.session_state.datos_plantillas.append({
                    "empresa": emp_actual,
                    "plantilla": plantilla_seleccionada,
                    "elemento": item_nombre,
                    "valor": item_valor,
                })
                st.success("Información guardada con éxito en la plantilla.")

        st.markdown("### 📋 Registros Actuales de la Empresa")
        registros_empresa = [
            r
            for r in st.session_state.datos_plantillas
            if r["empresa"] == emp_actual
        ]

        if registros_empresa:
            for idx, reg in enumerate(registros_empresa):
                st.write(
                    f"**{idx+1}. [{reg['plantilla']}]** {reg['elemento']} :"
                    f" *{reg['valor']}*"
                )
        else:
            st.info(
                "No hay registros cargados manualmente en esta empresa todavía."
            )

    # ----------------------------------------------------
    # VISTA 3: GERENTE
    # ----------------------------------------------------
    elif st.session_state.user_rol == "Gerente":
        st.markdown("### 📈 Panel Gerencial y de Consulta")
        st.markdown(
            "Visualiza el avance y los reportes operativos de tu universo de"
            " empresa."
        )

        emp_actual = st.session_state.user_empresa
        registros_empresa = [
            r
            for r in st.session_state.datos_plantillas
            if r["empresa"] == emp_actual
        ]

        if registros_empresa:
            for reg in registros_empresa:
                st.metric(
                    label=f"{reg['plantilla']} - {reg['elemento']}",
                    value=reg["valor"],
                )
        else:
            st.info(
                "Aún no hay métricas o información cargada por la administración"
                " para visualizar."
            )

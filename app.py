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
            "archivos_plantillas": {},
            "admin": "antonio.armendariz@innodep.com.mx",
        }
    }

if "usuarios" not in st.session_state:
    st.session_state.usuarios = {
        "antonio.armendariz@innodep.com.mx": {
            "nombre": "Antonio Armendariz",
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
    st.markdown(
        """
        <h1 style='color: #2F3F47; font-size: 3rem; margin-bottom: 0px;'>
            🎯 Skala
        </h1>
        <p style='color: #666666; font-size: 1.2rem; margin-top: 0px; font-weight: 500;'>
            Sistema de Gestión de Desarrollo de Talento &nbsp;|&nbsp; <span style='font-size: 1rem; color: #888888;'>Diseñado por INNODEP</span>[cite: 2]
        </p>
    """,
        unsafe_allow_html=True,
    )

    st.warning(
        'Por favor, ingresa tu correo y contraseña en la barra lateral y'
        ' presiona "Ingresar al Sistema" para comenzar.'
    )

else:
    st.markdown(f"# 🎯 Skala - Panel de Control ({st.session_state.user_empresa})")
    st.markdown("---")

    # ----------------------------------------------------
    # VISTA 1: KEY USER GLOBAL
    # ----------------------------------------------------
    if st.session_state.user_rol == "KeyUserGlobal":
        st.markdown(
            "### ⚙️ Módulo Global de Key User (Gestión de Empresas y Usuarios)"
        )

        tab1, tab2, tab3 = st.tabs(
            [
                "🏢 Alta de Empresas",
                "👥 Gestión de Usuarios por Empresa",
                "⚡ Key Users Globales",
            ]
        )

        with tab1:
            st.markdown(
                "Registra una nueva empresa cliente y carga los archivos"
                " iniciales para las tres plantillas base obligatorias."
            )
            with st.form("form_nueva_empresa"):
                nombre_empresa = st.text_input("Nombre de la Empresa:")
                logo_empresa = st.text_input(
                    "Icono o Logo (Emoji o URL corta):", value="📊"
                )

                st.markdown("#### Subida de las Tres Plantillas Base")
                file_p1 = st.file_uploader(
                    "Subir Plantilla_Estructura (Excel / CSV)",
                    type=["csv", "xlsx"],
                    key="up_p1",
                )
                file_p2 = st.file_uploader(
                    "Subir Plantilla_Modelo_Competencias (Excel / CSV)",
                    type=["csv", "xlsx"],
                    key="up_p2",
                )
                file_p3 = st.file_uploader(
                    "Subir Plantilla_Recursos_70_20_10 (Excel / CSV)",
                    type=["csv", "xlsx"],
                    key="up_p3",
                )

                admin_nombre = st.text_input(
                    "Nombre del Administrador Inicial:"
                )
                admin_correo = st.text_input(
                    "Correo del Administrador Inicial:"
                )
                admin_pass = st.text_input(
                    "Contraseña temporal del Administrador:", type="password"
                )

                submit_empresa = st.form_submit_button(
                    "💾 Registrar Empresa y Plantillas en Skala"
                )

                if submit_empresa:
                    if nombre_empresa and admin_correo:
                        archivos_dict = {
                            "Plantilla_Estructura": (
                                file_p1.name if file_p1 else "Sin archivo"
                            ),
                            "Plantilla_Modelo_Competencias": (
                                file_p2.name if file_p2 else "Sin archivo"
                            ),
                            "Plantilla_Recursos_70_20_10": (
                                file_p3.name if file_p3 else "Sin archivo"
                            ),
                        }

                        st.session_state.empresas[nombre_empresa] = {
                            "logo": logo_empresa,
                            "plantillas": [
                                "Plantilla_Estructura",
                                "Plantilla_Modelo_Competencias",
                                "Plantilla_Recursos_70_20_10",
                            ],
                            "archivos_plantillas": archivos_dict,
                            "admin": admin_correo,
                        }
                        st.session_state.usuarios[admin_correo] = {
                            "nombre": admin_nombre,
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
                if emp != "INNODEP":
                    st.info(
                        f"**{info['logo']} {emp}** — Admin: {info['admin']}"
                        " \n\n📁 Archivos base:"
                        f" {info.get('archivos_plantillas', {})}"
                    )

        with tab2:
            st.markdown(
                "### 👥 Gestión de Usuarios por Empresa Seleccionada"
            )

            # Filtrar empresas para excluir "INNODEP" de la selección de clientes
            empresas_clientes = [
                e for e in st.session_state.empresas.keys() if e != "INNODEP"
            ]

            if empresas_clientes:
                empresa_seleccionada = st.selectbox(
                    "1. Selecciona la empresa cliente para gestionar sus"
                    " usuarios:",
                    empresas_clientes,
                )

                st.markdown("---")
                st.markdown(
                    f"#### ➕ Registrar Usuario para: *{empresa_seleccionada}*"
                )

                with st.form("form_usuario_por_empresa"):
                    col_u1, col_u2 = st.columns(2)
                    u_nombre = col_u1.text_input("Nombre completo:")
                    u_correo = col_u2.text_input("Correo electrónico:")

                    col_u3, col_u4 = st.columns(2)
                    u_rol = col_u3.selectbox(
                        "Rol asignado:", ["AdminEmpresa", "Gerente"]
                    )
                    u_pass = col_u4.text_input("Contraseña:", type="password")

                    guardar_usuario_emp = st.form_submit_button(
                        "💾 Guardar Usuario en la Empresa"
                    )

                    if guardar_usuario_emp:
                        if u_correo and u_nombre:
                            st.session_state.usuarios[u_correo] = {
                                "nombre": u_nombre,
                                "password": u_pass,
                                "rol": u_rol,
                                "empresa": empresa_seleccionada,
                            }
                            st.success(
                                f"Usuario {u_nombre} registrado en"
                                f" {empresa_seleccionada} correctamente."
                            )
                        else:
                            st.error(
                                "Por favor ingresa el nombre y el correo."
                            )

                st.markdown("---")
                st.markdown(
                    f"#### 📋 Lista de Usuarios de: *{empresa_seleccionada}*"
                )

                usuarios_filtrados = {
                    k: v
                    for k, v in st.session_state.usuarios.items()
                    if v["empresa"] == empresa_seleccionada
                    and v["rol"] != "KeyUserGlobal"
                }

                if usuarios_filtrados:
                    for mail, u_info in usuarios_filtrados.items():
                        col_fila_1, col_fila_2 = st.columns([5, 1])
                        col_fila_1.markdown(
                            f"👤 **{u_info['nombre']}** ({mail}) — Rol:"
                            f" `{u_info['rol']}`"
                        )
                        if col_fila_2.button(
                            "🗑️ Borrar", key=f"del_emp_user_{mail}"
                        ):
                            del st.session_state.usuarios[mail]
                            st.success(
                                f"Usuario {mail} eliminado con éxito."
                            )
                            st.rerun()
                else:
                    st.info(
                        f"No hay usuarios registrados para {empresa_seleccionada}"
                        " todavía."
                    )
            else:
                st.warning(
                    "⚠️ No hay empresas clientes dadas de alta todavía. Ve a"
                    ' la pestaña "Alta de Empresas" para registrar la'
                    " primera."
                )

        with tab3:
            st.markdown("### ⚡ Control de Key Users Globales")

            with st.form("form_alta_keyuser"):
                st.markdown("#### Registrar Nuevo Key User Global")
                ku_nombre = st.text_input("Nombre completo:")
                ku_correo = st.text_input("Correo electrónico:")
                ku_pass = st.text_input("Contraseña:", type="password")

                guardar_ku = st.form_submit_button("💾 Guardar Key User Global")
                if guardar_ku:
                    if ku_correo and ku_nombre:
                        st.session_state.usuarios[ku_correo] = {
                            "nombre": ku_nombre,
                            "password": ku_pass,
                            "rol": "KeyUserGlobal",
                            "empresa": "INNODEP",
                        }
                        st.success(
                            f"Key User Global {ku_nombre} registrado con"
                            " éxito."
                        )
                    else:
                        st.error("Completa el nombre y correo.")

            st.markdown("---")
            st.markdown("#### 📋 Listado de Key Users Globales Activos")
            global_users = {
                k: v
                for k, v in st.session_state.usuarios.items()
                if v["rol"] == "KeyUserGlobal"
            }

            for mail, info in global_users.items():
                col_g1, col_g2 = st.columns([5, 1])
                col_g1.markdown(
                    f"⚡ **{info['nombre']}** ({mail}) — Empresa base:"
                    f" `{info['empresa']}`"
                )
                if mail != "antonio.armendariz@innodep.com.mx":
                    if col_g2.button("🗑️ Borrar", key=f"del_ku_{mail}"):
                        del st.session_state.usuarios[mail]
                        st.success(f"Key User {mail} eliminado.")
                        st.rerun()
                else:
                    col_g2.markdown("*Protegido*")

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
                "archivos_plantillas": {},
            },
        )

        st.markdown(
            f"### 🛠️ Panel de Administración - {config_emp['logo']}"
            f" {emp_actual}"
        )
        st.markdown(
            "Aquí puedes reemplazar las tres plantillas oficiales de tu"
            " empresa, o gestionar registros de manera manual, modificando o"
            " eliminando según sea necesario."
        )

        plantilla_seleccionada = st.selectbox(
            "Selecciona la Plantilla a Gestionar:",
            config_emp["plantillas"],
        )

        st.markdown("#### 🔄 Reemplazar o Actualizar Archivo de Plantilla")
        nuevo_archivo_plantilla = st.file_uploader(
            f"Subir nueva versión para {plantilla_seleccionada}",
            type=["csv", "xlsx"],
            key=f"repl_{plantilla_seleccionada}",
        )
        if nuevo_archivo_plantilla:
            if "archivos_plantillas" not in config_emp:
                config_emp["archivos_plantillas"] = {}
            config_emp["archivos_plantillas"][plantilla_seleccionada] = (
                nuevo_archivo_plantilla.name
            )
            st.success(
                f"¡Plantilla {plantilla_seleccionada} actualizada con éxito!"
            )

        st.markdown("---")
        st.markdown("#### ✏️ Gestión Manual de Registros (Agregar / Modificar)")
        with st.form("form_datos_plantilla"):
            col1, col2 = st.columns(2)
            item_nombre = col1.text_input("Nombre / Elemento del Registro:")
            item_valor = col2.text_input("Valor o Detalle:")

            guardar_item = st.form_submit_button(
                "➕ Agregar / Modificar Información"
            )

            if guardar_item and item_nombre:
                st.session_state.datos_plantillas.append({
                    "empresa": emp_actual,
                    "plantilla": plantilla_seleccionada,
                    "elemento": item_nombre,
                    "valor": item_valor,
                })
                st.success("Información guardada con éxito.")

        st.markdown("### 📋 Registros Actuales de la Empresa")
        registros_empresa = [
            r
            for r in st.session_state.datos_plantillas
            if r["empresa"] == emp_actual
        ]

        if registros_empresa:
            for idx, reg in enumerate(registros_empresa):
                col_reg1, col_reg2 = st.columns([5, 1])
                col_reg1.write(
                    f"**{idx+1}. [{reg['plantilla']}]** {reg['elemento']} :"
                    f" *{reg['valor']}*"
                )
                if col_reg2.button("🗑️ Borrar", key=f"del_reg_{idx}"):
                    st.session_state.datos_plantillas.pop(idx)
                    st.rerun()
        else:
            st.info("No hay registros cargados para esta empresa todavía.")

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

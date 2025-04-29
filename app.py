"""
APLICACIÓN STREAMLIT PARA PREDICCIÓN DE PRECIOS DE VIVIENDAS
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
from PIL import Image
import datetime

# Configurar la página
st.set_page_config(
    page_title="Avaluador de Viviendas",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Funciones para cargar datos y modelos
@st.cache_data
def load_data():
    try:
        return pd.read_csv('housing_data.csv')
    except FileNotFoundError:
        st.error("No se encontró el archivo de datos. Por favor, asegúrate de que housing_data.csv existe en el directorio.")
        return None

@st.cache_resource
def load_model():
    try:
        model = joblib.load('models/housing_model.pkl')
        scaler = joblib.load('models/scaler.pkl')
        return model, scaler
    except FileNotFoundError:
        st.error("No se encontraron los archivos del modelo. Asegúrate de que los archivos existen en la carpeta models/.")
        return None, None

# Cargar datos y modelo
df = load_data()
model, scaler = load_model()

# Sidebar
with st.sidebar:
    st.image("assets/logo.png", width=160)
    page = st.sidebar.radio("Ir a:", ["Inicio", "Avaluar", "Contacto"])
    st.markdown("---")
    st.caption("© 2025 Avaluador de Viviendas. Desarrollado por Home Value Avaluador")

# Página de inicio
if page == "Inicio":
    st.title("Bienvenido al Avaluador Viviendas")
    st.markdown("""
    Esta aplicación utiliza un modelo de Machine Learning para estimar el precio de una vivienda basado en características relevantes.
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("¿Qué puedes hacer aquí?")
        st.markdown("""
        - **Predecir precios** de viviendas de manera instantánea.
        - **Explorar** cómo distintos factores influyen en el precio.
        - **Comparar** distintas características para diferentes viviendas.
        """)
        
    with col2:
        st.image("assets/house_welcome.png", use_container_width=True)

    st.markdown("---")
    st.subheader("¿Cómo funciona?")
    st.markdown("""
    Solo debes ingresar algunos datos básicos de la vivienda y el modelo te dará una predicción aproximada del precio.  
    🔥 ¡Ideal para agentes inmobiliarios, compradores y desarrolladores de proyectos!
    """)

# Página de predicción
elif page == "Predicción":
    st.title("Predicción de Precios de Viviendas 🧮")
    st.markdown("""
    Ingrese las características de la vivienda para obtener una predicción del precio basado en nuestro modelo entrenado.
    """)

    if model is not None and scaler is not None and df is not None:
        with st.form("prediction_form"):
            st.subheader("🔎 Características de la vivienda")
            
            col1, col2 = st.columns(2)
            
            with col1:
                rm = st.slider("Número medio de habitaciones (RM)", 
                               min_value=int(df['RM'].min()), 
                               max_value=int(df['RM'].max()), 
                               value=int(df['RM'].mean()))
                
                lstat = st.slider("% de población de estatus bajo (LSTAT)", 
                                  min_value=float(df['LSTAT'].min()), 
                                  max_value=float(df['LSTAT'].max()), 
                                  value=float(df['LSTAT'].mean()))
            
            with col2:
                ptratio = st.slider("Ratio (PTRATIO)", 
                                    min_value=float(df['PTRATIO'].min()), 
                                    max_value=float(df['PTRATIO'].max()), 
                                    value=float(df['PTRATIO'].mean()))
                
                dis = st.slider("Distancia a centros de empleo (DIS)", 
                                min_value=float(df['DIS'].min()), 
                                max_value=float(df['DIS'].max()), 
                                value=float(df['DIS'].mean()))
            
            submit_button = st.form_submit_button("🚀 Predecir Precio")

        if submit_button:
            input_data = np.array([[rm, lstat, ptratio, dis]])
            input_scaled = scaler.transform(input_data)
            prediction = model.predict(input_scaled)[0]

            st.success(f"🏡 El precio estimado para esta vivienda es: **${prediction:.2f}k**")

            st.markdown("---")
            st.subheader("📈 ¿Cómo interpretarlo?")
            st.markdown("""
            - Este valor es una estimación basada en características promedio y puede variar dependiendo de condiciones de mercado.
            - Para una evaluación más precisa, sugerimos considerar variables adicionales.
            """)

    else:
        st.warning("🔧 El modelo o los datos no están disponibles. Por favor, verifique los archivos.")

# Página de contacto
elif page == "Contacto":
    st.title("📬 Contáctanos")
    st.markdown("""
    ¿Quieres recibir una asesoría personalizada o más información?  
    ¡Déjanos tus datos y nos pondremos en contacto contigo!
    """)

    with st.form("contact_form"):
        nombre = st.text_input("Nombre completo", placeholder="Tu nombre")
        email = st.text_input("Correo electrónico", placeholder="tunombre@correo.com")
        mensaje = st.text_area("Mensaje", placeholder="Escribe aquí tu mensaje...")
        
        submit_contact = st.form_submit_button("Enviar mensaje 📩")

    if submit_contact:
        # Puedes guardar los datos o enviar un correo. Aquí lo mostramos por simplicidad:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        contacto = pd.DataFrame({
            'Nombre': [nombre],
            'Email': [email],
            'Mensaje': [mensaje],
            'Fecha': [timestamp]
        })
        
        # Guardar en un archivo CSV (opcional)
        if not os.path.exists("contactos.csv"):
            contacto.to_csv("contactos.csv", index=False)
        else:
            contacto.to_csv("contactos.csv", mode='a', header=False, index=False)
        
        st.success("✅ ¡Gracias por contactarnos! Te responderemos pronto.")

# Footer personalizado
st.markdown("""
<style>
footer {
    visibility: hidden;
}
</style>
<div style="text-align: center; padding: 10px; font-size: 12px; color: gray;">
Desarrollado por Home Value Avaluador| © 2025 Avaluador de Viviendas
</div>
""", unsafe_allow_html=True)

import streamlit as st

# ==========================================
# BASE DE CONOCIMIENTO Y MOTOR DE INFERENCIA
# ==========================================
def motor_inferencia(fiebre, dolor_articular, sarpullido, conjuntivitis, dolor_ojos, sangrado):
    """
    Evalúa los síntomas ingresados contra la base de reglas lógicas.
    Retorna una tupla: (Diagnóstico, Recomendación, Tipo de Alerta)
    """
    # Regla 1: Descarte de urgencia (Dengue Grave)
    if sangrado == "Sí":
        return (
            "Dengue Grave (Hemorrágico)", 
            "🚨 ALERTA ROJA: Riesgo de shock. Requiere atención médica de urgencia inmediata en un hospital.", 
            "error"
        )
    
    # Regla 2: Inferencia de Chikungunya (Fiebre alta + Dolor articular incapacitante)
    elif fiebre == "Alta (repentina)" and dolor_articular == "Severo / Incapacitante":
        return (
            "Sospecha de Chikungunya", 
            "⚠️ Se caracteriza por dolores articulares muy intensos que pueden durar meses. Guarde reposo, hidrátese y acuda a su centro de salud.", 
            "warning"
        )
    
    # Regla 3: Inferencia de Zika (Fiebre baja/nula + Conjuntivitis + Sarpullido)
    elif fiebre in ["Baja", "Ninguna"] and conjuntivitis == "Sí" and sarpullido == "Sí":
        return (
            "Sospecha de Zika", 
            "⚠️ Atención especial si la paciente está embarazada por riesgo de microcefalia fetal. Acuda al centro de salud para confirmación serológica.", 
            "warning"
        )
    
    # Regla 4: Inferencia de Dengue Clásico (Fiebre alta + Dolor retro-ocular)
    elif fiebre == "Alta (repentina)" and dolor_ojos == "Sí" and dolor_articular in ["Leve", "Moderado"]:
        return (
            "Sospecha de Dengue Clásico", 
            "⚠️ Mantenga hidratación constante. ESTÁ CONTRAINDICADO tomar aspirina o ibuprofeno (riesgo de sangrado). Use solo paracetamol y acuda al médico.", 
            "warning"
        )
    
    # Regla 5: Cuadro inespecífico
    else:
        return (
            "Cuadro Viral Inespecífico", 
            "ℹ️ La combinación de síntomas no apunta claramente a una fase aguda típica de Dengue, Zika o Chikungunya. Si las molestias persisten por más de 3 días, consulte a un médico.", 
            "info"
        )

# ==========================================
# INTERFAZ DE USUARIO (STREAMLIT)
# ==========================================
def main():
    st.set_page_config(page_title="SE - Arbovirus", page_icon="🦟", layout="centered")
    
    st.title("🦟 Sistema Experto Médico")
    st.subheader("Triage Rápido: Dengue, Zika y Chikungunya")
    st.write("Seleccione los síntomas que presenta el paciente para recibir una evaluación probabilística basada en reglas clínicas.")
    
    st.divider()

    # Recolección de Hechos (Síntomas)
    col1, col2 = st.columns(2)
    
    with col1:
        fiebre = st.radio("🌡️ Nivel de Fiebre:", ["Ninguna", "Baja", "Alta (repentina)"])
        dolor_articular = st.selectbox("🦴 Dolor Articular:", ["Ninguno", "Leve", "Moderado", "Severo / Incapacitante"])
        sarpullido = st.radio("🔴 ¿Presenta sarpullido o erupción cutánea?", ["No", "Sí"])
        
    with col2:
        dolor_ojos = st.radio("👁️ ¿Presenta dolor retro-ocular (detrás de los ojos)?", ["No", "Sí"])
        conjuntivitis = st.radio("👀 ¿Presenta conjuntivitis (ojos rojos sin secreción)?", ["No", "Sí"])
        sangrado = st.radio("🩸 ¿Presenta sangrado (encías, nariz, o hematomas inexplicables)?", ["No", "Sí"])

    st.divider()

    # Ejecución del Motor de Inferencia
    if st.button("Diagnosticar Paciente", type="primary", use_container_width=True):
        diagnostico, recomendacion, alerta = motor_inferencia(
            fiebre, dolor_articular, sarpullido, conjuntivitis, dolor_ojos, sangrado
        )
        
        st.subheader("Resultado de la Inferencia:")
        
        if alerta == "error":
            st.error(f"**{diagnostico}**\n\n{recomendacion}")
        elif alerta == "warning":
            st.warning(f"**{diagnostico}**\n\n{recomendacion}")
        else:
            st.info(f"**{diagnostico}**\n\n{recomendacion}")
            
    st.caption("")

if __name__ == "__main__":
    main()

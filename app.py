import streamlit as st

# ==========================================
# MOTOR DE INFERENCIA (HEURÍSTICO POR PESOS)
# ==========================================
def evaluar_sintomas(fiebre, dolor_articular, sarpullido, conjuntivitis, dolor_ojos, sangrado):
    # Regla 1: Descarte crítico absoluto
    if sangrado == "Sí":
        return "Dengue Grave (Hemorrágico)", 100, "🚨 ALERTA ROJA: Riesgo de shock. Acudir a emergencias de inmediato.", "error"
    
    # Inicializar probabilidades
    prob = {"Dengue Clásico": 0, "Zika": 0, "Chikungunya": 0}
    
    # Asignación de pesos heurísticos (Acumulación de evidencia)
    if fiebre == "Alta (repentina)":
        prob["Dengue Clásico"] += 35
        prob["Chikungunya"] += 30
    elif fiebre == "Baja o Ninguna":
        prob["Zika"] += 35
        
    if dolor_articular == "Severo / Incapacitante":
        prob["Chikungunya"] += 45
    elif dolor_articular in ["Leve", "Moderado"]:
        prob["Dengue Clásico"] += 15
        prob["Zika"] += 15
        
    if sarpullido == "Sí":
        prob["Zika"] += 30
        prob["Dengue Clásico"] += 15
        prob["Chikungunya"] += 10
        
    if conjuntivitis == "Sí":
        prob["Zika"] += 20
        
    if dolor_ojos == "Sí":
        prob["Dengue Clásico"] += 35
        
    # Determinar el diagnóstico con mayor probabilidad
    diagnostico = max(prob, key=prob.get)
    certeza = prob[diagnostico]
    
    # Limitar a 99% (ya que la certeza absoluta en medicina es rara sin pruebas de laboratorio)
    if certeza > 99: 
        certeza = 99
        
    # Si los puntos son muy bajos, el sistema deduce que no es un arbovirus claro
    if certeza < 30:
        return "Cuadro Viral Inespecífico", certeza, "ℹ️ La evidencia es baja. Los síntomas no apuntan claramente a un arbovirus típico. Mantenga observación.", "info"
        
    # Recomendaciones personalizadas
    if diagnostico == "Dengue Clásico":
        rec = "⚠️ ESTÁ CONTRAINDICADO tomar aspirina o ibuprofeno (riesgo de hemorragia). Use solo paracetamol, beba mucha agua y acuda al médico."
    elif diagnostico == "Zika":
        rec = "⚠️ Especial atención en gestantes (riesgo fetal). Use repelente para evitar transmisión y busque confirmación clínica."
    else:
        rec = "⚠️ El dolor articular puede persistir por meses. Requiere reposo absoluto, analgésicos recetados y control médico."
        
    return diagnostico, certeza, rec, "warning"

# ==========================================
# INTERFAZ DE USUARIO (STREAMLIT)
# ==========================================
def main():
    st.set_page_config(page_title="SE Médico | Arbovirus", page_icon="🩺", layout="centered")
    
    st.title("🩺 SE: Diagnóstico de Arbovirus")
    st.markdown("**Motor de Inferencia Heurístico** que evalúa la probabilidad de Dengue, Zika o Chikungunya mediante la ponderación de síntomas.")
    
    st.divider()

    # Base de Hechos (Entrada de usuario)
    col1, col2 = st.columns(2)
    
    with col1:
        fiebre = st.radio("🌡️ Nivel de Fiebre:", ["Baja o Ninguna", "Alta (repentina)"])
        dolor_articular = st.selectbox("🦴 Dolor Articular:", ["Ninguno", "Leve", "Moderado", "Severo / Incapacitante"])
        sarpullido = st.radio("🔴 ¿Presenta sarpullido en la piel?", ["No", "Sí"])
        
    with col2:
        dolor_ojos = st.radio("👁️ ¿Presenta dolor detrás de los ojos?", ["No", "Sí"])
        conjuntivitis = st.radio("👀 ¿Ojos rojos sin secreción (Conjuntivitis)?", ["No", "Sí"])
        sangrado = st.radio("🩸 ¿Sangrado en encías o nariz?", ["No", "Sí"])

    st.divider()

    # Ejecución
    if st.button("Diagnosticar Paciente", type="primary", use_container_width=True):
        diagnostico, certeza, recomendacion, alerta = evaluar_sintomas(
            fiebre, dolor_articular, sarpullido, conjuntivitis, dolor_ojos, sangrado
        )
        
        st.subheader("Resultado de la Inferencia:")
        
        # Mostrar métrica y barra de probabilidad
        st.metric(label="Diagnóstico Principal Deduzido", value=diagnostico, delta=f"{certeza}% de probabilidad calculada")
        st.progress(certeza / 100.0)
        
        # Mostrar alertas
        if alerta == "error":
            st.error(recomendacion)
        elif alerta == "warning":
            st.warning(recomendacion)
        else:
            st.info(recomendacion)
            
    st.caption("")

if __name__ == "__main__":
    main()

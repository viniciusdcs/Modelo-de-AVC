import streamlit as st
import pandas as pd
import joblib

# Carregar o modelo e o scaler salvos
modelo = joblib.load("modelo_otimizado.pkl")
scaler = joblib.load("scaler_variaveis.pkl")

st.title("Previsão de Risco de AVC")
st.markdown("Preencha os dados abaixo para saber o seu risco estimado de Acidente Vascular Cerebral (AVC).")

# Entradas do usuário organizadas em colunas
st.header("📋 Dados do Paciente")

# Primeira linha de colunas
col1, col2, col3 = st.columns(3)

with col1:
    idade = st.slider("Idade", 0, 100, 43)
    doenca_cardiaca = st.selectbox("Você tem doença cardíaca?", ["Não", "Sim"])
    hipertensao = st.selectbox("Você tem hipertensão?", ["Não", "Sim"])

with col2:
    sexo = st.selectbox("Sexo", ["Masculino", "Feminino"])
    casado = st.selectbox("Você é/foi casado(a)?", ["Não", "Sim"])
    tipo_trabalho = st.selectbox("Tipo de trabalho", ["Funcionário Privado", "Autônomo", "Servidor Público", "Dono(a) de casa"])

with col3:
    tipo_residencia = st.selectbox("Tipo de residência", ["Urbana", "Rural"])
    fumante = st.selectbox("Status de tabagismo", ["Nunca fumou", "Fumante", "Ex-fumante", "Prefiro Não Informar"])

# Segunda linha para dados numéricos
col4, col5 = st.columns(2)

with col4:
    bmi = st.number_input("IMC (Índice de Massa Corporal)", 10.0, 100.0, 28.0)

with col5:
    glicose = st.number_input("Nível médio de glicose no sangue", 50.0, 300.0, 105.0)

# Preparar dados contínuos para escalar
dados_continuos = pd.DataFrame({
    'age': [idade],
    'bmi': [bmi],
    'avg_glucose_level': [glicose]
})

# Aplicar scaler
dados_escala = scaler.transform(dados_continuos)
age_scaled = dados_escala[0][0]
bmi_scaled = dados_escala[0][1]
glucose_scaled = dados_escala[0][2]

# Dicionário com as variáveis no formato esperado pelo modelo
entrada = {
    'gender': 1 if sexo == "Masculino" else 0,
    'hypertension': 1 if hipertensao == "Sim" else 0,
    'heart_disease': 1 if doenca_cardiaca == "Sim" else 0,
    'ever_married': 1 if casado == "Sim" else 0,
    'Residence_type': 1 if tipo_residencia == "Urbana" else 0,
    'work_type_Private': 1 if tipo_trabalho == "Funcionário Privado" else 0,
    'work_type_Self-employed': 1 if tipo_trabalho == "Autônomo" else 0,
    'work_type_children': 1 if tipo_trabalho == "Dono(a) de casa" else 0,
    'smoking_status_formerly smoked': 1 if fumante == "Ex-fumante" else 0,
    'smoking_status_never smoked': 1 if fumante == "Nunca fumou" else 0,
    'smoking_status_smokes': 1 if fumante == "Fumante" else 0,
    'age_scaled': age_scaled,
    'bmi_scaled': bmi_scaled,
    'avg_glucose_level_scaled': glucose_scaled
}

# Colunas na ordem correta
colunas_modelo = [
    'gender', 'hypertension', 'heart_disease', 'ever_married',
    'Residence_type', 'work_type_Private', 'work_type_Self-employed',
    'work_type_children', 'smoking_status_formerly smoked',
    'smoking_status_never smoked', 'smoking_status_smokes',
    'age_scaled', 'bmi_scaled', 'avg_glucose_level_scaled'
]

# Criar DataFrame para predizer
df_entrada = pd.DataFrame([entrada], columns=colunas_modelo)

# Botão para prever
st.header("Predição de AVC")

if st.button("Verificar risco de AVC", type="primary"):
    pred = modelo.predict(df_entrada)[0]
    prob = modelo.predict_proba(df_entrada)[0][1]
    prob_pct = prob * 100

    # Definir faixa de cor
    if prob_pct <= 20:
        bg_color = "#e8f5e8"
        text_color = "#2e7d32"
        faixa = "🟢 BAIXO RISCO"
    elif prob_pct <= 50:
        bg_color = "#fffde7"
        text_color = "#f9a825"
        faixa = "🟡 MÉDIO RISCO"
    else:
        bg_color = "#ffebee"
        text_color = "#d32f2f"
        faixa = "🔴 ALTO RISCO"

    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: center; padding: 20px; background-color: {bg_color}; border-radius: 10px;'>
        <h2 style='color: {text_color}; margin-bottom: 10px;'>
            {faixa}
        </h2>
        <h1 style='font-size: 3rem; color: {text_color}; margin: 20px 0;'>
            {prob_pct:.2f}%
        </h1>
        <p style='font-size: 1.2rem; color: #666;'>
            Probabilidade estimada de AVC
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

# Informações adicionais
st.header("ℹ️ Alertas importantes")
st.markdown("""
- Esta aplicação usa machine learning para estimar o risco de AVC
- Os resultados são apenas estimativas e não substituem consulta médica
- Para diagnóstico preciso, sempre consulte um profissional de saúde
""")

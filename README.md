# Modelo-de-AVC

## 🧠 Explicação do Problema

Segundo a Organização Mundial da Saúde (OMS), o Acidente Vascular Cerebral (AVC) é a **segunda principal causa de morte no mundo**, sendo responsável por aproximadamente **11% de todos os óbitos globais**.

Este projeto utiliza um conjunto de dados clínicos com informações sobre pacientes, com o objetivo de **prever a ocorrência de AVC** com base em variáveis como idade, hipertensão, doenças cardíacas, tipo de trabalho, estado civil e tabagismo.

Cada linha no conjunto de dados representa um paciente e contém as seguintes informações:

| Variável              | Descrição                                                                 |
|-----------------------|---------------------------------------------------------------------------|
| `id`                  | Identificador único do paciente                                           |
| `gender`              | Sexo do paciente: "Male", "Female" ou "Other"                             |
| `age`                 | Idade do paciente                                                         |
| `hypertension`        | 0 = não tem hipertensão, 1 = tem hipertensão                              |
| `heart_disease`       | 0 = sem doenças cardíacas, 1 = com doenças cardíacas                      |
| `ever_married`        | Estado civil: "Yes" ou "No"                                               |
| `work_type`           | Tipo de trabalho: "children", "Govt_job", "Never_worked", "Private", "Self-employed" |
| `Residence_type`      | Tipo de residência: "Rural" ou "Urban"                                    |
| `avg_glucose_level`   | Nível médio de glicose no sangue                                          |
| `bmi`                 | Índice de Massa Corporal                                                  |
| `smoking_status`      | Status de tabagismo: "formerly smoked", "never smoked", "smokes", "Unknown" |
| `stroke`              | 0 = sem histórico de AVC, 1 = teve AVC                                    |

---

## ⚙️ Processo e Justificativa

### 🧹 Pré-processamento

Foram realizadas as seguintes etapas:

- **Tratamento de valores ausentes:** entradas com `Unknown` ou `NaN` foram mantidas ou codificadas apropriadamente.
- **Codificação de variáveis categóricas:** foi aplicada codificação `one-hot` nas variáveis como `work_type`, `smoking_status` e `gender` para transformar categorias em variáveis binárias.
- **Escalonamento:** variáveis contínuas (`age`, `bmi`, `avg_glucose_level`) foram padronizadas com `StandardScaler` para melhorar o desempenho dos modelos.

### 🧠 Modelo de Machine Learning

- Foi escolhido o **Random Forest Classifier**, por ser:
  - Robusto a dados desbalanceados
  - Capaz de lidar com variáveis categóricas e numéricas sem necessidade de normalidade
  - Interpretável e eficiente em datasets tabulares

### ⚖️ Balanceamento de classes

- Como a variável alvo (`stroke`) é fortemente desbalanceada, foi utilizado **SMOTE (Synthetic Minority Oversampling Technique)** para gerar amostras sintéticas da classe minoritária e equilibrar o conjunto de dados.

### 🔍 Validação

- Os dados foram divididos em treino (85%) e teste (15%), com **estratificação**, para manter a proporção de classes.
- Foi aplicada **validação cruzada com 5 folds** no conjunto de treino, com otimização de hiperparâmetros usando **RandomizedSearchCV**.
- A métrica principal usada foi o **F1-score**, que equilibra precisão e recall, ideal para problemas com classes desbalanceadas.

---

🎯 Com isso, foi possível criar uma aplicação capaz de prever com boa acurácia e sensibilidade o risco de AVC a partir de dados clínicos simples, com uma interface interativa via **Streamlit**.

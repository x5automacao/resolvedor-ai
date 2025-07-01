Chave API Gemini: 
AIzaSyDKPaTD_3gh0aoUSgRzQfoLVF06ZyLCzCk

import streamlit as st
import google.generativeai as genai
import os

# --- Configuração Inicial ---
# Use st.secrets para gerenciar a chave da API de forma segura quando for fazer o deploy
# Por enquanto, vamos pedir para o usuário colar a chave na interface.
# Para desenvolvimento local, você pode descomentar a linha abaixo e colar sua chave
# os.environ['GEMINI_API_KEY'] = "SUA_CHAVE_API_AQUI" 

st.set_page_config(page_title="Resolvedor.AI", page_icon="🛠️")

st.title("🛠️ Resolvedor.AI")
st.caption("Transforme seus problemas em planos de ação.")

# --- Entrada da Chave da API e do Problema ---
# Usando um formulário para agrupar as entradas
# A chave da API será lida dos "Secrets" do Streamlit, não mais do usuário.
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("Ocorreu um erro na configuração da API. O administrador foi notificado.")
    # Este erro só aparecerá se você esquecer de configurar o segredo no Streamlit Cloud

with st.form("problem_form"):
    user_problem = st.text_area("Descreva o problema que você quer resolver:", height=150, placeholder="Ex: Meu notebook windows está muito lento ao iniciar")
    submitted = st.form_submit_button("Gerar Plano de Ação")

if submitted:
    if not user_problem:
        st.error("Por favor, descreva o problema que você quer resolver.")
    else:
        # O resto da lógica para gerar o plano continua aqui...
        # Certifique-se de que o bloco "try/except" que gera o plano esteja corretamente alinhado aqui dentro.
    elif not user_problem:
        st.error("Por favor, descreva o problema que você quer resolver.")
    else:
        try:
            # Configura a API com a chave fornecida pelo usuário
            genai.configure(api_key=api_key_input)

            # O "Mega-Prompt" - A instrução mestre para a IA
            prompt_template = f"""
            Você é o 'Resolvedor.AI', um especialista em criar planos de ação claros, objetivos e fáceis de seguir.
            Um usuário tem o seguinte problema: "{user_problem}"

            Sua tarefa é gerar um plano de ação em formato Markdown, seguindo estritamente a estrutura abaixo.
            Seja direto e evite frases desnecessárias. Vá direto ao ponto.

            ### 📝 Plano de Ação: [Título Criativo e Claro para o Problema]

            **Nível de Dificuldade:** [Avalie como Fácil, Médio ou Difícil]
            **Tempo Estimado:** [Ex: 15-30 minutos]

            ---

            #### 🛠️ Materiais e Ferramentas Necessárias
            (Se nenhum material for necessário, escreva "Nenhum material necessário.")
            - [ ] Item 1
            - [ ] Item 2

            ---

            #### 📋 Passo a Passo da Solução
            1.  **Primeiro Passo:** Descrição clara, curta e acionável.
            2.  **Segundo Passo:** Descrição clara, curta e acionável.
            3.  **Continue com quantos passos forem necessários...**

            ---

            #### ⚠️ Dicas de Segurança e Erros Comuns
            - **Cuidado:** [Alerte sobre um erro comum ou algo que o usuário deve evitar].
            - **Dica Pro:** [Ofereça um truque ou conselho que facilita a tarefa].
            """

            # Mostra uma mensagem enquanto o plano está sendo gerado
            with st.spinner("Analisando o problema e montando seu plano de ação..."):
                model = genai.GenerativeModel('gemini-1.5-flash') # Modelo rápido e eficiente
                response = model.generate_content(prompt_template)
            
            st.success("Seu plano de ação está pronto!")
            # Exibe a resposta formatada em Markdown
            st.markdown(response.text)

        except Exception as e:
            st.error(f"Ocorreu um erro ao se comunicar com a API. Verifique sua chave ou tente novamente. Erro: {e}")

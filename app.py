import streamlit as st
import google.generativeai as genai

# --- Configuração da Página e Título ---
st.set_page_config(page_title="Resolvedor.AI", page_icon="🛠️")
st.title("🛠️ Resolvedor.AI")
st.caption("Transforme seus problemas em planos de ação.")

# --- Configuração da API (deve ser a primeira coisa na lógica) ---
try:
    # Lê a chave da API dos "Secrets" do Streamlit
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    # Mostra um erro amigável se a chave não for encontrada nos Secrets
    st.error("Ocorreu um erro na configuração da API. O administrador foi notificado.")
    # Interrompe a execução se a chave não estiver configurada
    st.stop()

# --- Formulário de Entrada do Problema ---
with st.form("problem_form"):
    user_problem = st.text_area("Descreva o problema que você quer resolver:", height=150, placeholder="Ex: Como remover mancha de café da minha camisa?")
    submitted = st.form_submit_button("Gerar Plano de Ação")

# --- Lógica Principal ---
if submitted:
    if not user_problem:
        st.error("Por favor, descreva o problema que você quer resolver.")
    else:
        try:
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
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt_template)
            
            st.success("Seu plano de ação está pronto!")
            st.markdown(response.text)

        except Exception as e:
            st.error(f"Ocorreu um erro ao gerar a resposta. Por favor, tente novamente. Erro: {e}")
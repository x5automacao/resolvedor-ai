import streamlit as st
import google.generativeai as genai
import json
import requests

# --- FUNÇÃO AUXILIAR PARA RESOLVER URLs ---
def resolve_redirect_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.url
    except requests.RequestException as e:
        print(f"Erro ao resolver a URL {url}: {e}")
        return url

# --- Configuração da Página e Título ---
st.set_page_config(page_title="Resolvedor.AI", page_icon="🏆")
st.title("🏆 Resolvedor.AI")
st.caption("Planos de ação inteligentes com busca de mídia.")

# --- Configuração da API ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("Ocorreu um erro na configuração da API. O administrador foi notificado.")
    st.stop()

# --- Formulário de Entrada do Problema ---
with st.form("problem_form"):
    user_problem = st.text_area(
        "Descreva o problema que você quer resolver:",
        height=150,
        placeholder="Ex: Como fazer o melhor nó de gravata para um casamento?"
    )
    selected_model = 'gemini-1.5-pro'
    submitted = st.form_submit_button("Gerar Plano de Ação")

# --- Lógica Principal ---
if submitted:
    if not user_problem:
        st.error("Por favor, descreva o problema que você quer resolver.")
    else:
        # TENTATIVA FINAL DE REFINAMENTO DO PROMPT
        prompt_template = f"""
            Sua tarefa é criar um plano de ação multimídia em JSON para o problema: "{user_problem}".
            Para cada passo, use sua busca avançada. CRITÉRIO MAIS IMPORTANTE: todo conteúdo (vídeo ou GIF) deve ser de uma fonte pública e com alta probabilidade de estar disponível e permitir incorporação.
            1. Para vídeos, encontre um tutorial relevante no YouTube. A URL deve ser um link direto e público do YouTube.
            2. Para GIFs, encontre um GIF animado relevante. A URL deve ser um link direto para o arquivo de imagem.
            3. Para texto, forneça uma instrução clara.
            O JSON deve ter a estrutura: {{"title": "...", "difficulty": "...", "estimated_time": "...", "steps": [{{"type": "text|gif|video", "title": "...", "content": "..."}}]}}
            Retorne APENAS o código JSON.
            """

        with st.spinner(f"Consultando o modelo {selected_model}..."):
            try:
                model = genai.GenerativeModel(selected_model)
                response = model.generate_content(prompt_template)
                clean_response_text = response.text.strip().replace("```json", "").replace("```", "")
                plan = json.loads(clean_response_text)

                st.subheader(plan.get("title", "Seu Plano de Ação"))
                st.write(f"**Dificuldade:** {plan.get('difficulty')} | **Tempo Estimado:** {plan.get('estimated_time')}")
                st.divider()

                for i, step in enumerate(plan.get("steps", [])):
                    step_type = step.get("type")
                    step_title = step.get("title")
                    step_content = step.get("content")

                    st.markdown(f"**Passo {i+1}: {step_title}**")

                    if step_type == "text":
                        st.info(step_content)

                    elif step_type == "gif":
                        st.image(step_content, use_container_width=True)
                        # MELHORIA DE UX PARA GIFS
                        st.caption("Se a imagem não carregar, o conteúdo pode ter sido removido da fonte original.")

                    elif step_type == "video":
                        with st.spinner("Verificando e carregando o vídeo..."):
                            final_url = resolve_redirect_url(step_content)
                        st.video(final_url)
                        # MELHORIA DE UX PARA VÍDEOS
                        st.info(f"Às vezes, vídeos são privados ou removidos. Se não funcionar, tente o [link direto para o YouTube]({final_url}).")

                    st.divider()

                st.success("Plano de ação multimídia concluído!")

            except Exception as e:
                st.error(f"Ocorreu um erro inesperado durante a execução. Detalhes: {e}")
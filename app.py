import streamlit as st
import google.generativeai as genai
import json
from urllib.parse import quote_plus # Para criar links de busca seguros

# --- Configuração da Página e Título ---
st.set_page_config(page_title="Resolvedor.AI", page_icon="🏆")
st.title("🏆 Resolvedor.AI")
st.caption("Seu assistente para planos de ação claros e diretos.")

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
        placeholder="Ex: Minha pia da cozinha está vazando, como consertar?"
    )
    submitted = st.form_submit_button("Gerar Plano de Ação")

# --- Lógica Principal ---
if submitted:
    if not user_problem:
        st.error("Por favor, descreva o problema que você quer resolver.")
    else:
        # PROMPT PIVOTADO: Foco no que funciona: texto e links de busca.
        prompt_template = f"""
            Você é o 'Resolvedor.AI', um especialista em criar planos de ação textuais.
            O problema do usuário é: "{user_problem}"

            Sua tarefa é criar um plano em JSON com passos claros.
            Para passos que se beneficiariam de um vídeo, use o tipo "search_link" e, no campo "content", coloque uma frase de busca ideal para o YouTube.
            Para todos os outros, use o tipo "text".

            Estrutura do JSON:
            {{
                "title": "Um título claro para o plano",
                "difficulty": "Fácil, Médio ou Difícil",
                "estimated_time": "Ex: 20-40 minutos",
                "steps": [
                    {{
                        "type": "text | search_link",
                        "title": "O título descritivo do passo.",
                        "content": "O texto da instrução OU a frase de busca para o YouTube."
                    }}
                ]
            }}
            Retorne APENAS o JSON.
            """

        with st.spinner("Construindo seu plano de ação..."):
            try:
                # Voltamos para o Flash: Rápido, barato e perfeito para esta tarefa.
                model = genai.GenerativeModel('gemini-1.5-flash')
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

                    elif step_type == "search_link":
                        # Criamos a URL de busca do YouTube
                        search_query = quote_plus(step_content)
                        youtube_url = f"https://www.youtube.com/watch?v=yuVUcOwjTYc3"
                        st.markdown(f"Para uma demonstração visual, pode ser útil buscar vídeos sobre este tópico.")
                        # st.button não suporta links diretos, então usamos st.link_button
                        st.link_button(f'🔎 Buscar no YouTube por "{step_content}"', youtube_url)

                    st.divider()

                st.success("Plano de ação concluído!")

            except Exception as e:
                st.error(f"Ocorreu um erro inesperado. Detalhes: {e}")
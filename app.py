import streamlit as st
import google.generativeai as genai
import json

# --- Configuração da Página e Título ---
st.set_page_config(page_title="Resolvedor.AI Pro", page_icon="💡")
st.title("💡 Resolvedor.AI Pro")
st.caption("Planos de ação com a máxima qualidade de IA.")

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

    submitted = st.form_submit_button("Gerar Plano de Ação Inteligente")

# --- Lógica Principal ---
if submitted:
    if not user_problem:
        st.error("Por favor, descreva o problema que você quer resolver.")
    else:
        # AQUI ESTÁ A GRANDE MUDANÇA: O PROMPT HIPER-ESPECÍFICO
        prompt_template = f"""
            Você é o 'Resolvedor.AI', um especialista em criar planos de ação multímidia.
            Um usuário tem o seguinte problema: "{user_problem}"

            Sua tarefa é criar um plano de ação detalhado, retornando a resposta EXCLUSIVAMENTE em formato JSON.
            Para cada passo da solução, use sua capacidade de busca avançada:
            1.  Para passos que exigem uma demonstração em vídeo, use o tipo "video". Encontre no YouTube o melhor e mais relevante vídeo tutorial.
                A URL retornada no campo "content" DEVE OBRIGATORIAMENTE estar em um formato público e direto do YouTube.
                Formatos válidos: `https://www.youtube.com/watch?v=...` ou `https://youtu.be/...`
                NÃO retorne de forma alguma URLs com 'googleusercontent.com' ou qualquer outro formato de link interno. Se não encontrar um vídeo adequado, retorne um passo do tipo "text" explicando o que fazer.
            2.  Para passos visuais simples, use o tipo "gif". A URL deve ser pública e terminar em .gif, .webp, etc.
            3.  Para todos os outros passos, use o tipo "text".

            O JSON deve seguir esta estrutura exata:
            {{
                "title": "Um título claro e objetivo para o plano",
                "difficulty": "Fácil, Médio ou Difícil",
                "estimated_time": "Ex: 10-20 minutos",
                "steps": [
                    {{
                        "type": "text | gif | video",
                        "title": "O título descritivo do passo.",
                        "content": "A URL do gif, a URL do vídeo do YouTube ou o texto da instrução."
                    }}
                ]
            }}

            Retorne APENAS o código JSON, sem nenhum outro texto antes ou depois.
            """

        with st.spinner(f"Consultando o modelo {selected_model}... Buscando as melhores mídias..."):
            try:
                model = genai.GenerativeModel(selected_model)
                response = model.generate_content(prompt_template)

                clean_response_text = response.text.strip().replace("```json", "").replace("```", "")

                plan = json.loads(clean_response_text)

                # --- Renderização do Plano ---
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

                    elif step_type == "video":
                        st.video(step_content)
                        # LINHA DE INVESTIGAÇÃO: Vamos mostrar a URL exata que a IA nos deu.
                        st.code(f"URL recebida da IA: {step_content}", language=None)
                        st.markdown(f"Se o vídeo não aparecer, [clique aqui para abrir no YouTube]({step_content})")

                    st.divider()

                st.success("Plano de ação multimídia concluído!")

            except json.JSONDecodeError:
                st.error("Ocorreu um erro ao processar a resposta da IA. A resposta não estava no formato JSON esperado. Por favor, tente novamente.")
                st.text("Resposta recebida (para depuração):")
                st.code(clean_response_text)
            except Exception as e:
                st.error(f"Ocorreu um erro inesperado: {e}")
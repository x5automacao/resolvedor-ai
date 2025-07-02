import streamlit as st
import google.generativeai as genai
import json # Importamos a biblioteca para trabalhar com JSON

# --- Configuração da Página e Título ---
st.set_page_config(page_title="Resolvedor.AI v2.0", page_icon="🚀")
st.title("🚀 Resolvedor.AI v2.0")
st.caption("Planos de ação com textos, GIFs e vídeos.")

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
        placeholder="Ex: Como trocar a resistência do chuveiro Lorenzetti?"
    )
    submitted = st.form_submit_button("Gerar Plano de Ação Multimídia")

# --- Lógica Principal ---
if submitted:
    if not user_problem:
        st.error("Por favor, descreva o problema que você quer resolver.")
    else:
        # O NOVO "Mega-Prompt" v2.0 que pede uma saída em JSON
        prompt_template = f"""
            Você é o 'Resolvedor.AI', um especialista em criar planos de ação multímidia.
            Um usuário tem o seguinte problema: "{user_problem}"

            Sua tarefa é criar um plano de ação detalhado, retornando a resposta EXCLUSIVAMENTE em formato JSON.
            Para cada passo da solução, analise a complexidade:
            1.  Para passos simples e muito visuais (ex: "clique no menu Iniciar"), use o tipo "gif" e encontre na internet uma URL de um GIF animado relevante.
            2.  Para passos complexos que exigem uma demonstração (ex: "soldar um fio"), use o tipo "video" e encontre no YouTube o melhor vídeo tutorial, fornecendo a URL. Tente encontrar um link com timestamp (ex: &t=123s) se o vídeo for longo.
            3.  Para passos conceituais ou textuais, use o tipo "text".

            O JSON deve seguir esta estrutura exata:
            {{
                "title": "Um título claro e objetivo para o plano",
                "difficulty": "Fácil, Médio ou Difícil",
                "estimated_time": "Ex: 20-40 minutos",
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

        with st.spinner("Criando um plano de ação multimídia... Isso pode levar um momento..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-pro') # Usando o modelo Pro para tarefas mais complexas
                response = model.generate_content(prompt_template)
                
                # Decodifica a resposta JSON
                plan = json.loads(response.text)

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
                        # st.image pode exibir GIFs diretamente da URL
                        st.image(step_content, use_column_width=True)
                        
                    elif step_type == "video":
                        # st.video funciona perfeitamente com links do YouTube
                        st.video(step_content)
                    
                    st.divider()

                st.success("Plano de ação multimídia concluído!")

            except json.JSONDecodeError:
                st.error("Ocorreu um erro ao processar a resposta da IA. A resposta não estava no formato JSON esperado. Por favor, tente novamente.")
                st.text("Resposta recebida (para depuração):")
                st.code(response.text) # Mostra o que a IA retornou para ajudar a depurar
            except Exception as e:
                st.error(f"Ocorreu um erro inesperado: {e}")
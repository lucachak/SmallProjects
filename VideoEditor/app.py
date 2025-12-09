import streamlit as st
import os
import tempfile
from video_processor import VideoProcessor, TriggerConfig
import time

# Configuração da página
st.set_page_config(
    page_title="🎬 Smart Video Editor",
    page_icon="✂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Cabeçalho
    st.markdown('<h1 class="main-header">🎬 Smart Video Editor</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar com informações
    with st.sidebar:
        st.header("ℹ️ Sobre")
        st.markdown("""
        **Como funciona:**
        1. 📹 Faça upload dos vídeos
        2. 🖼️ Faça upload das imagens de trigger
        3. ⚙️ Configure a sensibilidade
        4. ✂️ Processe automaticamente
        
        **O que são Triggers:**
        São imagens que, quando aparecem no vídeo, 
        determinam onde o corte será feito.
        
        **Modos de Corte:**
        - **After**: Mantém do início até o trigger
        - **Before**: Mantém do trigger até o fim
        """)
        
        st.header("🔧 Configurações")
        cut_mode = st.selectbox(
            "Modo de Corte",
            ["after", "before"],
            format_func=lambda x: "After (início → trigger)" if x == "after" else "Before (trigger → fim)"
        )
        
        threshold = st.slider(
            "Sensibilidade do Trigger",
            min_value=0.1,
            max_value=1.0,
            value=0.8,
            help="Valores mais altos = match mais exato, mais baixo = match mais flexível"
        )
    
    # Área principal
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("📹 Upload de Vídeos")
        uploaded_videos = st.file_uploader(
            "Selecione os vídeos para editar",
            type=['mp4', 'avi', 'mov', 'mkv'],
            accept_multiple_files=True,
            help="Podem ser selecionados múltiplos vídeos"
        )
        
        if uploaded_videos:
            st.success(f"✅ {len(uploaded_videos)} vídeo(s) carregado(s)")
            for video in uploaded_videos:
                st.write(f"📼 {video.name} ({video.size // (1024*1024)} MB)")
    
    with col2:
        st.header("🖼️ Upload de Triggers")
        uploaded_triggers = st.file_uploader(
            "Selecione as imagens de trigger",
            type=['jpg', 'jpeg', 'png'],
            accept_multiple_files=True,
            help="O vídeo será cortado na PRIMEIRA imagem que aparecer"
        )
        
        if uploaded_triggers:
            st.success(f"✅ {len(uploaded_triggers)} trigger(s) carregado(s)")
            for trigger in uploaded_triggers:
                st.write(f"🎯 {trigger.name}")
    
    # Processamento
    if uploaded_videos and uploaded_triggers:
        st.markdown("---")
        st.header("⚡ Processamento")
        
        if st.button("🎬 Iniciar Processamento", type="primary", use_container_width=True):
            
            # Cria arquivos temporários
            with tempfile.TemporaryDirectory() as temp_dir:
                # Salva vídeos
                video_paths = []
                for video in uploaded_videos:
                    video_path = os.path.join(temp_dir, video.name)
                    with open(video_path, 'wb') as f:
                        f.write(video.getvalue())
                    video_paths.append(video_path)
                
                # Salva triggers e cria configurações
                triggers = []
                for trigger in uploaded_triggers:
                    trigger_path = os.path.join(temp_dir, trigger.name)
                    with open(trigger_path, 'wb') as f:
                        f.write(trigger.getvalue())
                    triggers.append(TriggerConfig(
                        image_path=trigger_path,
                        threshold=threshold,
                        name=trigger.name
                    ))
                
                # Barra de progresso
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Processa cada vídeo
                results = []
                for i, video_path in enumerate(video_paths):
                    status_text.text(f"Processando {i+1}/{len(video_paths)}: {os.path.basename(video_path)}")
                    
                    processor = VideoProcessor(video_path)
                    output_path = os.path.join(temp_dir, f"edited_{os.path.basename(video_path)}")
                    
                    result = processor.cut_video_at_trigger(triggers, output_path, cut_mode)
                    result['video_name'] = os.path.basename(video_path)
                    results.append(result)
                    
                    progress_bar.progress((i + 1) / len(video_paths))
                    time.sleep(0.5)  # Pequena pausa para visualização
                
                status_text.text("✅ Processamento concluído!")
                
                # Mostra resultados
                st.markdown("---")
                st.header("📊 Resultados")
                
                success_count = sum(1 for r in results if r['success'])
                st.metric("Vídeos Processados com Sucesso", f"{success_count}/{len(results)}")
                
                for result in results:
                    if result['success']:
                        with st.expander(f"✅ {result['video_name']}", expanded=True):
                            st.markdown(f"""
                            <div class="success-box">
                            **Trigger encontrado:** {result['trigger_name']}  
                            **Posição:** {result['cut_position']:.2f}s  
                            **Similaridade:** {result['similarity']:.3f}  
                            **Status:** {result['message']}
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Botão de download
                            with open(result['output_path'], 'rb') as f:
                                st.download_button(
                                    label="📥 Baixar Vídeo Editado",
                                    data=f,
                                    file_name=f"edited_{result['video_name']}",
                                    mime="video/mp4",
                                    key=result['video_name']
                                )
                    else:
                        with st.expander(f"❌ {result['video_name']}", expanded=False):
                            st.markdown(f"""
                            <div class="error-box">
                            **Erro:** {result.get('error', 'Erro desconhecido')}  
                            {result.get('best_match', '')}
                            </div>
                            """, unsafe_allow_html=True)
    
    elif not uploaded_videos and not uploaded_triggers:
        # Tela inicial
        st.markdown("""
        <div class="info-box">
        <h3>👋 Bem-vindo ao Smart Video Editor!</h3>
        <p>Esta ferramenta usa <strong>visão computacional</strong> para editar seus vídeos automaticamente.</p>
        
        <h4>🎯 Como usar:</h4>
        <ol>
            <li>Faça upload dos vídeos que deseja editar</li>
            <li>Faça upload das imagens que servirão como "gatilho" para o corte</li>
            <li>Configure a sensibilidade (quão parecida a imagem precisa ser)</li>
            <li>Clique em "Iniciar Processamento"</li>
        </ol>
        
        <h4>🔧 Tecnologias usadas:</h4>
        <ul>
            <li>OpenCV para detecção de imagens</li>
            <li>FFmpeg para processamento de vídeo</li>
            <li>Streamlit para interface web</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    elif not uploaded_videos:
        st.warning("⚠️ Por favor, faça upload de pelo menos um vídeo")
    elif not uploaded_triggers:
        st.warning("⚠️ Por favor, faça upload de pelo menos uma imagem de trigger")

if __name__ == "__main__":
    main()

# abas/disparos.py
import streamlit as st
import threading
import time
import subprocess
import os
import queue # Importar a biblioteca queue

# importe sua função do cad_verify
# Certifique-se de que cad_verify.py está no diretório base ou em um caminho acessível
try:
    from scripts.cad_verify import detecta_nova_ocorrencia
except ImportError:
    st.error("Erro: Não foi possível importar 'detecta_nova_ocorrencia' de cad_verify.py")
    st.stop() # Parar a execução do Streamlit se a importação falhar

# Fila para comunicação do worker para o thread principal do Streamlit
# A fila será armazenada no session_state para persistir entre reruns
if 'status_queue' not in st.session_state:
    st.session_state.status_queue = queue.Queue()

# Lista para armazenar as mensagens de log a serem exibidas
if 'disparos_log' not in st.session_state:
    st.session_state.disparos_log = []

# Flag para controlar o estado da thread worker
if 'disparos_thread' not in st.session_state:
    st.session_state.disparos_thread = None
    st.session_state.stop_event = threading.Event()

def worker(stop_event: threading.Event, status_queue: queue.Queue, base_dir: str, paths: dict):
    """Função que roda na thread separada para checar e disparar scripts."""
    status_queue.put("Thread de disparos iniciada. Aguardando ocorrências...")
    
    while not stop_event.is_set():
        try:
            # 1) checa ocorrência
            status_queue.put("Verificando novas ocorrências no CAD...")
            ocorrencia_detectada = detecta_nova_ocorrencia()

            if ocorrencia_detectada:
                status_queue.put("🆕 NOVA OCORRÊNCIA detectada! Executando scripts...")
                
                # 2) executa main.py
                status_queue.put(f"Executando: {paths['main']}")
                # Use check=True para levantar exceção em caso de erro no subprocesso
                subprocess.run(["python", paths["main"]], cwd=base_dir, check=True) 
                status_queue.put("✅ main.py finalizado.")

                # 3) executa organize.py
                status_queue.put(f"Executando: {paths['organize']}")
                subprocess.run(["python", paths["organize"]], cwd=base_dir, check=True)
                status_queue.put("✅ organize.py finalizado.")

                # 4) executa whatsapp_sender.py
                status_queue.put(f"Executando: {paths['whatsapp']}")
                subprocess.run(["python", paths["whatsapp"]], cwd=base_dir, check=True)
                status_queue.put("✅ whatsapp_sender.py finalizado.")

                status_queue.put("✅ Ciclo de scripts finalizado. Voltando à espera...")

            else:
                 status_queue.put("Nenhuma nova ocorrência detectada.")


            # intervalo entre checagens
            # Use a non-blocking sleep that checks the stop event periodically
            # This makes the thread more responsive to the stop command
            sleep_interval = 5 # seconds
            for _ in range(int(sleep_interval * 10)): # Check stop event 10 times per second
                if stop_event.is_set():
                    break
                time.sleep(0.1)

        except subprocess.CalledProcessError as e:
             status_queue.put(f"❌ Erro na execução de um script: {e}")
             status_queue.put("Parando disparos devido a erro.")
             stop_event.set() # Stop the thread on script error

        except Exception as e:
            status_queue.put(f"❌ Erro inesperado na thread de disparos: {e}")
            status_queue.put("Parando disparos devido a erro inesperado.")
            stop_event.set() # Stop the thread on other errors

    status_queue.put("Thread de disparos encerrada.")


def aba_disparos(base_dir: str):
    """Conteúdo e lógica para a aba de Disparos."""
    st.header("Gerenciamento de Disparos Automáticos")
    st.write("Inicie ou pare a checagem contínua de novas ocorrências e o disparo automático dos scripts.")

    # Caminhos absolutos dos scripts a serem executados
    paths = {
        "main":       os.path.join(base_dir, "main.py"),
        "organize":   os.path.join(base_dir, "organize.py"),
        "whatsapp":   os.path.join(base_dir, "whatsapp_sender.py")
    }

    # --- Botões Iniciar / Parar ---
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Iniciar Disparos"):
            th = st.session_state.disparos_thread
            # Só inicia se não houver uma thread rodando ou se a thread anterior morreu
            if th is None or not th.is_alive():
                # Limpa a fila e o log antes de iniciar um novo ciclo
                while not st.session_state.status_queue.empty():
                    st.session_state.status_queue.get()
                st.session_state.disparos_log = []

                st.session_state.stop_event.clear() # Garante que o stop event está limpo
                
                # Cria e inicia a thread worker
                t = threading.Thread(
                    target=worker,
                    args=(st.session_state.stop_event, st.session_state.status_queue, base_dir, paths),
                    daemon=True # Daemon=True faz a thread parar quando o Streamlit para
                )
                t.start()
                st.session_state.disparos_thread = t
                st.session_state.disparos_log.append("✅ Comando de Início recebido.")
                st.rerun() # Rerun para atualizar o estado e o log imediatamente
            else:
                st.warning("Os disparos já estão rodando.")

    with col2:
        if st.button("⏹️ Parar Disparos"):
            th = st.session_state.disparos_thread
            if th and th.is_alive():
                st.session_state.stop_event.set() # Sinaliza para a thread parar
                # Não chame th.join() aqui, pois isso bloquearia o thread principal do Streamlit
                st.session_state.disparos_log.append("⏳ Comando de Parada recebido. Aguardando thread finalizar...")
                st.rerun() # Rerun para atualizar o estado e o log imediatamente
            else:
                st.info("Não há disparos em execução.")

    # --- Área de Status e Log ---
    st.subheader("Status e Log")

    # Verifica o estado da thread e exibe
    is_running = st.session_state.disparos_thread and st.session_state.disparos_thread.is_alive()
    if is_running:
        st.text("Status: ▶️ Rodando...")
    else:
        # Se não está rodando, pode ser porque parou, terminou ou nunca iniciou
        if st.session_state.stop_event.is_set() and st.session_state.disparos_thread and not st.session_state.disparos_thread.is_alive():
             st.text("Status: ⏹️ Parado.")
        elif st.session_state.disparos_thread is None:
             st.text("Status: ⚪ Inativo (Pressione Iniciar).")
        else:
             st.text("Status: ❗ Thread finalizou inesperadamente.") # Caso a thread morra por erro

    # Processa as mensagens da fila para o log de exibição
    while not st.session_state.status_queue.empty():
        try:
            message = st.session_state.status_queue.get_nowait()
            st.session_state.disparos_log.append(message)
            # Opcional: limitar o tamanho do log para não ocupar muita memória
            max_log_size = 100
            if len(st.session_state.disparos_log) > max_log_size:
                 st.session_state.disparos_log = st.session_state.disparos_log[-max_log_size:]
        except queue.Empty:
            # Fila vazia, sair do loop
            break
    
    # Exibe o log
    # Use um text_area para exibir o log de forma contínua
    log_text = "\n".join(st.session_state.disparos_log)
    st.text_area("Detalhes do Disparo:", log_text, height=300)

    # Nota: O log só será atualizado na UI quando ocorrer um "rerun" do script Streamlit
    # (por exemplo, ao clicar em um botão, mudar de aba, ou no início/fim do processo).
    # Streamlit não tem atualização em tempo real automática a partir de threads sem bibliotecas adicionais.


import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Foto de Natal", page_icon="🎄", layout="centered")

st.title("🎄Natal da Equipe")
st.markdown("Escolha seu cenário abaixo, alinhe o rosto e envie sua foto diretamente para o nosso mural base.")

# Código HTML encapsulado com links absolutos e correção do CORS (Cross-Origin)
html_code = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-color: #0c3b2e; 
            color: white;
            padding: 10px;
            margin: 0;
        }
        .container {
            max-width: 400px;
            margin: 0 auto;
            background: #b22222; 
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }
        input, select, button {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            border-radius: 8px;
            border: none;
            font-size: 16px;
            box-sizing: border-box;
        }
        button {
            background-color: #ffcc00;
            color: #333;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
        }
        button:disabled { background-color: #999; cursor: not-allowed; }
        
        .camera-box {
            position: relative;
            width: 100%;
            max-width: 350px;
            margin: 15px auto;
            border-radius: 10px;
            overflow: hidden;
            background: #000;
            display: none;
        }
        video {
            width: 100%;
            display: block;
            transform: scaleX(-1);
        }
        #moldura-preview {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 10;
            pointer-events: none; 
        }
        #status-envio { font-weight: bold; color: #ffeb3b; margin-top: 10px; display: none; }
    </style>
</head>
<body>

    <div class="container">
        <h2>🎄 Captura de Natal 🎅</h2>
        
        <input type="text" id="nome" placeholder="Seu Nome (Ex: Joao Silva)">
        
        <!-- Apontando obrigatoriamente para os links absolutos do GitHub -->
        <select id="tema" onchange="trocarMoldura()">
            <option value="https://elcioflaviano-dev.github.io/FOTO/natal/1.png">Cenário 1</option>
            <option value="https://elcioflaviano-dev.github.io/FOTO/natal/2.png">Cenário 2</option>
            <option value="https://elcioflaviano-dev.github.io/FOTO/natal/3.png">Cenário 3</option>
            <option value="https://elcioflaviano-dev.github.io/FOTO/natal/4.png">Cenário 4</option>
            <option value="https://elcioflaviano-dev.github.io/FOTO/natal/5.png">Cenário 5</option>
            <option value="https://elcioflaviano-dev.github.io/FOTO/natal/6.png">Cenário 6</option>
            <option value="https://elcioflaviano-dev.github.io/FOTO/natal/7.png">Cenário 7</option>
            <option value="https://elcioflaviano-dev.github.io/FOTO/natal/8.png">Cenário 8</option>
            <option value="https://elcioflaviano-dev.github.io/FOTO/natal/9.png">Cenário 9</option>
            <option value="https://elcioflaviano-dev.github.io/FOTO/natal/10.png">Cenário 10</option>
            <option value="https://elcioflaviano-dev.github.io/FOTO/natal/11.png">Cenário 11</option>
            <option value="https://elcioflaviano-dev.github.io/FOTO/natal/12.png">Cenário 12</option>
            <option value="https://elcioflaviano-dev.github.io/FOTO/natal/13.png">Cenário 13</option>
            <option value="https://elcioflaviano-dev.github.io/FOTO/natal/14.png">Cenário 14</option>
            <option value="https://elcioflaviano-dev.github.io/FOTO/natal/15.png">Cenário 15</option>
            <option value="https://elcioflaviano-dev.github.io/FOTO/natal/16.png">Cenário 16</option>
        </select>
        
        <button id="btn-iniciar" onclick="iniciarCamera()">1. Ativar Câmera</button>
        
        <div class="camera-box" id="camera-box">
            <video id="video" autoplay playsinline></video>
            <!-- Permissão crossorigin explícita adicionada aqui -->
            <img id="moldura-preview" src="https://elcioflaviano-dev.github.io/FOTO/natal/1.png" alt="Moldura" crossorigin="anonymous">
        </div>
        
        <canvas id="canvas" style="display:none;"></canvas>
        <p id="status-envio">Enviando para a pasta Natal (Drive)... 🛷</p>

        <div id="controles" style="display:none; margin-top: 15px;">
            <button id="btn-capturar" onclick="capturar()">📸 Capturar e Enviar</button>
        </div>
    </div>

    <script>
        const SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxsh8xXp6UfvNZR7ts3gadeUWwogMI8pro6PWIOEX-PnvVCl1lvF9SYyXgJvQKENC1CVw/exec";

        const video = document.getElementById('video');
        const molduraPreview = document.getElementById('moldura-preview');
        const canvas = document.getElementById('canvas');
        const controles = document.getElementById('controles');
        const statusEnvio = document.getElementById('status-envio');
        const btnCapturar = document.getElementById('btn-capturar');

        function trocarMoldura() {
            const temaSelecionado = document.getElementById('tema').value;
            // Força o navegador a aceitar a imagem hospedada fora do Streamlit
            molduraPreview.setAttribute('crossorigin', 'anonymous');
            molduraPreview.src = temaSelecionado;
        }

        async function iniciarCamera() {
            try {
                // Medidas invertidas para formato Retrato (em pé), removendo o corte de zoom
                const stream = await navigator.mediaDevices.getUserMedia({
                    video: { 
                        facingMode: "user", 
                        width: { ideal: 1080 }, 
                        height: { ideal: 1920 } 
                    }
                });
                video.srcObject = stream;
                document.getElementById('camera-box').style.display = "block";
                controles.style.display = "block";
                document.getElementById('btn-iniciar').style.display = "none";
            } catch (erro) {
                alert("Erro ao acessar a câmera. Verifique permissões.");
            }
        }

        async function capturar() {
            const nome = document.getElementById('nome').value.trim().replace(/ /g, '_'); 
            const urlParts = document.getElementById('tema').value.split('/');
            const tema = urlParts[urlParts.length - 1].replace('.png', '');

            if (!nome) {
                alert("Por favor, preencha o seu nome antes de tirar a foto!");
                return;
            }

            btnCapturar.disabled = true;
            statusEnvio.style.display = "block";

            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext('2d');
            
            ctx.translate(canvas.width, 0);
            ctx.scale(-1, 1);
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            
            ctx.translate(canvas.width, 0);
            ctx.scale(-1, 1);
            ctx.drawImage(molduraPreview, 0, 0, canvas.width, canvas.height);

            const imagemFinal = canvas.toDataURL('image/jpeg', 0.9);
            const nomeArquivo = `Natal_${nome}_Cenario_${tema}.jpg`;

            try {
                await fetch(SCRIPT_URL, {
                    method: 'POST',
                    mode: 'no-cors',
                    headers: { 'Content-Type': 'text/plain' },
                    body: JSON.stringify({ filename: nomeArquivo, image: imagemFinal })
                });
                
                btnCapturar.innerText = "✅ Foto Enviada! Feliz Natal!";
                btnCapturar.style.backgroundColor = "#28a745";
            } catch (erro) {
                alert("Erro de conexão ao enviar para o Drive.");
                btnCapturar.disabled = false;
                btnCapturar.innerText = "📸 Tentar Novamente";
            } finally {
                statusEnvio.style.display = "none";
            }
        }
    </script>
</body>
</html>
"""

# Renderiza o HTML dentro do Streamlit, reservando altura suficiente para a câmera e controles
components.html(html_code, height=850, scrolling=True)

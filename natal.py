import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Foto de Natal", page_icon="🎄", layout="centered")

st.title("🎄Natal da Equipe")
st.markdown("Escolha seu cenário, **ajuste o tamanho do seu rosto** na barra deslizando para os lados e envie sua foto!")

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
            padding: 5px;
            margin: 0;
        }
        .container {
            width: 100%;
            max-width: 100%;
            margin: 0 auto;
            background: #b22222; 
            padding: 10px;
            border-radius: 12px;
            box-sizing: border-box;
        }
        input[type="text"], select, button {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            border-radius: 8px;
            border: none;
            font-size: 16px;
            box-sizing: border-box;
        }
        /* Estilo da barra de zoom */
        input[type="range"] {
            width: 100%;
            margin: 10px 0 15px 0;
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
            max-width: 100%;
            aspect-ratio: 3 / 4; 
            margin: 10px auto;
            border-radius: 10px;
            overflow: hidden;
            background: #000;
            display: none;
            /* Centraliza o vídeo para quando ele for reduzido pelo zoom */
            display: flex;
            justify-content: center;
            align-items: center;
        }
        video {
            width: 100%;
            height: 100%;
            object-fit: cover;
            /* O zoom padrão começa em 0.8 (levemente menor) para caber melhor o rosto */
            transform: scaleX(-1) scale(0.8);
            transition: transform 0.1s;
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
        
        <!-- Bloco de câmera e controles de captura que aparecem depois -->
        <div id="area-captura" style="display:none;">
            
            <label for="zoom" style="font-size: 14px; display: block; margin-top: 10px;">🔍 Ajustar Tamanho do Rosto:</label>
            <input type="range" id="zoom" min="0.4" max="1.5" step="0.05" value="0.8" oninput="ajustarZoom()">

            <div class="camera-box" id="camera-box">
                <video id="video" autoplay playsinline></video>
                <img id="moldura-preview" src="https://elcioflaviano-dev.github.io/FOTO/natal/1.png" alt="Moldura" crossorigin="anonymous">
            </div>
            
            <canvas id="canvas" style="display:none;"></canvas>
            <p id="status-envio">Enviando para a pasta Natal (Drive)... 🛷</p>

            <div id="controles" style="margin-top: 15px;">
                <button id="btn-capturar" onclick="capturar()">📸 Capturar e Enviar</button>
            </div>
        </div>
    </div>

    <script>
        const SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxsh8xXp6UfvNZR7ts3gadeUWwogMI8pro6PWIOEX-PnvVCl1lvF9SYyXgJvQKENC1CVw/exec";

        const video = document.getElementById('video');
        const molduraPreview = document.getElementById('moldura-preview');
        const canvas = document.getElementById('canvas');
        const areaCaptura = document.getElementById('area-captura');
        const statusEnvio = document.getElementById('status-envio');
        const btnCapturar = document.getElementById('btn-capturar');

        function trocarMoldura() {
            const temaSelecionado = document.getElementById('tema').value;
            molduraPreview.setAttribute('crossorigin', 'anonymous');
            molduraPreview.src = temaSelecionado;
        }

        // Função nova para aplicar o zoom no vídeo em tempo real
        function ajustarZoom() {
            const zoom = document.getElementById('zoom').value;
            // Mantém o vídeo espelhado (scaleX -1) e aplica o zoom escolhido
            video.style.transform = `scaleX(-1) scale(${zoom})`;
        }

        async function iniciarCamera() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({
                    video: { facingMode: "user", width: { ideal: 960 }, height: { ideal: 1280 } }
                });
                video.srcObject = stream;
                
                // Exibe a área de captura com o vídeo e o slider
                areaCaptura.style.display = "block";
                document.getElementById('camera-box').style.display = "flex";
                document.getElementById('btn-iniciar').style.display = "none";
            } catch (erro) {
                alert("Erro ao acessar a câmera. Verifique permissões.");
            }
        }

        async function capturar() {
            const nome = document.getElementById('nome').value.trim().replace(/ /g, '_'); 
            const urlParts = document.getElementById('tema').value.split('/');
            const tema = urlParts[urlParts.length - 1].replace('.png', '');
            const zoom = parseFloat(document.getElementById('zoom').value);

            if (!nome) {
                alert("Por favor, preencha o seu nome antes de tirar a foto!");
                return;
            }

            btnCapturar.disabled = true;
            statusEnvio.style.display = "block";

            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext('2d');
            
            // Pinta o fundo de preto caso o vídeo tenha sido muito reduzido pelo zoom
            ctx.fillStyle = "#000000";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Aplica a mesma matemática do zoom no canvas antes de "bater a foto"
            ctx.save();
            ctx.translate(canvas.width / 2, canvas.height / 2);
            ctx.scale(-zoom, zoom); // Escala negativa no X para espelhar
            ctx.drawImage(video, -canvas.width / 2, -canvas.height / 2, canvas.width, canvas.height);
            ctx.restore();
            
            // Desenha a moldura por cima, sem aplicar zoom nela
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

components.html(html_code, height=950, scrolling=True)

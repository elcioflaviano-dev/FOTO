import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Foto de Natal", page_icon="🎄", layout="centered")

st.title("🎄Natal da Equipe")
st.markdown("Escolha seu cenário, **ajuste o tamanho e a altura do rosto** e envie sua foto!")

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
        input[type="range"] {
            width: 100%;
            margin: 5px 0 10px 0;
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
            max-width: 350px; /* Limitado para ficar mais estreito e focado no rosto */
            aspect-ratio: 4 / 5; /* Formato mais vertical e estreito */
            margin: 10px auto;
            border-radius: 10px;
            overflow: hidden;
            background: #000;
            display: none;
        }
        video {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            transform: translateY(-10%) scaleX(-1) scale(0.9); /* Ajustado para aproximar mais o rosto */
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
        
        .controles-duplos {
            display: flex;
            justify-content: space-between;
            gap: 15px;
            margin-top: 10px;
            background: rgba(0,0,0,0.2);
            padding: 10px;
            border-radius: 8px;
        }
        .controle-item {
            flex: 1;
            text-align: left;
        }
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
        
        <div id="area-captura" style="display:none;">
            
            <div class="controles-duplos">
                <div class="controle-item">
                    <label for="zoom" style="font-size: 13px; font-weight: bold;">🔍 Tamanho:</label>
                    <input type="range" id="zoom" min="0.4" max="1.8" step="0.05" value="0.9" oninput="ajustarCamera()">
                </div>
                <div class="controle-item">
                    <label for="pos-y" style="font-size: 13px; font-weight: bold;">↕️ Altura:</label>
                    <input type="range" id="pos-y" min="-50" max="50" step="2" value="-10" oninput="ajustarCamera()">
                </div>
            </div>

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

        function ajustarCamera() {
            const zoom = document.getElementById('zoom').value;
            const posY = document.getElementById('pos-y').value;
            video.style.transform = `translateY(${posY}%) scaleX(-1) scale(${zoom})`;
        }

        async function iniciarCamera() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({
                    video: { facingMode: "user", width: { ideal: 720 }, height: { ideal: 960 } }
                });
                video.srcObject = stream;
                
                areaCaptura.style.display = "block";
                document.getElementById('camera-box').style.display = "block";
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
            const posY = parseFloat(document.getElementById('pos-y').value);

            if (!nome) {
                alert("Por favor, preencha o seu nome antes de tirar a foto!");
                return;
            }

            btnCapturar.disabled = true;
            statusEnvio.style.display = "block";

            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext('2d');
            
            ctx.fillStyle = "#000000";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.save();
            ctx.translate(canvas.width / 2, canvas.height / 2);
            ctx.translate(0, canvas.height * (posY / 100));
            ctx.scale(-zoom, zoom);
            ctx.drawImage(video, -canvas.width / 2, -canvas.height / 2, canvas.width, canvas.height);
            ctx.restore();
            
            ctx.drawImage(molduraPreview, 0, 0, canvas.width, canvas.height);

            const imagemFinal = canvas.toDataURL('image/jpeg', 0.95);
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

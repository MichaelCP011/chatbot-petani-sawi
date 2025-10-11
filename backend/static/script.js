// backend/static/script.js

document.addEventListener("DOMContentLoaded", () => {
    // --- ELEMEN DOM ---
    const chatLog = document.getElementById("chat-log");
    const inputArea = document.getElementById("input-area");
    const API_BASE_URL = 'http://localhost:5000';
    let currentDiseaseName = '';

    // --- FUNGSI UTAMA ---

    function addMessage(text, sender) {
        const message = document.createElement("div");
        message.classList.add("chat-message", `${sender}-message`);
        message.innerText = text;
        chatLog.appendChild(message);
        chatLog.scrollTop = chatLog.scrollHeight;
    }
    
    // --- FUNGSI BARU UNTUK MENAMPILKAN GAMBAR ---
    function addImageMessage(file) {
        const message = document.createElement("div");
        message.classList.add("chat-message", "user-message");

        const img = document.createElement("img");
        img.classList.add("chat-image");

        // Gunakan FileReader untuk membuat URL sementara dari gambar
        const reader = new FileReader();
        reader.onload = (e) => {
            img.src = e.target.result;
        };
        reader.readAsDataURL(file);

        message.appendChild(img);
        chatLog.appendChild(message);
        chatLog.scrollTop = chatLog.scrollHeight;
    }

    function setInputArea(type, onSend, options = {}) {
        inputArea.innerHTML = '';
        const isDisabled = options.disabled || false;

        if (type === 'upload') {
            const fileInput = document.createElement("input");
            fileInput.type = "file";
            fileInput.accept = "image/*";
            fileInput.style.display = "none";
            fileInput.onchange = (e) => {
                const file = e.target.files[0];
                if (file) onSend(file);
            };
            document.body.appendChild(fileInput);

            const uploadButton = document.createElement("button");
            uploadButton.innerText = "Pilih Gambar untuk Dianalisis";
            uploadButton.disabled = isDisabled;
            uploadButton.onclick = () => fileInput.click();
            inputArea.appendChild(uploadButton);

        } else if (type === 'text') {
            const textInput = document.createElement("input");
            textInput.type = "text";
            textInput.placeholder = isDisabled ? "Sedang memproses..." : "Ketik pertanyaan Anda di sini...";
            textInput.className = "text-input";
            textInput.disabled = isDisabled;
            textInput.onkeydown = (e) => {
                if (e.key === 'Enter' && textInput.value.trim() !== "" && !isDisabled) {
                    onSend(textInput.value.trim());
                    textInput.value = "";
                }
            };
            inputArea.appendChild(textInput);
            if (!isDisabled) {
                textInput.focus();
            }
        }
    }

    async function handleImageUpload(file) {
        // --- PERUBAHAN DI SINI: Tampilkan gambar, bukan nama file ---
        addImageMessage(file); 
        
        addMessage("Menganalisis gambar dengan model CV...", "bot");
        setInputArea('upload', handleImageUpload, { disabled: true });

        const formData = new FormData();
        formData.append('image', file);

        try {
            const response = await fetch(`${API_BASE_URL}/api/diagnose`, { method: 'POST', body: formData });
            if (!response.ok) throw new Error('Gagal diagnosis.');
            
            const result = await response.json();
            const { disease_name, confidence, initial_response } = result.data;

            addMessage(`Hasil Diagnosis Model CV:\n- Penyakit: ${disease_name}\n- Keyakinan: ${confidence.toFixed(2)}%`, "bot");
            addMessage(initial_response, "bot");
            
            setInputArea('text', handleTextMessage, { disabled: false });
        } catch (error) {
            console.error(error);
            addMessage("Maaf, terjadi kesalahan.", "bot");
            setupInitialState();
        }
    }

    async function handleTextMessage(question) {
        addMessage(question, "user");
        addMessage("...", "bot");
        setInputArea('text', handleTextMessage, { disabled: true });

        try {
            const response = await fetch(`${API_BASE_URL}/api/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: question })
            });
            if (!response.ok) throw new Error('Gagal mendapat respons chat.');

            const result = await response.json();
            chatLog.removeChild(chatLog.lastChild);
            addMessage(result.data.answer, "bot");
            
            setInputArea('text', handleTextMessage, { disabled: false });
        } catch (error) {
            console.error(error);
            addMessage("Maaf, terjadi kesalahan.", "bot");
            setInputArea('text', handleTextMessage, { disabled: false });
        }
    }

    function setupInitialState() {
        addMessage("Selamat datang! Silakan unggah gambar daun cabai untuk memulai diagnosis.", "bot");
        setInputArea('upload', handleImageUpload);
    }

    setupInitialState();
});
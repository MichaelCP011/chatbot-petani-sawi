document.addEventListener("DOMContentLoaded", () => {
    // --- ELEMEN DOM ---
    const chatLog = document.getElementById("chat-log");
    const fileInput = document.getElementById("file-input");
    const uploadButton = document.getElementById("upload-button");
    const optionsContainer = document.getElementById("options-container");
    const API_BASE_URL = 'http://127.0.0.1:5000';
    let currentDiseaseName = '';

    // --- FUNGSI ---

    function addMessage(text, sender) {
        // ... (fungsi ini tidak perlu diubah)
        const message = document.createElement("div");
        message.classList.add("chat-message", `${sender}-message`);
        message.innerText = text;
        chatLog.appendChild(message);
        chatLog.scrollTop = chatLog.scrollHeight;
    }

    async function handleImageUpload() {
        // ================== PERANGKAP DEBUGGER ==================
        debugger; // Kode akan berhenti di sini saat DevTools terbuka
        // ======================================================
        
        console.log("1. FUNGSI handleImageUpload DIMULAI.");
        
        const file = fileInput.files[0];
        if (!file) {
            console.log("Tidak ada file, proses berhenti.");
            return;
        }

        addMessage(`Anda memilih: ${file.name}`, "user");
        addMessage("Menganalisis gambar...", "bot");
        uploadButton.innerText = "Memproses...";
        uploadButton.disabled = true;

        const formData = new FormData();
        formData.append('image', file);

        try {
            console.log("2. MENGIRIM request 'fetch' ke backend...");
            const response = await fetch(`${API_BASE_URL}/api/diagnose`, {
                method: 'POST',
                body: formData,
            });
            
            console.log("3. MENERIMA respons dari backend.", response);
            if (!response.ok) throw new Error('Gagal diagnosis.');

            const result = await response.json();
            console.log("4. Respons JSON BERHASIL di-parse.", result);
            
            const { disease_name, confidence, description, handling_options } = result.data;
            currentDiseaseName = disease_name;

            const reply = `Hasil Analisis:\n- Penyakit: ${disease_name}\n- Keyakinan: ${confidence.toFixed(2)}%`;
            addMessage(reply, "bot");
            addMessage(description, "bot");

            uploadButton.style.display = 'none';
            displayOptions(handling_options);
            console.log("5. SEMUA HASIL SELESAI DITAMPILKAN.");

        } catch (error) {
            console.error("TERJADI ERROR DI DALAM FETCH:", error);
            addMessage("Maaf, terjadi kesalahan.", "bot");
            resetToInitialState();
        }
    }

    function displayOptions(options) {
        // ... (fungsi ini tidak perlu diubah)
        optionsContainer.innerHTML = '';
        options.forEach(option => {
            const button = document.createElement("button");
            button.innerText = option.title;
            button.addEventListener("click", (e) => {
                e.preventDefault();
                handleOptionClick(option.action, option.title);
            });
            optionsContainer.appendChild(button);
        });
    }

    async function handleOptionClick(action, title) {
        // ... (fungsi ini tidak perlu diubah)
        addMessage(`Tanya: "${title}"`, "user");
        addMessage("Mencari info...", "bot");
        try {
            const response = await fetch(`${API_BASE_URL}/api/details?disease_name=${encodeURIComponent(currentDiseaseName)}&info_type=${action}`);
            if (!response.ok) throw new Error('Gagal mendapatkan detail.');
            const result = await response.json();
            addMessage(result.data.text, "bot");
        } catch (error) {
            console.error("Error:", error);
            addMessage("Maaf, gagal mengambil detail.", "bot");
        }
    }

    function resetToInitialState() {
        // ... (fungsi ini tidak perlu diubah)
        uploadButton.innerText = "Pilih Gambar untuk Dianalisis";
        uploadButton.disabled = false;
        uploadButton.style.display = 'block';
        optionsContainer.innerHTML = '';
        currentDiseaseName = '';
    }

    // --- EVENT LISTENERS ---
    uploadButton.addEventListener("click", (e) => {
        e.preventDefault();
        fileInput.click();
    });
    fileInput.addEventListener("change", handleImageUpload);

    // --- INISIALISASI ---
    addMessage("Selamat datang! Silakan pilih gambar daun cabai untuk dianalisis.", "bot");
});
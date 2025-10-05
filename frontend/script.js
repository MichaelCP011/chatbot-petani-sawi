// Menghubungkan elemen HTML ke JavaScript
const fileInput = document.getElementById('file-input');
const chatLog = document.getElementById('chat-log');
const inputContainer = document.getElementById('input-container');

const API_BASE_URL = 'http://127.0.0.1:5000';
let currentDiseaseName = '';

function addMessage(message, sender = 'bot') {
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message', `${sender}-message`);
    messageElement.style.whiteSpace = "pre-wrap"; 
    messageElement.innerText = message;
    chatLog.appendChild(messageElement);
    chatLog.scrollTop = chatLog.scrollHeight;
}

async function fetchAndDisplayDetails(diseaseName, infoType, buttonTitle) {
    // ... (fungsi ini tidak berubah)
    addMessage(`Anda memilih: "${buttonTitle}"`, 'user');
    addMessage(`Mencari info tentang ${buttonTitle}...`);
    try {
        const response = await fetch(`${API_BASE_URL}/api/details?disease_name=${encodeURIComponent(diseaseName)}&info_type=${infoType}`);
        if (!response.ok) throw new Error('Respon jaringan bermasalah.');
        const result = await response.json();
        addMessage(result.data.text);
    } catch (error) {
        console.error("Gagal mengambil detail:", error);
        addMessage("Maaf, gagal mengambil informasi detail dari server.");
    }
}

function displayOptions(options) {
    // ... (fungsi ini tidak berubah)
    inputContainer.innerHTML = '';
    options.forEach(option => {
        const button = document.createElement('button');
        button.innerText = option.title;
        button.addEventListener('click', () => {
            fetchAndDisplayDetails(currentDiseaseName, option.action, option.title);
        });
        inputContainer.appendChild(button);
    });
}

// --- FUNGSI BARU UNTUK MENGIRIM GAMBAR ---
async function handleImageUpload(file) {
    addMessage(`Anda memilih gambar: ${file.name}`, "user");
    addMessage("Menganalisis gambar...");

    // Buat FormData untuk mengirim file
    const formData = new FormData();
    formData.append('image', file);

    try {
        const response = await fetch(`${API_BASE_URL}/api/diagnose`, {
            method: 'POST',
            body: formData, // Kirim FormData sebagai body
            // PENTING: Jangan set header 'Content-Type', browser akan melakukannya secara otomatis
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.message || 'Gagal melakukan diagnosis.');
        }

        const result = await response.json();
        const diseaseInfo = result.data;

        currentDiseaseName = diseaseInfo.disease_name;

        const reply = `Hasil analisis (simulasi):\nNama Penyakit: ${diseaseInfo.disease_name}`;
        addMessage(reply);
        displayOptions(diseaseInfo.handling_options);

    } catch (error) {
        console.error("Error saat unggah gambar:", error);
        addMessage(`Maaf, terjadi kesalahan: ${error.message}`);
    }
}

// Event listener untuk input file
fileInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        handleImageUpload(file);
    }
});

addMessage("Selamat datang! Silakan pilih gambar daun sawi yang ingin dianalisis.");
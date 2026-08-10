document.addEventListener("DOMContentLoaded", () => {
  const textarea = document.getElementById("reviewInput");
  const charCount = document.getElementById("charCount");
  const submitBtn = document.getElementById("submitBtn");
  const btnText = document.getElementById("btnText");
  const btnSpinner = document.getElementById("btnSpinner");
  const resultPanel = document.getElementById("resultPanel");
  const sentimentBadge = document.getElementById("sentimentBadge");
  const confidenceText = document.getElementById("confidenceText");
  const progressBar = document.getElementById("progressBar");

  // Hitung Karakter Input
  textarea.addEventListener("input", () => {
    charCount.textContent = textarea.value.length;
  });

  // Event Listener Klik Tombol
  submitBtn.addEventListener("click", analyzeSentiment);

  async function analyzeSentiment() {
    const textInput = textarea.value.trim();

    if (!textInput) {
      alert("Silakan masukkan teks ulasan terlebih dahulu.");
      return;
    }

    // Set UI State Loading
    submitBtn.disabled = true;
    btnText.classList.add("hidden");
    btnSpinner.classList.remove("hidden");

    try {
      // Panggil endpoint /predict langsung di domain/port yang sama
      const response = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: textInput })
      });

      if (!response.ok) {
        throw new Error("Gagal mengambil respon dari API");
      }

      const data = await response.json();
      const sentiment = data.sentiment;
      const confidenceVal = parseFloat(data.confidence);

      // Render Badge Sentimen
      sentimentBadge.textContent = sentiment;
      sentimentBadge.className = "badge " + getSentimentClass(sentiment);

      // Render Progress Bar Keyakinan Model
      confidenceText.textContent = `${confidenceVal}%`;
      progressBar.style.width = `${confidenceVal}%`;
      progressBar.className = "progress-bar-fill " + getBarClass(sentiment);

      // Tampilkan Result Panel
      resultPanel.classList.remove("hidden");

    } catch (error) {
      alert("Gagal terhubung ke API server.");
    } finally {
      // Restore UI State Button
      submitBtn.disabled = false;
      btnText.classList.remove("hidden");
      btnSpinner.classList.add("hidden");
    }
  }

  function getSentimentClass(label) {
    const l = label.toLowerCase();
    if (l.includes("pos")) return "badge-positive";
    if (l.includes("neg")) return "badge-negative";
    return "badge-neutral";
  }

  function getBarClass(label) {
    const l = label.toLowerCase();
    if (l.includes("pos")) return "bg-positive";
    if (l.includes("neg")) return "bg-negative";
    return "bg-neutral";
  }
});
const reviewInput = document.getElementById("reviewInput");
const charCount = document.getElementById("charCount");
const submitBtn = document.getElementById("submitBtn");
const btnText = document.getElementById("btnText");
const btnSpinner = document.getElementById("btnSpinner");
const resultPanel = document.getElementById("resultPanel");
const sentimentBadge = document.getElementById("sentimentBadge");
const confidenceText = document.getElementById("confidenceText");
const progressBar = document.getElementById("progressBar");

reviewInput.addEventListener("input", () => {
  const len = reviewInput.value.length;
  charCount.textContent = len;
});

submitBtn.addEventListener("click", async () => {
  const text = reviewInput.value.trim();

  if (!text) {
    alert("Silakan masukkan teks ulasan terlebih dahulu.");
    reviewInput.focus();
    return;
  }

  submitBtn.disabled = true;
  btnText.classList.add("hidden");
  btnSpinner.classList.remove("hidden");

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text })
    });

    if (!response.ok) {
      throw new Error("Prediksi gagal diproses");
    }

    const result = await response.json();

    const sentiment = result.sentiment.toLowerCase();
    const confidence = Number(result.confidence || 0);

    sentimentBadge.textContent = result.sentiment;
    sentimentBadge.classList.remove("positive", "negative", "neutral");

    if (sentiment === "positif") {
      sentimentBadge.classList.add("positive");
    } else if (sentiment === "negatif") {
      sentimentBadge.classList.add("negative");
    } else {
      sentimentBadge.classList.add("neutral");
    }

    confidenceText.textContent = `${confidence}%`;
    progressBar.style.width = `${confidence}%`;

    resultPanel.classList.remove("hidden");
  } catch (error) {
    alert("Terjadi kesalahan saat menganalisis. Silakan coba lagi.");
    console.error(error);
  } finally {
    submitBtn.disabled = false;
    btnSpinner.classList.add("hidden");
    btnText.classList.remove("hidden");
  }
});
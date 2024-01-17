document.getElementById('image-input').addEventListener('change', function() {
    const reader = new FileReader();
    reader.onload = function() {
        const img = document.getElementById('image-preview');
        img.src = reader.result;
    };
    reader.readAsDataURL(this.files[0]);
});

document.getElementById('caption-btn').addEventListener('click', function() {
    const img = document.getElementById('image-preview');
    if (img.src) {
        fetch('http://localhost:8000/caption', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({image: img.src.split(',')[1]})
        })
        .then(response => response.json())
        .then(data => {
            const captionText = data['caption'][0]['generated_text'] || 'No caption generated';
            console.log(data['caption'][0]['generated_text'])
            document.getElementById('caption-text').textContent = captionText;
            speakCaption(captionText);
        });
    } else {
        alert('Please upload an image first.');
    }
});

function speakCaption(text) {
    const speech = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(speech);
}

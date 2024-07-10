import streamlit as st
import streamlit.components.v1 as components

st.title("麥克風錄音與上傳")

mic_recorder_html = """
<!DOCTYPE html>
<html>
<head>
    <title>麥克風錄音</title>
</head>
<body>
    <button id="recordButton">開始錄音</button>
    <button id="stopButton" disabled>停止錄音</button>
    <audio id="audioPlayback" controls></audio>
    <script>
        let mediaRecorder;
        let audioChunks = [];

        document.getElementById('recordButton').onclick = async () => {
            let stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };
            mediaRecorder.onstop = async () => {
                let audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                let audioUrl = URL.createObjectURL(audioBlob);
                document.getElementById('audioPlayback').src = audioUrl;

                // 上傳錄音文件
                let formData = new FormData();
                formData.append('audio', audioBlob, 'recording.wav');
                await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
            };
            mediaRecorder.start();
            document.getElementById('recordButton').disabled = true;
            document.getElementById('stopButton').disabled = false;
        };

        document.getElementById('stopButton').onclick = () => {
            mediaRecorder.stop();
            document.getElementById('recordButton').disabled = false;
            document.getElementById('stopButton').disabled = true;
        };
    </script>
</body>
</html>
"""

components.html(mic_recorder_html, height=600)

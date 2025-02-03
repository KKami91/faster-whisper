import runpod
import os
from faster_whisper import WhisperModel

def run_whisper(audio_path):
    model = WhisperModel("tiny", device="cuda")
    segments, info = model.transcribe(audio_path, word_timestamps=True)
    
    results = []
    for segment in segments:
        results.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text
        })
    
    return results

def handler(event):
    """
    RunPod Handler Function
    """
    try:
        # 입력 데이터에서 오디오 파일 저장
        input_audio = event["input"]["audio"]
        audio_path = "/tmp/audio.wav"  # 임시 파일로 저장
        
        # 오디오 데이터를 파일로 저장
        with open(audio_path, "wb") as f:
            f.write(input_audio)
        
        # Whisper 실행
        results = run_whisper(audio_path)
        
        # 임시 파일 삭제
        os.remove(audio_path)
        
        return {
            "segments": results
        }
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
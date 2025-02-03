import runpod
import os
import base64
from faster_whisper import WhisperModel

def run_whisper(audio_path):
    # GPU로 모델 로드
    model = WhisperModel("tiny", device="cuda")
    
    # 음성 파일 처리
    segments, info = model.transcribe(audio_path, word_timestamps=True)
    
    # 결과를 리스트로 변환
    results = []
    for segment in segments:
        results.append({
            "start": float(segment.start),
            "end": float(segment.end),
            "text": segment.text
        })
    
    return results

def handler(event):
    """
    RunPod Serverless 핸들러
    """
    try:
        # base64로 인코딩된 오디오 데이터 받기
        audio_base64 = event["input"]["audio"]
        
        # base64 디코딩
        audio_data = base64.b64decode(audio_base64)
        
        # 임시 파일로 저장
        audio_path = "/tmp/audio.wav"
        with open(audio_path, "wb") as f:
            f.write(audio_data)
        
        # Whisper로 처리
        results = run_whisper(audio_path)
        
        # 임시 파일 삭제
        os.remove(audio_path)
        
        # 결과 반환
        return {
            "segments": results
        }
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
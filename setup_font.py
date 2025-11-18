"""
나눔고딕 폰트 다운로드 및 설정 스크립트
"""
import urllib.request
import os

def download_nanum_font():
    """나눔고딕 폰트 다운로드"""
    # 폰트 URL (공개 저장소)
    font_url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"

    # 폰트 디렉토리 생성
    font_dir = os.path.expanduser('~/.fonts')
    os.makedirs(font_dir, exist_ok=True)

    font_path = os.path.join(font_dir, 'NanumGothic.ttf')

    try:
        print(f"나눔고딕 폰트 다운로드 중...")
        urllib.request.urlretrieve(font_url, font_path)

        # 파일 크기 확인
        file_size = os.path.getsize(font_path)

        if file_size > 10000:  # 10KB 이상이면 정상
            print(f"✅ 폰트 다운로드 성공: {font_path}")
            print(f"   파일 크기: {file_size:,} bytes")
            return True
        else:
            print(f"❌ 다운로드된 파일이 너무 작습니다: {file_size} bytes")
            os.remove(font_path)
            return False

    except Exception as e:
        print(f"❌ 폰트 다운로드 실패: {e}")
        if os.path.exists(font_path):
            os.remove(font_path)
        return False

if __name__ == "__main__":
    if download_nanum_font():
        print("\n폰트가 성공적으로 설치되었습니다.")
        print("이제 analyze_data.py를 실행하면 한글이 정상적으로 표시됩니다.")
    else:
        print("\n폰트 다운로드에 실패했습니다.")

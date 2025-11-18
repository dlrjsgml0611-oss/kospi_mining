# KOSPI 투자자별 거래 데이터 분석

코스피 시장의 개인, 외국인, 기관 투자자별 매수/매도 데이터를 수집하고 분석하는 프로젝트입니다.

## 설치

```bash
pip install -r requirements.txt
```

## 사용법

### 1. 한글 폰트 설치 (처음 한 번만)
차트에서 한글이 깨지지 않도록 나눔고딕 폰트를 설치합니다:
```bash
python setup_font.py
```

### 2. 샘플 데이터 생성
실제 API 접근이 제한된 환경에서는 샘플 데이터를 생성합니다:
```bash
python generate_sample_data.py
```

### 3. 실제 데이터 수집 (선택사항)
KRX API 접근 가능한 경우:
```bash
python collect_data.py
```

### 4. 데이터 분석 (정적 차트)
```bash
python analyze_data.py
```

### 5. 웹 대시보드 생성 (추천! 🌟)
인터랙티브한 웹 대시보드를 생성합니다:
```bash
python create_web_dashboard.py
```
그 후 브라우저에서 `results/dashboard.html` 파일을 열어보세요!

## 분석 결과

### 정적 분석 결과 (analyze_data.py)
`results/` 디렉토리에 다음 파일들이 생성됩니다:

- `investor_trends.png`: **모든 투자자**(7개) 일별 순매수 추이 (한 차트에 통합)
- `cumulative_trends.png`: **모든 투자자**(7개) 누적 순매수 추이 (한 차트에 통합)
- `investor_trends_detailed.png`: 각 투자자별 상세 일별 순매수 추이 (서브플롯)
- `correlation_heatmap.png`: 투자자별 거래와 코스피 지수 상관관계
- `analysis_report.md`: 분석 리포트

**포함된 투자자**: 개인, 외국인, 기관, 금융투자, 보험, 투신, 은행 (총 7개)

### 인터랙티브 대시보드 (create_web_dashboard.py)
`results/dashboard.html` 파일이 생성됩니다:
- 📈 투자자별 일별 순매수 추이 (확대/축소 가능)
- 📊 누적 순매수 추이 (호버로 상세 정보 확인)
- 📉 코스피 지수 캔들스틱 차트
- 🔥 투자자별 총 순매수 비교 차트
- 🎯 상관관계 히트맵
- 💡 주요 통계 카드

## 주요 분석 내용

- **전체 기간 총 순매수액**: 투자자별 1년간 총 순매수 금액
- **투자자별 거래 통계**: 평균, 표준편차, 최소/최대값 등
- **코스피 지수 상관관계**: 각 투자자 그룹의 순매수와 코스피 수익률의 상관계수
- **주요 발견사항**: 최대 순매수일/순매도일 및 금액

## 데이터 소스
- pykrx: 한국거래소(KRX) 공식 데이터
- 샘플 데이터: 실제 시장 패턴을 모방한 시뮬레이션 데이터

## 프로젝트 구조

```
kospi_mining/
├── setup_font.py              # 한글 폰트 설치 스크립트
├── collect_data.py            # 실제 데이터 수집 (KRX API)
├── generate_sample_data.py    # 샘플 데이터 생성
├── analyze_data.py            # 정적 차트 생성 (matplotlib/seaborn)
├── create_web_dashboard.py    # 인터랙티브 웹 대시보드 생성 (Plotly)
├── requirements.txt           # 필요한 패키지
├── data/                      # 수집된 데이터
│   ├── kospi_investor_trading.csv
│   └── kospi_index.csv
└── results/                   # 분석 결과
    ├── dashboard.html              # 웹 대시보드 (추천!)
    ├── investor_trends.png         # 7개 투자자 일별 순매수 (통합)
    ├── cumulative_trends.png       # 7개 투자자 누적 순매수 (통합)
    ├── investor_trends_detailed.png # 각 투자자별 상세 차트
    ├── correlation_heatmap.png     # 상관관계 히트맵
    └── analysis_report.md          # 분석 리포트
```

## 분석 예시

샘플 데이터 기준 주요 발견사항:
- 개인 투자자는 1년간 약 -6,902억원 순매도
- 외국인 투자자는 약 -2,714억원 순매도
- 기관 투자자(금융투자, 보험, 투신, 은행 포함)는 총 약 65,847억원 순매수
- 은행의 순매수와 코스피 수익률의 상관계수가 -0.0950으로 가장 낮음

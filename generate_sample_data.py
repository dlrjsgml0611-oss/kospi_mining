"""
실제 API 접근이 불가능한 경우를 위한 샘플 데이터 생성 스크립트
실제 코스피 투자자별 거래 패턴을 시뮬레이션합니다.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_sample_investor_data(start_date, end_date, output_dir="data"):
    """
    투자자별 순매수 샘플 데이터를 생성합니다.
    실제 한국 시장 패턴을 반영한 시뮬레이션 데이터입니다.
    """
    os.makedirs(output_dir, exist_ok=True)

    # 날짜 범위 생성 (평일만)
    dates = pd.date_range(start=start_date, end=end_date, freq='B')  # B = Business day

    print(f"샘플 데이터 생성: {start_date} ~ {end_date}")
    print(f"총 거래일: {len(dates)} 일\n")

    # 실제 투자자별 거래 패턴을 시뮬레이션
    # 실제 코스피 일일 순매수는 보통 -3000억 ~ +3000억 범위
    np.random.seed(42)

    # 기관투자자: 안정적이고 변동성이 적음 (평균 0, 표준편차 500억)
    institution = np.random.normal(0, 500, len(dates)) * 100000000  # 단위: 원

    # 외국인: 큰 금액으로 움직이고 트렌드가 있음 (평균 -300~+300억, 표준편차 800억)
    trend = np.linspace(-300, 300, len(dates))  # 점진적 트렌드
    foreigner = np.random.normal(trend, 800, len(dates)) * 100000000

    # 개인: 외국인과 반대 패턴 (외국인이 사면 개인이 팔고, 외국인이 팔면 개인이 사는 경향)
    # 개인 = -(외국인 + 기관) + 노이즈
    individual = -(foreigner + institution) + np.random.normal(0, 200, len(dates)) * 100000000

    # 데이터프레임 생성
    df = pd.DataFrame({
        '개인': individual,
        '외국인': foreigner,
        '기관': institution,
        '금융투자': institution * 0.6 + np.random.normal(0, 300, len(dates)) * 100000000,
        '보험': institution * 0.2 + np.random.normal(0, 150, len(dates)) * 100000000,
        '투신': institution * 0.15 + np.random.normal(0, 150, len(dates)) * 100000000,
        '은행': institution * 0.05 + np.random.normal(0, 80, len(dates)) * 100000000,
    }, index=dates)

    # 데이터 저장
    output_file = os.path.join(output_dir, "kospi_investor_trading.csv")
    df.to_csv(output_file, encoding='utf-8-sig')
    print(f"투자자별 거래 데이터 저장: {output_file}")

    return df

def generate_sample_kospi_index(start_date, end_date, output_dir="data"):
    """
    코스피 지수 샘플 데이터를 생성합니다.
    """
    dates = pd.date_range(start=start_date, end=end_date, freq='B')

    # 초기 가격
    initial_price = 2500
    prices = [initial_price]

    # 랜덤 워크로 주가 생성
    np.random.seed(42)
    for i in range(1, len(dates)):
        # 일일 수익률: 평균 0.05%, 표준편차 1%
        daily_return = np.random.normal(0.0005, 0.01)
        new_price = prices[-1] * (1 + daily_return)
        prices.append(new_price)

    # OHLCV 데이터 생성
    df = pd.DataFrame({
        '시가': [p * (1 + np.random.normal(0, 0.005)) for p in prices],
        '고가': [p * (1 + abs(np.random.normal(0.01, 0.005))) for p in prices],
        '저가': [p * (1 - abs(np.random.normal(0.01, 0.005))) for p in prices],
        '종가': prices,
        '거래량': np.random.randint(300000, 800000, len(dates)),
    }, index=dates)

    # 고가는 시가/종가보다 높아야 함
    df['고가'] = df[['시가', '고가', '종가']].max(axis=1)
    # 저가는 시가/종가보다 낮아야 함
    df['저가'] = df[['시가', '저가', '종가']].min(axis=1)

    # 데이터 저장
    output_file = os.path.join(output_dir, "kospi_index.csv")
    df.to_csv(output_file, encoding='utf-8-sig')
    print(f"코스피 지수 데이터 저장: {output_file}\n")

    return df

def main():
    print("=== 코스피 투자자별 거래 샘플 데이터 생성 ===\n")
    print("주의: 이 데이터는 실제 API 접근이 불가능한 경우를 위한 시뮬레이션 데이터입니다.")
    print("실제 코스피 투자자별 거래 패턴을 모방하여 생성되었습니다.\n")

    # 1년간 데이터 생성
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    # 데이터 생성
    df_investor = generate_sample_investor_data(start_date, end_date)
    df_index = generate_sample_kospi_index(start_date, end_date)

    # 요약 출력
    print("=== 생성된 데이터 요약 ===")
    print(f"\n투자자별 거래 데이터:")
    print(df_investor.head())
    print(f"\n기본 통계:")
    print(df_investor.describe())

    print(f"\n\n코스피 지수 데이터:")
    print(df_index.head())
    print(f"\n기간: {df_index.index[0].strftime('%Y-%m-%d')} ~ {df_index.index[-1].strftime('%Y-%m-%d')}")
    print(f"시작 지수: {df_index.iloc[0]['종가']:.2f}")
    print(f"종료 지수: {df_index.iloc[-1]['종가']:.2f}")
    print(f"수익률: {((df_index.iloc[-1]['종가'] / df_index.iloc[0]['종가']) - 1) * 100:.2f}%")

if __name__ == "__main__":
    main()

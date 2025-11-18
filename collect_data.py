"""
코스피 투자자별 거래 데이터 수집 스크립트
"""
import pandas as pd
from pykrx import stock
from datetime import datetime, timedelta
import os

def collect_investor_trading_data(start_date, end_date, output_dir="data"):
    """
    투자자별 순매수 데이터를 수집합니다.

    Args:
        start_date: 시작일 (YYYYMMDD)
        end_date: 종료일 (YYYYMMDD)
        output_dir: 데이터 저장 디렉토리
    """
    # 데이터 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)

    print(f"데이터 수집 시작: {start_date} ~ {end_date}")

    # 코스피 투자자별 거래 데이터 수집
    try:
        # 일별 투자자별 순매수 데이터 수집
        df = stock.get_market_net_purchases_of_equities(
            start_date,
            end_date,
            "KOSPI"
        )

        print(f"수집된 데이터: {len(df)} 행")
        print(df.head())

        # 데이터 저장
        output_file = os.path.join(output_dir, "kospi_investor_trading.csv")
        df.to_csv(output_file, encoding='utf-8-sig')
        print(f"\n데이터 저장 완료: {output_file}")

        # 코스피 지수 데이터도 함께 수집
        try:
            kospi_index = stock.get_index_ohlcv(start_date, end_date, "1001")  # 1001: 코스피
            kospi_file = os.path.join(output_dir, "kospi_index.csv")
            kospi_index.to_csv(kospi_file, encoding='utf-8-sig')
            print(f"코스피 지수 데이터 저장: {kospi_file}")
        except Exception as e:
            print(f"코스피 지수 데이터 수집 실패: {e}")
            # 대체 방법: 코스피 티커로 시도
            try:
                kospi_index = stock.get_index_ohlcv(start_date, end_date, "KOSPI")
                kospi_file = os.path.join(output_dir, "kospi_index.csv")
                kospi_index.to_csv(kospi_file, encoding='utf-8-sig')
                print(f"코스피 지수 데이터 저장 (대체 방법): {kospi_file}")
            except Exception as e2:
                print(f"코스피 지수 데이터 수집 실패 (대체 방법): {e2}")
                kospi_index = None

        return df, kospi_index

    except Exception as e:
        print(f"데이터 수집 중 오류 발생: {e}")
        return None, None

def main():
    # 최근 1년간 데이터 수집
    # 종료일은 오늘 기준 최근 평일로 설정 (여유있게 3일 전)
    end_date = datetime.now() - timedelta(days=3)
    start_date = end_date - timedelta(days=365)

    start_str = start_date.strftime("%Y%m%d")
    end_str = end_date.strftime("%Y%m%d")

    print(f"=== 코스피 투자자별 거래 데이터 수집 ===")
    print(f"기간: {start_str} ~ {end_str}\n")

    df, kospi_index = collect_investor_trading_data(start_str, end_str)

    if df is not None:
        print("\n=== 데이터 요약 ===")
        print(f"총 거래일: {len(df)} 일")
        print(f"\n컬럼: {list(df.columns)}")
        print(f"\n기본 통계:")
        print(df.describe())

if __name__ == "__main__":
    main()

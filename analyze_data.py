"""
코스피 투자자별 거래 데이터 분석 스크립트
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
from datetime import datetime
import os

# 나눔고딕 폰트 설정
font_path = os.path.expanduser('~/.fonts/NanumGothic.ttf')

if os.path.exists(font_path):
    try:
        # 폰트 파일 직접 등록
        fm.fontManager.addfont(font_path)
        # 폰트 속성 가져오기
        font_entry = fm.FontEntry(fname=font_path, name='NanumGothic')
        fm.fontManager.ttflist.append(font_entry)

        # matplotlib에 폰트 설정
        plt.rcParams['font.family'] = 'NanumGothic'
        plt.rcParams['axes.unicode_minus'] = False
        print(f"✅ 나눔고딕 폰트 적용 완료")
    except Exception as e:
        print(f"❌ 폰트 로드 실패: {e}")
        # 폴백: 기본 폰트 사용
        plt.rcParams['font.family'] = 'DejaVu Sans'
        plt.rcParams['axes.unicode_minus'] = False
        print("⚠️  기본 폰트 사용 (한글 깨질 수 있음)")
else:
    # 폰트 파일이 없는 경우
    print("⚠️  나눔고딕 폰트를 찾을 수 없습니다.")
    print("   'python setup_font.py'를 먼저 실행하세요.")
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['axes.unicode_minus'] = False

def load_data(data_dir="data"):
    """데이터 로드"""
    investor_file = os.path.join(data_dir, "kospi_investor_trading.csv")
    index_file = os.path.join(data_dir, "kospi_index.csv")

    df_investor = pd.read_csv(investor_file, index_col=0, encoding='utf-8-sig')
    df_index = pd.read_csv(index_file, index_col=0, encoding='utf-8-sig')

    # 인덱스를 datetime으로 변환
    df_investor.index = pd.to_datetime(df_investor.index)
    df_index.index = pd.to_datetime(df_index.index)

    return df_investor, df_index

def analyze_investor_trends(df):
    """투자자별 거래 추이 분석"""
    print("=== 투자자별 순매수 통계 ===\n")

    # 컬럼명 출력
    print(f"데이터 컬럼: {list(df.columns)}\n")

    # 기본 통계
    print(df.describe())

    # 총 순매수액 계산
    print("\n=== 전체 기간 총 순매수액 (단위: 억원) ===")
    total_net_purchase = df.sum() / 100000000  # 원 -> 억원
    print(total_net_purchase.sort_values(ascending=False))

    return total_net_purchase

def plot_investor_trends(df, output_dir="results"):
    """투자자별 거래 추이 시각화"""
    os.makedirs(output_dir, exist_ok=True)

    # 억원 단위로 변환
    df_billions = df / 100000000

    # 1. 모든 투자자별 일별 순매수 추이 (하나의 차트에)
    fig, ax = plt.subplots(figsize=(16, 8))

    # 색상 팔레트
    colors = ['#E74C3C', '#3498DB', '#2ECC71', '#9B59B6', '#F39C12', '#1ABC9C', '#34495E']

    for idx, col in enumerate(df.columns):
        ax.plot(df_billions.index, df_billions[col],
                label=col, linewidth=2, color=colors[idx % len(colors)])

    ax.axhline(y=0, color='red', linestyle='--', alpha=0.3, linewidth=1)
    ax.set_title('투자자별 일별 순매수 추이 (Daily Net Purchase by Investor)', fontsize=16, pad=15, fontweight='bold')
    ax.set_xlabel('날짜 (Date)', fontsize=12)
    ax.set_ylabel('순매수 (100M KRW)', fontsize=12)
    ax.legend(loc='best', fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle='--')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'investor_trends.png'), dpi=300, bbox_inches='tight')
    print(f"\n저장됨: {output_dir}/investor_trends.png")
    plt.close()

    # 2. 모든 투자자별 누적 순매수 추이
    fig, ax = plt.subplots(figsize=(16, 8))

    for idx, col in enumerate(df.columns):
        cumulative = df_billions[col].cumsum()
        ax.plot(cumulative.index, cumulative.values,
                label=col, linewidth=2.5, color=colors[idx % len(colors)])

    ax.axhline(y=0, color='black', linestyle='--', alpha=0.5, linewidth=1)
    ax.set_title('투자자별 누적 순매수 추이 (Cumulative Net Purchase by Investor)',
                 fontsize=16, pad=15, fontweight='bold')
    ax.set_xlabel('날짜 (Date)', fontsize=12)
    ax.set_ylabel('누적 순매수 (100M KRW)', fontsize=12)
    ax.legend(loc='best', fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle='--')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'cumulative_trends.png'), dpi=300, bbox_inches='tight')
    print(f"저장됨: {output_dir}/cumulative_trends.png")
    plt.close()

    # 3. 투자자별 상세 비교 (서브플롯)
    n_investors = len(df.columns)
    fig, axes = plt.subplots(n_investors, 1, figsize=(16, 3*n_investors))

    if n_investors == 1:
        axes = [axes]

    for idx, col in enumerate(df.columns):
        axes[idx].plot(df_billions.index, df_billions[col],
                      linewidth=1.5, color=colors[idx % len(colors)])
        axes[idx].axhline(y=0, color='red', linestyle='--', alpha=0.3)
        axes[idx].set_title(f'{col} 순매수 추이', fontsize=12, pad=10, fontweight='bold')
        axes[idx].set_ylabel('순매수 (억원)', fontsize=10)
        axes[idx].grid(True, alpha=0.3)

    axes[-1].set_xlabel('날짜 (Date)', fontsize=12)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'investor_trends_detailed.png'), dpi=300, bbox_inches='tight')
    print(f"저장됨: {output_dir}/investor_trends_detailed.png")
    plt.close()

def analyze_correlation(df_investor, df_index, output_dir="results"):
    """투자자별 거래와 코스피 지수 상관관계 분석"""
    os.makedirs(output_dir, exist_ok=True)

    # 데이터 병합
    merged = df_investor.join(df_index[['종가']], how='inner')
    merged.columns = list(df_investor.columns) + ['KOSPI_Close']

    # 코스피 수익률 계산
    merged['KOSPI_Return'] = merged['KOSPI_Close'].pct_change() * 100

    # 상관관계 계산
    print("\n=== 투자자 순매수와 코스피 수익률 상관관계 ===")
    correlations = {}
    for col in df_investor.columns:
        corr = merged[col].corr(merged['KOSPI_Return'])
        correlations[col] = corr
        print(f"{col}: {corr:.4f}")

    # 상관관계 히트맵
    corr_matrix = merged.corr()

    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm',
                center=0, square=True, ax=ax, cbar_kws={'label': 'Correlation'})
    ax.set_title('Correlation Matrix: Investor Trading vs KOSPI', fontsize=14, pad=15)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'correlation_heatmap.png'), dpi=300, bbox_inches='tight')
    print(f"\n저장됨: {output_dir}/correlation_heatmap.png")
    plt.close()

    return correlations

def generate_report(df_investor, df_index, total_net_purchase, correlations, output_dir="results"):
    """분석 리포트 생성"""
    os.makedirs(output_dir, exist_ok=True)

    report = []
    report.append("# 코스피 투자자별 거래 데이터 분석 리포트\n")
    report.append(f"분석일: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append(f"분석 기간: {df_investor.index[0].strftime('%Y-%m-%d')} ~ {df_investor.index[-1].strftime('%Y-%m-%d')}\n")
    report.append(f"총 거래일: {len(df_investor)} 일\n\n")

    report.append("## 1. 전체 기간 총 순매수액 (단위: 억원)\n\n")
    for col, value in total_net_purchase.sort_values(ascending=False).items():
        report.append(f"- {col}: {value:,.0f} 억원\n")

    report.append("\n## 2. 투자자별 거래 통계\n\n")
    stats = df_investor.describe()
    report.append(stats.to_markdown())
    report.append("\n")

    report.append("\n## 3. 코스피 지수 상관관계\n\n")
    for col, corr in correlations.items():
        report.append(f"- {col}: {corr:.4f}\n")

    report.append("\n## 4. 주요 발견사항\n\n")

    # 최대 순매수일/순매도일 찾기
    for col in df_investor.columns[:3]:  # 주요 3개 투자자
        max_buy_date = df_investor[col].idxmax()
        max_buy_value = df_investor[col].max() / 100000000
        max_sell_date = df_investor[col].idxmin()
        max_sell_value = df_investor[col].min() / 100000000

        report.append(f"\n### {col}\n")
        report.append(f"- 최대 순매수일: {max_buy_date.strftime('%Y-%m-%d')} ({max_buy_value:,.0f} 억원)\n")
        report.append(f"- 최대 순매도일: {max_sell_date.strftime('%Y-%m-%d')} ({max_sell_value:,.0f} 억원)\n")

    # 리포트 저장
    report_file = os.path.join(output_dir, 'analysis_report.md')
    with open(report_file, 'w', encoding='utf-8') as f:
        f.writelines(report)

    print(f"\n\n=== 분석 리포트 생성 완료 ===")
    print(f"저장 위치: {report_file}\n")

    # 콘솔에도 출력
    print(''.join(report))

def main():
    print("=== 코스피 투자자별 거래 데이터 분석 시작 ===\n")

    # 데이터 로드
    try:
        df_investor, df_index = load_data()
        print(f"데이터 로드 완료: {len(df_investor)} 거래일\n")
    except FileNotFoundError:
        print("데이터 파일을 찾을 수 없습니다.")
        print("먼저 'python collect_data.py'를 실행하여 데이터를 수집하세요.")
        return

    # 분석 실행
    total_net_purchase = analyze_investor_trends(df_investor)
    plot_investor_trends(df_investor)
    correlations = analyze_correlation(df_investor, df_index)
    generate_report(df_investor, df_index, total_net_purchase, correlations)

    print("\n=== 분석 완료 ===")
    print("결과 파일:")
    print("- results/investor_trends.png")
    print("- results/cumulative_trends.png")
    print("- results/correlation_heatmap.png")
    print("- results/analysis_report.md")

if __name__ == "__main__":
    main()

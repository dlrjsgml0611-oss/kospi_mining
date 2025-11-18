"""
코스피 투자자별 거래 데이터 웹 대시보드 생성 스크립트
Plotly를 사용한 인터랙티브 시각화
"""
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime

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

def create_investor_trends_chart(df):
    """투자자별 순매수 추이 차트 (인터랙티브)"""
    # 억원 단위로 변환
    df_billions = df / 100000000

    # 개인, 외국인, 기관만 표시
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=('Individual Investor Net Purchase',
                       'Foreign Investor Net Purchase',
                       'Institutional Investor Net Purchase'),
        vertical_spacing=0.1
    )

    # 개인
    fig.add_trace(
        go.Scatter(x=df_billions.index, y=df_billions['개인'],
                  name='Individual', line=dict(color='#E74C3C', width=2),
                  hovertemplate='%{x|%Y-%m-%d}<br>%{y:,.0f} 100M KRW<extra></extra>'),
        row=1, col=1
    )

    # 외국인
    fig.add_trace(
        go.Scatter(x=df_billions.index, y=df_billions['외국인'],
                  name='Foreigner', line=dict(color='#3498DB', width=2),
                  hovertemplate='%{x|%Y-%m-%d}<br>%{y:,.0f} 100M KRW<extra></extra>'),
        row=2, col=1
    )

    # 기관
    fig.add_trace(
        go.Scatter(x=df_billions.index, y=df_billions['기관'],
                  name='Institution', line=dict(color='#2ECC71', width=2),
                  hovertemplate='%{x|%Y-%m-%d}<br>%{y:,.0f} 100M KRW<extra></extra>'),
        row=3, col=1
    )

    # 0 기준선 추가
    for i in range(1, 4):
        fig.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.5, row=i, col=1)

    fig.update_xaxes(title_text="Date", row=3, col=1)
    fig.update_yaxes(title_text="Net Purchase (100M KRW)", row=1, col=1)
    fig.update_yaxes(title_text="Net Purchase (100M KRW)", row=2, col=1)
    fig.update_yaxes(title_text="Net Purchase (100M KRW)", row=3, col=1)

    fig.update_layout(
        height=900,
        showlegend=False,
        title_text="KOSPI Investor Net Purchase Trends (Daily)",
        title_x=0.5,
        hovermode='x unified'
    )

    return fig

def create_cumulative_chart(df):
    """누적 순매수 추이 차트"""
    df_billions = df / 100000000

    fig = go.Figure()

    colors = {
        '개인': '#E74C3C',
        '외국인': '#3498DB',
        '기관': '#2ECC71',
        '금융투자': '#9B59B6',
        '보험': '#F39C12',
        '투신': '#1ABC9C',
        '은행': '#34495E'
    }

    for col in df_billions.columns:
        cumulative = df_billions[col].cumsum()
        fig.add_trace(
            go.Scatter(
                x=df_billions.index,
                y=cumulative,
                name=col,
                line=dict(width=2.5, color=colors.get(col, '#95A5A6')),
                hovertemplate='%{x|%Y-%m-%d}<br>%{y:,.0f} 100M KRW<extra></extra>'
            )
        )

    fig.add_hline(y=0, line_dash="dash", line_color="black", opacity=0.5)

    fig.update_layout(
        title="Cumulative Net Purchase by Investor Type",
        title_x=0.5,
        xaxis_title="Date",
        yaxis_title="Cumulative Net Purchase (100M KRW)",
        height=600,
        hovermode='x unified',
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.01
        )
    )

    return fig

def create_correlation_heatmap(df_investor, df_index):
    """상관관계 히트맵"""
    # 데이터 병합
    merged = df_investor.join(df_index[['종가']], how='inner')
    merged.columns = list(df_investor.columns) + ['KOSPI_Close']

    # 코스피 수익률 계산
    merged['KOSPI_Return'] = merged['KOSPI_Close'].pct_change() * 100

    # 상관관계 계산
    corr_matrix = merged.corr()

    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=corr_matrix.values,
        texttemplate='%{text:.3f}',
        textfont={"size": 10},
        colorbar=dict(title="Correlation")
    ))

    fig.update_layout(
        title="Correlation Matrix: Investor Trading vs KOSPI",
        title_x=0.5,
        height=700,
        width=800
    )

    return fig

def create_kospi_index_chart(df_index):
    """코스피 지수 차트"""
    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(
            x=df_index.index,
            open=df_index['시가'],
            high=df_index['고가'],
            low=df_index['저가'],
            close=df_index['종가'],
            name='KOSPI'
        )
    )

    fig.update_layout(
        title="KOSPI Index (OHLC)",
        title_x=0.5,
        xaxis_title="Date",
        yaxis_title="Index",
        height=500,
        xaxis_rangeslider_visible=False
    )

    return fig

def create_investor_comparison_chart(df):
    """투자자별 비교 차트 (막대 그래프)"""
    total_net_purchase = (df.sum() / 100000000).sort_values(ascending=True)

    colors = ['#E74C3C' if x < 0 else '#2ECC71' for x in total_net_purchase.values]

    fig = go.Figure(
        go.Bar(
            x=total_net_purchase.values,
            y=total_net_purchase.index,
            orientation='h',
            marker=dict(color=colors),
            text=total_net_purchase.values,
            texttemplate='%{text:,.0f}',
            textposition='outside',
            hovertemplate='%{y}<br>%{x:,.0f} 100M KRW<extra></extra>'
        )
    )

    fig.add_vline(x=0, line_dash="dash", line_color="black", opacity=0.5)

    fig.update_layout(
        title="Total Net Purchase by Investor Type (1 Year)",
        title_x=0.5,
        xaxis_title="Total Net Purchase (100M KRW)",
        yaxis_title="Investor Type",
        height=500
    )

    return fig

def create_html_dashboard(df_investor, df_index, output_file="dashboard.html"):
    """HTML 대시보드 생성"""

    print("차트 생성 중...")

    # 각 차트 생성
    fig1 = create_investor_trends_chart(df_investor)
    fig2 = create_cumulative_chart(df_investor)
    fig3 = create_correlation_heatmap(df_investor, df_index)
    fig4 = create_kospi_index_chart(df_index)
    fig5 = create_investor_comparison_chart(df_investor)

    # HTML 생성
    html_content = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KOSPI Investor Trading Analysis Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f6fa;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        h1 {{
            margin: 0;
            font-size: 2.5em;
        }}
        .subtitle {{
            margin-top: 10px;
            opacity: 0.9;
            font-size: 1.1em;
        }}
        .stats-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            margin: 10px 0;
        }}
        .stat-value.positive {{ color: #2ECC71; }}
        .stat-value.negative {{ color: #E74C3C; }}
        .stat-label {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .footer {{
            text-align: center;
            color: #7f8c8d;
            margin-top: 50px;
            padding: 20px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 KOSPI Investor Trading Analysis Dashboard</h1>
        <div class="subtitle">Last 1 Year Trading Data Analysis</div>
        <div class="subtitle">Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
    </div>

    <div class="stats-container">
        <div class="stat-card">
            <div class="stat-label">Individual</div>
            <div class="stat-value negative">{(df_investor['개인'].sum() / 100000000):,.0f}</div>
            <div class="stat-label">100M KRW</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Foreigner</div>
            <div class="stat-value negative">{(df_investor['외국인'].sum() / 100000000):,.0f}</div>
            <div class="stat-label">100M KRW</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Institution</div>
            <div class="stat-value positive">{(df_investor['기관'].sum() / 100000000):,.0f}</div>
            <div class="stat-label">100M KRW</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Financial Investment</div>
            <div class="stat-value positive">{(df_investor['금융투자'].sum() / 100000000):,.0f}</div>
            <div class="stat-label">100M KRW</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Trading Days</div>
            <div class="stat-value">{len(df_investor)}</div>
            <div class="stat-label">Days</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">KOSPI Return</div>
            <div class="stat-value positive">{((df_index.iloc[-1]['종가'] / df_index.iloc[0]['종가'] - 1) * 100):.2f}%</div>
            <div class="stat-label">1 Year</div>
        </div>
    </div>

    <div class="chart-container">
        <div id="chart1"></div>
    </div>

    <div class="chart-container">
        <div id="chart2"></div>
    </div>

    <div class="chart-container">
        <div id="chart5"></div>
    </div>

    <div class="chart-container">
        <div id="chart4"></div>
    </div>

    <div class="chart-container">
        <div id="chart3"></div>
    </div>

    <div class="footer">
        <p>KOSPI Investor Trading Data Analysis | Data Source: KRX (Korea Exchange)</p>
        <p>Generated by Python with Plotly</p>
    </div>

    <script>
        {fig1.to_html(full_html=False, include_plotlyjs=False, div_id="chart1")}
        {fig2.to_html(full_html=False, include_plotlyjs=False, div_id="chart2")}
        {fig3.to_html(full_html=False, include_plotlyjs=False, div_id="chart3")}
        {fig4.to_html(full_html=False, include_plotlyjs=False, div_id="chart4")}
        {fig5.to_html(full_html=False, include_plotlyjs=False, div_id="chart5")}
    </script>
</body>
</html>
"""

    # HTML 파일 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"\n✅ 대시보드 생성 완료: {output_file}")
    print(f"   브라우저에서 이 파일을 열어보세요!")

def main():
    print("=== KOSPI 투자자별 거래 웹 대시보드 생성 ===\n")

    # 데이터 로드
    try:
        df_investor, df_index = load_data()
        print(f"데이터 로드 완료: {len(df_investor)} 거래일\n")
    except FileNotFoundError:
        print("데이터 파일을 찾을 수 없습니다.")
        print("먼저 'python generate_sample_data.py'를 실행하여 데이터를 생성하세요.")
        return

    # HTML 대시보드 생성
    create_html_dashboard(df_investor, df_index, "results/dashboard.html")

    print("\n=== 완료 ===")
    print("웹 브라우저에서 results/dashboard.html 파일을 열어보세요!")

if __name__ == "__main__":
    main()

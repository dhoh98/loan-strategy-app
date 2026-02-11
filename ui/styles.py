# ui/styles.py

def load_css():
    return """
    <style>
        /* KPI 카드 */
        .kpi-card {
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            padding: 25px;
            border-radius: 15px;
            text-align: center; /* 가운데 정렬 */
            color: white;
            font-size: 22px; /* 글자 크기 조금 더 크게 */
            font-weight: bold;
            margin: 10px auto; /* 카드 간격 중앙 */
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        /* 전체 앱 기본 글자 */
        body, .css-1d391kg {
            font-family: 'Nanum Gothic', sans-serif;
        }

        /* 서브 제목 크기 조정 */
        h2 {
            font-size: 22px !important;
        }

        /* 레이더 차트와 라인 차트 크기 조정 */
        .stPlotlyChart, .element-container {
            max-width: 90%;
            margin: auto;
        }
    </style>
    """

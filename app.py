import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI 지역분석시스템 기획서",
    page_icon="📊",
    layout="wide",
)

# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
    .main {
        background-color: #f7f9fc;
    }
    .hero {
        background: linear-gradient(135deg, #0f2d52 0%, #1a56a0 100%);
        padding: 2.2rem 2rem;
        border-radius: 18px;
        color: white;
        margin-bottom: 1.2rem;
    }
    .hero-badge {
        display: inline-block;
        padding: 0.3rem 0.7rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.12);
        font-size: 0.8rem;
        margin-bottom: 0.8rem;
    }
    .card {
        background: white;
        border: 1px solid #dde5f0;
        border-radius: 16px;
        padding: 1.1rem 1rem;
        height: 100%;
    }
    .metric-card {
        border-radius: 16px;
        padding: 1rem;
        border: 1px solid #dde5f0;
        background: #ffffff;
    }
    .metric-red {
        background: #fdecea;
        border-color: #f5c6c6;
    }
    .metric-blue {
        background: #e8f2fd;
        border-color: #c3ddf7;
    }
    .metric-green {
        background: #e6f4ec;
        border-color: #b7dfc8;
    }
    .small-label {
        font-size: 0.8rem;
        color: #64748b;
        font-weight: 600;
        margin-bottom: 0.25rem;
    }
    .big-number {
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
    }
    .section-title {
        font-size: 1.6rem;
        font-weight: 800;
        color: #0f2d52;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .highlight {
        background: #e8f2fd;
        border-left: 5px solid #2e7dd4;
        padding: 0.8rem 1rem;
        border-radius: 0 10px 10px 0;
        color: #1a56a0;
        margin: 1rem 0;
    }
    .tag {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 999px;
        font-size: 0.8rem;
        margin-right: 0.35rem;
        margin-bottom: 0.35rem;
        font-weight: 600;
    }
    .tag-blue { background: #e8f2fd; color: #1a56a0; }
    .tag-green { background: #e6f4ec; color: #1b6e3a; }
    .tag-amber { background: #fff4e0; color: #7c4a00; }
    .tag-red { background: #fdecea; color: #9b1c1c; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Data
# -----------------------------
DB = {
    "인천": {
        "pop": "299만",
        "grdp": "89.2조",
        "retail": 112.4,
        "spend": "198만원",
        "popT": "+0.8%",
        "retailT": "+2.1%",
        "tags": [
            ("크루즈 관광객", "blue"),
            ("인천공항 면세", "blue"),
            ("송도 팝업", "green"),
            ("외국인 소비↑", "amber"),
            ("청라 개발호재", "amber"),
        ],
        "food": ["송도 오마카세 급부상", "차이나타운 재방문↑", "부평 로컬카페 확산", "연수구 브런치 맛집↑"],
        "trend": ["인천 크루즈 일정", "송도 신규 맛집", "인천 팝업스토어"],
        "districts": {
            "연수구": {
                "pop": "36.2만",
                "popT": "+1.4%",
                "retail": 118.0,
                "spend": "212만원",
                "retailT": "+2.8%",
                "grdp": "18.4%",
                "tags": [
                    ("송도 팝업", "blue"),
                    ("국제도시 개발", "green"),
                    ("글로벌캠퍼스", "blue"),
                    ("고급주거 수요", "amber"),
                ],
                "food": ["오마카세 급부상", "센트럴파크 카페↑", "글로벌 브런치", "CGV 주변 맛집"],
                "trend": ["송도동 맛집", "연수구 아파트", "국제병원"],
                "dongs": {
                    "송도1동": {
                        "pop": "2.8만",
                        "popT": "+2.3%",
                        "spend": "241만원",
                        "retail": 124.8,
                        "foreign": "6.4%",
                        "avgAge": "36.2세",
                        "age": {
                            "10대이하": 18,
                            "20대": 14,
                            "30대": 34,
                            "40대": 22,
                            "50대+": 12,
                        },
                        "tags": [
                            ("국제업무지구", "blue"),
                            ("외국인 거주↑", "blue"),
                            ("오마카세 급부상", "green"),
                            ("센트럴파크 인근", "green"),
                            ("프리미엄 소비", "amber"),
                        ],
                        "trend": ["송도1동 오마카세", "센트럴파크 카페", "송도 파인다이닝", "송도 외국인 맛집", "루프탑 레스토랑"],
                        "food": ["오마카세·일식 파인다이닝", "스페셜티 커피 카페", "글로벌 브런치 레스토랑", "와인바·비스트로", "프리미엄 베이커리"],
                        "insights": [
                            "프리미엄 F&B 수요 급증: 외국인 거주자 증가와 국제업무지구 직장인 유입으로 오마카세·파인다이닝 검색이 급등.",
                            "30대 핵심 소비층 집중: 평균 연령 36.2세, 30대 비중 34%로 트렌디한 라이프스타일 MD에 적합.",
                            "센트럴파크 집객 효과 활용: 주말 10~14시 유동인구 집중 구간 팝업 이벤트 연계에 유리.",
                            "가성비 MD보다 프리미엄 적합: 20대 비중이 낮아 품질·경험 중심 포지셔닝이 효과적.",
                        ],
                    },
                    "송도2동": {
                        "pop": "2.6만",
                        "popT": "+1.9%",
                        "spend": "228만원",
                        "retail": 121.3,
                        "foreign": "4.8%",
                        "avgAge": "37.8세",
                        "age": {
                            "10대이하": 16,
                            "20대": 15,
                            "30대": 30,
                            "40대": 26,
                            "50대+": 13,
                        },
                        "tags": [
                            ("주거 밀집", "blue"),
                            ("소비 급증", "amber"),
                            ("신규 상권 형성", "green"),
                        ],
                        "trend": ["송도2동 카페", "송도2동 맛집", "신규 상가"],
                        "food": ["카페형 베이커리↑", "가족 레스토랑", "편의식 전문점"],
                        "insights": [
                            "소비 급증 중인 신흥 상권: 신규 입주세대 증가로 생활밀착형 상권 육성에 적합.",
                            "40대 가족 소비층 강세: 가족 외식·교육 관련 소비 중심의 MD 구성이 유효.",
                        ],
                    },
                    "연수1동": {},
                    "연수2동": {},
                    "연수3동": {},
                    "청학동": {},
                    "선학동": {},
                    "옥련1동": {},
                    "옥련2동": {},
                    "동춘1동": {},
                    "동춘2동": {},
                    "동춘3동": {},
                },
            },
            "남동구": {
                "pop": "52.1만",
                "popT": "+0.3%",
                "retail": 110.0,
                "spend": "185만원",
                "retailT": "+0.8%",
                "grdp": "12.1%",
                "tags": [("구월상권", "blue"), ("소래포구 관광", "green"), ("남동공단", "amber")],
                "food": ["소래포구 해산물↑", "구월동 음식거리", "간석오거리 카페"],
                "trend": ["구월동 쇼핑", "남동공단 채용", "소래포구 주차"],
                "dongs": {
                    "구월1동": {},
                    "구월2동": {},
                    "구월3동": {},
                    "간석1동": {},
                    "간석2동": {},
                    "만수1동": {},
                    "만수2동": {},
                    "서창동": {},
                },
            },
            "부평구": {
                "pop": "50.8만",
                "popT": "-0.5%",
                "retail": 106.0,
                "spend": "176만원",
                "retailT": "-0.3%",
                "grdp": "10.8%",
                "tags": [("부평역 상권", "blue"), ("문화특구", "green"), ("재개발 이슈", "amber")],
                "food": ["부평 먹자골목↑", "삼산동 카페거리", "갈산동 브런치"],
                "trend": ["부평역 맛집", "부평 재개발", "문화특구 행사"],
                "dongs": {
                    "부평1동": {},
                    "부평2동": {},
                    "부평3동": {},
                    "십정1동": {},
                    "산곡1동": {},
                    "갈산1동": {},
                },
            },
        },
    },
    "서울": {
        "pop": "941만",
        "grdp": "480조",
        "retail": 118.7,
        "spend": "234만원",
        "popT": "-0.4%",
        "retailT": "+1.5%",
        "tags": [
            ("성수 팝업 열풍", "blue"),
            ("강남 명품↑", "amber"),
            ("2030 소비회복", "green"),
            ("외국인 관광객", "blue"),
        ],
        "food": ["성수 빈티지샵 핫플", "한남동 카페거리↑", "강남 오마카세 대기↑"],
        "trend": ["성수동 팝업스토어", "강남 명품 세일", "한남동 맛집"],
        "districts": {
            "강남구": {
                "pop": "55.3만",
                "popT": "+0.2%",
                "retail": 132.0,
                "spend": "312만원",
                "retailT": "+2.1%",
                "grdp": "9.8%",
                "tags": [("명품 소비↑", "amber"), ("청담 플래그십", "blue"), ("압구정 재개발", "amber")],
                "food": ["오마카세 대기↑", "청담 파인다이닝", "압구정 카페거리"],
                "trend": ["강남 명품 세일", "압구정 재개발", "청담 레스토랑"],
                "dongs": {
                    "압구정동": {},
                    "신사동": {},
                    "청담동": {},
                    "역삼1동": {},
                    "역삼2동": {},
                    "삼성1동": {},
                    "대치1동": {},
                    "개포1동": {},
                },
            },
            "성동구": {
                "pop": "30.1만",
                "popT": "+1.2%",
                "retail": 124.0,
                "spend": "245만원",
                "retailT": "+3.4%",
                "grdp": "4.2%",
                "tags": [("성수 팝업 성지", "blue"), ("MZ 핫플", "green"), ("젠트리피케이션", "amber")],
                "food": ["성수 팝업 줄서기", "카페 뚝도시장↑", "왕십리 먹자골목"],
                "trend": ["성수동 팝업", "성수 카페", "뚝섬역 맛집"],
                "dongs": {
                    "성수1가1동": {},
                    "성수1가2동": {},
                    "성수2가1동": {},
                    "왕십리2동": {},
                    "행당1동": {},
                    "금호1가동": {},
                },
            },
            "마포구": {
                "pop": "37.8만",
                "popT": "-0.2%",
                "retail": 119.0,
                "spend": "228만원",
                "retailT": "+1.2%",
                "grdp": "5.1%",
                "tags": [("홍대 상권", "blue"), ("망원 로컬", "green"), ("연남 카페거리", "green")],
                "food": ["망원동 브런치↑", "연남동 카페거리", "홍대 클럽거리"],
                "trend": ["홍대 맛집", "망원동 카페", "연남동 팝업"],
                "dongs": {
                    "서교동": {},
                    "연남동": {},
                    "망원1동": {},
                    "합정동": {},
                    "상암동": {},
                    "성산1동": {},
                },
            },
        },
    },
    "부산": {
        "pop": "332만",
        "grdp": "98.5조",
        "retail": 108.3,
        "spend": "186만원",
        "popT": "-0.6%",
        "retailT": "-0.8%",
        "tags": [("해운대 관광시즌", "blue"), ("북항 재개발", "amber"), ("서면 상권 회복", "green")],
        "food": ["해운대 씨푸드↑", "서면 로컬카페↑", "광안리 루프탑 바"],
        "trend": ["부산 해수욕장", "해운대 맛집", "북항 개발"],
        "districts": {
            "해운대구": {
                "pop": "41.8만",
                "popT": "-0.3%",
                "retail": 114.0,
                "spend": "198만원",
                "retailT": "+0.8%",
                "grdp": "8.4%",
                "tags": [("해변 관광", "blue"), ("마린시티 부촌", "amber"), ("센텀 쇼핑", "blue")],
                "food": ["해수욕장 씨푸드↑", "센텀 레스토랑", "마린시티 와인바"],
                "trend": ["해운대 해수욕장", "센텀시티 쇼핑", "마린시티 맛집"],
                "dongs": {"우1동": {}, "중1동": {}, "재송1동": {}, "반여1동": {}, "좌1동": {}, "송정동": {}},
            },
            "부산진구": {
                "pop": "37.1만",
                "popT": "-0.7%",
                "retail": 109.0,
                "spend": "182만원",
                "retailT": "-0.2%",
                "grdp": "6.2%",
                "tags": [("서면 중심상권", "blue"), ("롯데백화점 부산", "blue"), ("전포카페거리", "green")],
                "food": ["서면 먹자골목↑", "전포카페거리 MZ↑", "부전시장 먹거리"],
                "trend": ["서면 맛집", "전포 카페", "부산진 쇼핑"],
                "dongs": {"부전1동": {}, "전포1동": {}, "전포2동": {}, "개금1동": {}, "당감1동": {}},
            },
        },
    },
}

KPI_DF = pd.DataFrame(
    [
        ["분석 소요시간 절감", "1인 주 4시간", "1인 주 24분 (↓90%)", "팀원 작업일지 월 측정"],
        ["팀 전체 절감 시간", "주 36시간", "주 3.6시간 (32.4h 절감)", "시스템 접속 로그"],
        ["데이터 업데이트 주기", "주 1~2회 수작업", "매일 자동 갱신", "스케줄러 실행 로그"],
        ["분석 커버 지역 수", "2~3개 지역/담당", "전국 17개 광역시도 100%", "대시보드 지역 탭 수"],
        ["MD 보고서 작성 시간", "보고서당 평균 3시간", "보고서당 1시간 이내 (↓67%)", "착수~완료 시간 측정"],
    ],
    columns=["KPI", "현재 (Before)", "목표 (After)", "측정 방식"],
)

RISKS = [
    {
        "title": "데이터 정확도·신뢰성",
        "tag": "공공 API 오류·결측, AI 요약 오류",
        "action": "원본 소스 링크 동시 노출, 월 1회 샘플 검증, AI 요약 검토 플래그 추가",
    },
    {
        "title": "초기 구축 비용·일정",
        "tag": "개발 인력 부재, 일정 지연",
        "action": "무료 공공 API 중심 MVP 우선 구축, 8주 타임박스 내 최소 기능 우선 완성",
    },
    {
        "title": "구성원 활용도 저하",
        "tag": "학습 저항, 기존 습관 유지",
        "action": "파일럿 2명 설계 참여, 1페이지 가이드 제작, 4주 병행 운영 후 전환",
    },
]

MILESTONES = [
    ("1–2주차", "기반 설계", ["요구사항 정의", "데이터 소스 확정", "API 연결 검증", "화면 와이어프레임"]),
    ("3–4주차", "MVP 개발", ["통계청 API 자동 수집", "AI 키워드 추출 연동", "지역 클릭 대시보드", "2개 지역 파일럿"]),
    ("5–6주차", "고도화·검증", ["전국 17개 지역 확대", "맛집·트렌드 연동", "행정동 드릴다운 완성", "데이터 정확도 검증"]),
    ("7–8주차", "운영 전환", ["팀 전체 사용법 교육", "기존 방식 병행 후 전환", "KPI 초기값 측정", "개선사항 수집·반영"]),
]


# -----------------------------
# Helpers
# -----------------------------
def render_tags(tags):
    html = ""
    mapping = {
        "blue": "tag-blue",
        "green": "tag-green",
        "amber": "tag-amber",
        "red": "tag-red",
    }
    for text, color in tags:
        html += f'<span class="tag {mapping.get(color, "tag-blue")}">{text}</span>'
    st.markdown(html, unsafe_allow_html=True)


def updown_text(value):
    return "증가" if str(value).startswith("+") else "감소"


def metric_card(label, value, delta=None):
    with st.container():
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="small-label">{label}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:1.4rem;font-weight:800;color:#0f2d52;">{value}</div>', unsafe_allow_html=True)
        if delta:
            st.caption(delta)
        st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# Header
# -----------------------------
st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">AI 활용 프로젝트 기획서</div>
        <h1 style="margin:0;">지역 거시환경 <span style="color:#8dc4ff;">AI 자동 분석</span> 시스템 구축</h1>
        <p style="margin-top:0.7rem;margin-bottom:0.5rem;font-size:1.05rem;opacity:0.9;">
            Regional Intelligence Dashboard — 영업기획팀 효율화 프로젝트
        </p>
        <p style="margin:0;opacity:0.8;">제안팀: 영업기획팀 · 대상: 9명 전체 구성원 · 기간: 총 8주(4단계) · 작성일: 2026.04</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Summary
# -----------------------------
st.markdown('<div class="section-title">01. 요약</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        """
        <div class="metric-card metric-red">
            <div class="small-label">문제</div>
            <div class="big-number">36h</div>
            <div>지역별 거시경제·트렌드 데이터를 <b>1인당 주 4시간 이상</b> 수작업 수집·분석. 팀 전체 주 36시간 낭비.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        """
        <div class="metric-card metric-blue">
            <div class="small-label">솔루션</div>
            <div class="big-number">3단계</div>
            <div>AI가 통계·트렌드·뉴스를 수집·분석하고 <b>시·도 → 행정구 → 행정동</b> 드릴다운 대시보드 제공.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        """
        <div class="metric-card metric-green">
            <div class="small-label">기대효과</div>
            <div class="big-number">↓90%</div>
            <div>분석 소요시간 <b>90% 단축</b> (4시간 → 24분), 데이터 정확도 향상, MD 의사결정 속도 개선.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------
# Problem
# -----------------------------
st.markdown('<div class="section-title">02. 현황 및 문제 정의</div>', unsafe_allow_html=True)
st.write(
    """
현재 영업기획팀은 지역별 거시경제 분석 자료를 통계청 KOSIS, 검색 트렌드, 뉴스 등 여러 소스에서 직접 수집하고 있습니다.
이 과정에서 1인당 최소 4시간, 팀 전체로는 주 36시간 이상의 시간이 단순 수집 작업에 소비됩니다.

또한 담당자별 분석 기준과 수집 범위가 달라 동일 지역에 대한 해석이 달라질 수 있고,
트렌드·이슈 데이터는 실시간성이 중요한데도 수작업 구조상 주 1~2회 업데이트가 한계입니다.
"""
)
st.markdown(
    """
    <div class="highlight">
    ※ 수치 근거: 팀원 인터뷰 기반 평균 소요시간 추정 (1인 4시간 × 9명). 도입 전 2주간 실제 측정으로 검증 권장.
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Solution
# -----------------------------
st.markdown('<div class="section-title">03. AI 솔루션 설계</div>', unsafe_allow_html=True)
st.write("AI 솔루션은 Problem → Data → Insight → Action의 4단계 구조로 설계됩니다.")

flow_cols = st.columns(4)
flow_items = [
    ("Problem", "분산 데이터", "통계청, 검색포털, 뉴스 등 소스별 수작업 수집"),
    ("Data", "자동 수집", "API·크롤링으로 지역별 데이터 실시간 통합"),
    ("Insight", "AI 분석", "LLM이 트렌드 요약·이슈 추출·소비지표 해석"),
    ("Action", "MD 의사결정", "대시보드 클릭 → 인사이트 즉시 활용"),
]
for col, (tag, title, desc) in zip(flow_cols, flow_items):
    with col:
        st.markdown(
            f"""
            <div class="card">
                <div class="small-label">{tag}</div>
                <div style="font-size:1.1rem;font-weight:800;color:#0f2d52;margin-bottom:0.4rem;">{title}</div>
                <div style="color:#4a5568;">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write(
    """
데이터 수집 레이어는 통계청 KOSIS Open API, 검색 트렌드, 뉴스 RSS 등을 자동 호출하여 지역별 데이터를 갱신합니다.
AI 분석 레이어는 핵심 이슈 키워드, 소비 트렌드, 맛집 버즈 등을 자동 추출·요약하고,
시각화 레이어는 시·도 → 행정구 → 행정동 3단계 드릴다운으로 탐색할 수 있게 구성합니다.
"""
)

col_ai, col_human = st.columns(2)
with col_ai:
    st.markdown("#### AI 담당 역할")
    st.markdown(
        """
- 공공 API·뉴스 데이터 자동 수집 및 정제  
- 지역별 이슈 키워드 추출 및 요약  
- 소비 트렌드 변화 감지 및 알림  
- 지표 간 상관관계 1차 해석  
- 차트·표·태그 자동 생성
"""
    )
with col_human:
    st.markdown("#### 사람 담당 역할")
    st.markdown(
        """
- MD 전략 방향성 및 기획 판단  
- AI 분석 결과의 맥락적 해석  
- 이상 데이터 검증 및 보정  
- 임원 보고 자료 편집·커뮤니케이션  
- 신규 분석 어젠다 설정
"""
    )

# -----------------------------
# KPI
# -----------------------------
st.markdown('<div class="section-title">04. 기대 효과 — KPI 5가지</div>', unsafe_allow_html=True)
st.dataframe(KPI_DF, use_container_width=True, hide_index=True)
st.markdown(
    """
    <div class="highlight">
    ※ 목표 수치는 유사 사례 기반 추정치. 도입 후 4주 시점 중간 측정으로 재조정 권장.
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Risks
# -----------------------------
st.markdown('<div class="section-title">05. 리스크 및 대응 방안</div>', unsafe_allow_html=True)
risk_cols = st.columns(3)
for col, risk in zip(risk_cols, RISKS):
    with col:
        st.markdown(
            f"""
            <div class="card">
                <div class="small-label">{risk["tag"]}</div>
                <div style="font-size:1.05rem;font-weight:800;color:#0f2d52;margin-bottom:0.5rem;">{risk["title"]}</div>
                <div style="color:#4a5568;">{risk["action"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# -----------------------------
# Milestones
# -----------------------------
st.markdown('<div class="section-title">06. 실행 계획 — 8주 마일스톤</div>', unsafe_allow_html=True)
ms_cols = st.columns(4)
for col, (week, title, tasks) in zip(ms_cols, MILESTONES):
    with col:
        st.markdown(f"#### {week}")
        st.markdown(f"**{title}**")
        for task in tasks:
            st.markdown(f"- {task}")

# -----------------------------
# Dashboard
# -----------------------------
st.markdown('<div class="section-title">부록. 대시보드 시안 — 라이브 데모</div>', unsafe_allow_html=True)
st.info("시·도 → 행정구 → 행정동 3단계 드릴다운 구조를 Streamlit으로 구현한 예시입니다.")

search = st.text_input("지역명 검색", placeholder="예: 인천, 연수구, 송도1동, 강남구")

sido_options = list(DB.keys())

if search:
    results = []
    for sido_name, sido_data in DB.items():
        if search in sido_name:
            results.append(("시·도", sido_name))
        for gu_name, gu_data in sido_data["districts"].items():
            if search in gu_name:
                results.append(("행정구", f"{sido_name} > {gu_name}"))
            for dong_name in gu_data["dongs"].keys():
                if search in dong_name:
                    results.append(("행정동", f"{sido_name} > {gu_name} > {dong_name}"))

    st.subheader(f"검색 결과 ({len(results)}건)")
    if results:
        for rtype, rname in results[:20]:
            st.write(f"- **{rtype}**: {rname}")
    else:
        st.write("검색 결과가 없습니다.")

st.markdown("### 1) 시·도 선택")
selected_sido = st.selectbox("시·도", sido_options)

sido_data = DB[selected_sido]
m1, m2, m3, m4 = st.columns(4)
with m1:
    metric_card("인구수", sido_data["pop"], f"전년 대비 {sido_data['popT']} ({updown_text(sido_data['popT'])})")
with m2:
    metric_card("소매판매지수", sido_data["retail"], f"전년 대비 {sido_data['retailT']}")
with m3:
    metric_card("1인당 소비지출", sido_data["spend"])
with m4:
    metric_card("GRDP", sido_data["grdp"])

st.markdown("**이슈 키워드**")
render_tags(sido_data["tags"])

c_food, c_trend = st.columns(2)
with c_food:
    st.markdown("#### 인기 맛집·소비 트렌드")
    for i, item in enumerate(sido_data["food"], start=1):
        st.write(f"{i}. {item}")
with c_trend:
    st.markdown("#### 급상승 검색어")
    for i, item in enumerate(sido_data["trend"], start=1):
        st.write(f"{i}. {item}")

st.markdown("---")
st.markdown("### 2) 행정구·군 선택")
gu_options = list(sido_data["districts"].keys())
selected_gu = st.selectbox("행정구·군", gu_options)

gu_data = sido_data["districts"][selected_gu]
m1, m2, m3, m4 = st.columns(4)
with m1:
    metric_card("인구수", gu_data["pop"], f"전년 대비 {gu_data['popT']}")
with m2:
    metric_card("소매판매지수", gu_data["retail"], f"전년 대비 {gu_data['retailT']}")
with m3:
    metric_card("1인당 소비지출", gu_data["spend"])
with m4:
    metric_card("GRDP/기여도", gu_data["grdp"])

st.markdown("**이슈 키워드**")
render_tags(gu_data["tags"])

c_food2, c_trend2 = st.columns(2)
with c_food2:
    st.markdown("#### 인기 맛집·소비 트렌드")
    for i, item in enumerate(gu_data["food"], start=1):
        st.write(f"{i}. {item}")
with c_trend2:
    st.markdown("#### 급상승 검색어")
    for i, item in enumerate(gu_data["trend"], start=1):
        st.write(f"{i}. {item}")

st.markdown("---")
st.markdown("### 3) 행정동 선택")
dong_options = list(gu_data["dongs"].keys())
selected_dong = st.selectbox("행정동", dong_options)

dong_data = gu_data["dongs"][selected_dong]

if dong_data:
    d1, d2, d3, d4 = st.columns(4)
    with d1:
        metric_card("총 인구", dong_data["pop"], f"전년 대비 {dong_data['popT']}")
    with d2:
        metric_card("1인당 월 소비지출", dong_data["spend"])
    with d3:
        metric_card("외국인 비율", dong_data["foreign"])
    with d4:
        metric_card("소매판매지수", dong_data["retail"])

    st.markdown("**행정동 키워드**")
    render_tags(dong_data["tags"])

    age_df = pd.DataFrame(
        {
            "연령대": list(dong_data["age"].keys()),
            "비중": list(dong_data["age"].values()),
        }
    )
    st.markdown("#### 연령대별 인구 분포")
    st.bar_chart(age_df.set_index("연령대"))

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 급상승 검색 키워드")
        for i, item in enumerate(dong_data["trend"], start=1):
            st.write(f"{i}. {item}")
    with c2:
        st.markdown("#### 인기 맛집·소비 업종")
        for i, item in enumerate(dong_data["food"], start=1):
            st.write(f"{i}. {item}")

    st.markdown("#### AI 종합 인사이트")
    for insight in dong_data["insights"]:
        st.success(insight)
else:
    st.warning("이 행정동의 상세 데이터는 실제 시스템 구축 후 통계청 KOSIS API 및 외부 데이터와 연동하여 자동 수집되도록 설계할 수 있습니다.")

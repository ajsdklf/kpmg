import os 
import streamlit as st 
from openai import OpenAI
import openai_function as of
from audio_recorder_streamlit import audio_recorder
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

os.environ["OPENAI_API_KEY"] = "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"

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

activity_grader_id = "asst_zXxVZ8765kYkKeKcwI0MMHLB"
RCS_capabilities_id = "asst_KzXXln3wovplS0KqE1KLbH8e"
roadmap_assistant_id = "asst_gfvgWuhZJpxveh3q6DyWgHyd"

integrity = """
정직, 공정, 일관성, 책임 
올바른 일을 한다. 업무 내·외적인 모든 상황에서 말과 행동 및 의사결정을 함에 있어 정직하고 공정하며 일관성이 있다. 일상의 모든 행동에 대해 책임을 지며, 외압이 있는 상황을 포함한 모든 상황에서 최고의 도덕 및 윤리 기준을 준수한다. 약속을 지키며 타인의 모범이 됩니다. 
윤리적 책임/ 올바른 의사결정
공정하게 경쟁한다. 자유경쟁시장의 목표를 분명히 지지한다. 
객관성과 독립성을 유지한다. 갈등을 초래할 수 있는 이해상충을 계약 업무 전에 파악하고 해소한다. 
불법행위나 비윤리적인 행위를 용인하지 않는다. 불법적인 행위 또는 인권에 반하는 행위를 묵과하지 않는다. 
법률, 규정, 기준을 준수한다.
의심스러운 부분이 있다면 자문을 구한다. 개인이 모든 것을 알고 있을 수는 없으므로 본인 또는 제3 자가 실수할 가능성이 있다고 판단되는 경우 자문을 구한다.
성과 달성에 대한 압박 또는 부적절한 행동을 유도하는 압력헤 타협하지 않는다. 
개인적인 일에 있어서도 윤리강령과 일관된 방식으로 행동한다. 
옳지 않다고 판단되는 경우, 이슈를 제기할 용기를 가진다. 
"""

excellence = """
역량 강화, 고품질 업무, 지속적 학습, 업무 개선, 새로운 도전과 피드백
끊임없이 역량을 강화한다. 최고의 전문가 기준을 준수하며 고품질 서비스를 제공한다. 이는 업무에 대한 지적 호기심과 책임감을 가지고 지속적으로 수행하는 학습을 통해 이루어진다. 각종 데이터와 통찰력을 활용하여 업무의 개선을 끊임없이 도모하며, 새로운 도전과 피드백을 적극적으로 수용한다. 이를 통해 발전해 나아간다. 
동기부여/ 자기 인식/ 품질 지향 / 고객이 신뢰하는
업계 최초 유연근로 도입, 최신IT플랫폼을 접목한 스마트 오피스 구축 등 구성원들이 업무에 집중할 수 있도록 ‘행복한 일터’를 만들어 나간다.
공정한 평가, 최고의 보상: 공정한 평가와 업계 최고 수준의 보상을 통해 인재들을 최고의 대우로 예우한다
산업별 전문화 조직, 엄격한 품질관리, 투명성 및 독립성 유지를 기반으로 차별화된 감사서비스를 제공한다. 
해외Member Firm 파견, Korea Desk, 1~3년차 집중 육성 프로그램 등을 통해 글로벌 리더로 성장할 수 있도록 지속적인 교육과 경력개발의 기회를 제공한다.
다양한 경력 개발 기회 제공을 위해 본부이동 제도인 ‘New Challenge Program’을 운영하고 있다. 매년 본부 수요에 따라 이동 희망본부의 인터뷰를 통해 영구 이동하는 제도로 연1회 운영하고 있다.
삼정KPMG에 신입회계사로 입사하게 되면3년간 ‘Junior 집중 육성 프로그램’에 따라 교육을 이수하게 된다. 1년차부터3년차까지, 각 연차에 맞춘 체계적인 집합 교육, 온라인 교육 등을 통해 전문가로 성장할 수 있도록 지원하고 있다. 또한 각Function, 직급별 직무에 맞추어 다양한 사내 교육을 제공하고 있다.
의견의 차이를 표현하거나 비호의적인 메시지를 전달하는 것을 두려워하지 않는다.
"""

courage = """
새로운 아이디어, 전문가적 의구심
진취적이고 담대하게 생각하고 행동한다. 새로운 아이디어에 개방적이며, 우리의 지식과 경험의 한계를 정직하게 인정한다. 이는 의심스러운 상황에서 질문하고 전문가적 의구심을 발휘하는 것 과도 관련되어 있다. 우리는 옳지 않은 것을 인지하였을 때 적극적으로 의견을 개진한다. 본인 스스로 옳지 않음을 먼저 말할 수 있는 용기 있는 자들을 지지한다. 용기란 안전지대에서 기꺼이 나올 수 있는 담대함이다. 
전략적 관점/ 혁신 추구
"""

together = """
다양성, 상호존중, 협업
서로 존중하고 다양성으로부터 강점을 끌어낸다. 팀내에서, 팀간에 그리고 조직 외부의 사람들과 함께 일할 때 최고의 결과물을 만들어 낼 수 있다. 협업을 통해 의견이 형성되고 창의력이 도출된다는 것을 알고 있기 때문에 함께 일하는 것은 중요하다. 다양한 배경, 능력, 관점, 경험을 가진 사람들을 포용하며, 서로 다른 의견 들을 경청한다. 타인을 돌보고 배려하며, 모든 사람들이 소속감을 느낄 수 있는 포용적인 환경을 만들기 위해 매진한다. 
다양성 존중/ 협력관계 구축 / 구성원이 자랑스러워하는
함께 성장할 수 있는 통합환경을 지지한다. 인종, 민족, 성별, 성 정체성, 성적 취향, 장애, 나이, 결혼 여부, 종교적 신념 등에 있어서 다양성을 인정하고 어떠한 차별도 없는 평등한 조직 문화를 약속한다. 모든 사람을 존중하고 존엄하게 대한다. 차이를 가치 있고 소중하게 여기며 포용적인 통합 환경을 조성한다. 
리더의 책임 : 솔선수범한다, 팀원을 지원한다.팀원의 역량을 이끌어낸다. 명확하고 측정 가능하며 도전할 수 있는 목표를 제시하고, 윤리적인 행동과 높은 수준의 고객 서비스 제공을 촉진한다. 일관되고 공정한 기준을 제시한다. 리더로서 기준을 일관되고 공정하게 적용하며 규정 준수를 촉진한다. 신중하게 판단한다. 부하 직원들이 제시하는 질문 및 문제들에 대해 본인의 신념을 바탕으로 신중하게 판단하여 대응한다. 결과에 책임을 진다. 부하 직원 또는 본인에 의해 문제가 발생할 경우 스스로 그에 대한 책임을 질 수 있는 마음가짐이 되어 있어야 한다.
"""

for_better = """
장기적 안목, 지역사회와 사회 전반에 지속 가능하고 긍정적인 변화
사회와 미래를 위해 의미 있는 일을 한다. 매순간, 일상적인 선택에 있어서도, 장기적인 안목으로 생각하고 행동하는 것을 의미한다. 자본시장에 신뢰를 부여하는 역할의 중요성을 결코 망각하지 않는다. 이 세상을 보다 더 살기 좋은 곳으로 만들기 위해 지역사회와 사회 전반에 지속가능하고 긍정적인 변화를 만들어 나아간다
미래 세대를 생각하며 실질적인 변화를 주도한다. 
올바른 판단력과 통찰력을 통해 지속 가능한 변화를 지향한다. 
신뢰를 부여하고 세상의 변화를 주도한다. 
책임감 있는 기업 시민으로서의 역할을 한다. 책임감 있는 기업시민으로서 기후변화, 지속 가능한 발전, 국제 개발과 연관된 글로벌 이슈들에 있어서 적극적인 역할을 담당한다. 
훌륭한 기업 시민 정신을 장려한다. 
회계전문가의 역할을 증진시키고, 국제자본시장에서 신뢰도를 향상시킨다. 
시장경제기능의 발전에 기여한다. 
환경적 영향을 최소화하기 위해 관리한다. 
보다 강한 커뮤니티를 구축하기 위하여, 다른 산업, 정부 및 자선 단체들과 협업한다.
사회로부터의 신뢰를 구축한다. 사회로부터의 신뢰는 규제 기관, 투자자 및 고객부터 지역 사회 및 시민단체에 이르기까지 광범위한 외부 이해관계자와의 관계 속에서 구축된다. 이러한 다양한 이해관계자와의 관계는 변화 하는 비즈니스 환경에 계속해서 대응하고 사회적 기대를 지속적으로 충족시킬 수 있는 방법에 대한 폭넓은 시각과 새로운 사고를 제공한다. 
품질에 대해 끊임없이 관리하며, 우리가 하는 모든 일에 있어서 매 순간 공공의 신뢰를 지키고 옳은 일을 올바른 방법으로 한다. 
사회로부터의 신뢰를 얻기 위해서는 리더 및 전문가로서의 다짐을 지속적으로 강화하는 것이 중요하다.
"""

option = st.sidebar.selectbox(
    "이용할 기능을 선택하세요",
    ("지원서 활동 요약 / 회사와의 적합도", "직무 역량 분석 (RCS), 로드맵 추천", "로드맵 추천 (RCS)", "직무 역량 분석 (MCS-1)", "로드맵 추천 (MCS-1)", "부서별 적합도", "면접 텍스트 변환 / 분석")
)

st.title(f"{option}")

if option == "지원서 활동 요약 / 회사와의 적합도":
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    integrity_embedding = of.get_embedding(integrity)
    courage_embedding = of.get_embedding(courage)
    together_embedding = of.get_embedding(together)
    for_better_embedding = of.get_embedding(for_better)
    excellence_embedding = of.get_embedding(excellence)
    
    norm_integrity = np.linalg.norm(integrity_embedding)
    norm_courage = np.linalg.norm(courage_embedding)
    norm_together = np.linalg.norm(together_embedding)
    norm_for_better = np.linalg.norm(for_better_embedding)
    norm_excellence = np.linalg.norm(excellence_embedding)
    
    prompt = st.chat_input("submit application form here.")
    if prompt:
        thread = client.beta.threads.create()
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        run = of.complete_run(of.create_run(activity_grader_id, thread, prompt), thread)
        
        model_response = of.get_response(thread)
        full_model_response = ""
        
        for i in range(1, len(model_response.data)):
            full_model_response += model_response.data[i].content[0].text.value
        
        st.session_state.messages.append({"role": "assistant", "content": full_model_response})
        
        with st.chat_message("assistant"):
            st.markdown(full_model_response)
        
        summarized_prompt = full_model_response
        
        application_embedding = of.get_embedding(summarized_prompt)
        norm_application = np.linalg.norm(application_embedding)
        
        dot_integreity = np.dot(integrity_embedding, application_embedding)
        dot_excellence = np.dot(excellence_embedding, application_embedding)
        dot_courage = np.dot(courage_embedding, application_embedding)
        dot_together = np.dot(together_embedding, application_embedding)
        dot_for_better = np.dot(for_better_embedding, application_embedding)
        
        similarity_integrity = 170 * dot_integreity / (norm_integrity * norm_application)
        similarity_excellence = 170 * dot_excellence / (norm_excellence * norm_application)
        similarity_courage = 170 * dot_courage / (norm_courage * norm_application)
        similarity_together = 170 * dot_together / (norm_together * norm_application)
        similarity_for_better = 170 * dot_for_better / (norm_for_better * norm_application)
        
        similarity_list = [similarity_integrity, similarity_excellence, similarity_courage, similarity_together, similarity_for_better]
        
        integer_list = [int(num) for num in similarity_list]
        
        labels = np.array(["integrity", "excellence", "courage", "together", "for_better"])
        stats = np.array(similarity_list)
        
        num_vars = len(labels)
        
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        stats = np.concatenate((stats, [stats[0]]))
        angles += angles[:1]
        
        fig, ax, = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.fill(angles, stats, color="red", alpha=0.25)
        ax.plot(angles, stats, color="red", linewidth=2)
        
        ax.set_ylim(0,100)
        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        
        st.session_state.messages.append({"role": "assistant", "content": st.pyplot(fig)})
        
        with st.chat_message("assistant"):
            st.markdown(f"integrity: {int(similarity_integrity)}, excellence: {int(similarity_excellence)}, courage: {int(similarity_courage)}, together: {int(similarity_together)}, for_better: {int(similarity_for_better)}")

if option == "면접 텍스트 변환 / 분석":
    uploaded_file = st.file_uploader("음성 파일을 선택하세요.", type=['wav', 'mp3'])

    # 파일이 업로드되면, 정보를 표시
    if uploaded_file is not None:
        # 파일의 이름과 크기를 표시 (옵션)
        file_details = {"FileName":uploaded_file.name, "FileType":uploaded_file.type, "FileSize":uploaded_file.size}
        st.write(file_details)
        
        # 파일을 처리하거나 저장하는 로직을 여기에 추가
        # 예: 파일을 임시 디렉토리에 저장
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success('파일 업로드 성공!')
        
        audio_file = open(uploaded_file.name, "rb")
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            prompt="면접문이 제시될거야. 면접관의 질문에 해당하는 부분은 {면접관의 질문 : 내용}의 형식으로, 면접자의 응답에 해당하는 부분은 {면접자의 답변 : 내용}으로 구분해줘."
        )
        
        interview_text = transcript.text
        interview_summarizer_id = "asst_ySDu9a5UVmhRIgul2fL23GeJ"
        
        thread = client.beta.threads.create()
        run = of.complete_run(of.create_run(interview_summarizer_id, thread, interview_text), thread)
        
        model_response = of.get_response(thread)
        for i in range(1, len(model_response.data)):
            st.session_state.messages.append({"role": "assistant", "content": model_response.data[1].content[0].text.value})
        full_model_response = ""
        
        with st.chat_message("assistant"):
            st.markdown(f"면접 내용 텍스트 전환 : {interview_text}")
            for i in range(1, len(model_response.data)):
                full_model_response += model_response.data[i].content[0].text.value
            st.markdown(full_model_response)

if option == "직무 역량 분석 (RCS), 로드맵 추천":
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    의사소통능력 = """의사소통능력이란 직업인이 직업생활에서 우리말로 된 문서를 읽고 이해하거나, 상대방의 말을 듣고 의미를 파악하며, 자신의 의사를 정확하게 표현하는 능력을 의미한다. 또한 국제화 시대에 간단한 외국어 자료를 읽고 이해하며, 외국인의 간단한 의사표시를 이해하는 능력까지 포함한다. 이에 따라 의사소통능력은 문서이해능력, 문서작성능력, 경청능력, 의사표현능력 및 기초 외국어능력으로 구분될 수 있다. 직업생활에서 필요한 문서를 읽고 내용을 이해하며 요점을 파악하는 문서이해능력, 목적과 상황에 적합한 아이디어와 정보를 전달할 수 있는 문서를 작성하는 문서작성능력, 다른 사람의 말을 주의 깊게 들으며 공감하는 경청능력, 목적과 상황에 맞는 말과 비언어적 행동을 통해서 아이디어와 정보를 효과적으로 전달하는 의사표현능력, 그리고 외국어로 된 간단한 자료를 이해하거나 간단한 외국인의 의사표현을 이해하는 기초외국어능력으로 구성되어 있다.
    """
    
    자원관리능력 = """자원관리능력이란 직업생활에서 시간, 예산, 물적자원, 인적자원 등의 자원 가운데 무엇이 얼마나 필요한지를 확인하고, 가용할 수 있는 자원을 최대한 확보하여 실제 업무에 어떻게 활용할 것인지에 대한 계획을 수립하고, 계획에 따라 확보한 자원을 효율적으로 활용하여 관리하는 능력을 의미한다. 자원관리능력은 ① 시간관리능력, ② 예산관리능력, ③ 물적자원관리능력, ④ 인적자원관리능력으로 구분할 수 있다.시간관리능력은 직업생활에서 필요한 시간자원을 파악하고, 가용할 수 있는 시간자원을 최대한 확보하여 실제 업무에 어떻게 활용할 것인지에 대한 시간계획을 수립하고, 이에 따라 시간을 효율적으로 활용하여 관리하는 능력을 의미한다. 예산관리능력은 직업생활에서 필요한 예산을 파악하고, 가용할 수 있는 예산을 최대한 확보하여 실제 업무에 어떻게 집행할 것인지에 대한 예산계획을 수립하고, 이에 따른 예산을 효율적으로 집행하여 관리하는 능력을 의미한다. 물적자원관리능력은 직업생활에서 필요한 물적자원(재료, 시설자원 등)을 파악하고, 가용할 수 있는 물적자원을 최대한 확보하여 실제 업무에 어떻게 활용할 것인지에 대한 계획을 수립하고, 이에 따른 물적자원을 효율적으로 활용하여 관리하는 능력을 의미한다.인적자원관리능력은 직업생활에서 필요한 인적자원(근로자의 기술, 능력, 업무 등)을 파악하고, 동원할 수 있는 인적자원을 최대한 확보하여 실제 업무에 어떻게 배치할 것인지에 대한 예산계획을 수립하고, 이에 따른 인적자원을 효율적으로 배치하여 관리하는 능력을 의미한다."""
    
    문제해결능력 = """문제해결능력이란 업무 수행 중 문제 상황이 발생하였을 경우 창의적이고 논리적인 사고를 통하여 이를 올바르게 인식하고 적절히 해결하는 능력을 의미한다. 문제해결능력은 사고력과 문제처리능력으로 이루어진다. 사고력은 직업생활에서 발생한 문제를 인식하고 해결하기 위해서 창의적, 논리적, 비판적으로 생각하는 능력이며, 문제처리능력은 문제의 특성을 파악하고 대안을 제시하며 적절한 대안을 선택, 적용하고 그 결과를 평가하여 피드백하는 능력이다."""
    
    정보능력 = """정보능력이란 업무를 수행할 때 기본적인 컴퓨터를 활용하여 필요한 정보를 수집, 분석, 활용하는 능력을 의미한다. 이러한 정보능력은 컴퓨터를 사용하는 컴퓨터활용능력과 업무 수행에 필요한 정보를 수집하고, 분석하여 의미 있는 정보를 찾아내며, 찾아낸 정보를 업무 수행에 적절하도록 조직, 관리하고 활용하는 능력인 정보처리능력으로 구성되어 있다."""
    
    조직이해능력 = """조직이해능력이란 일상적인 일 경험에서 요구되는 조직의 체제와 경영 및 업무 수행, 그리고 국제감각을 이해하는 능력을 의미한다. 이러한 조직이해능력은 직업생활에 필요한 조직의 경영전략과 의사결정과정을 이해하는 경영이해능력, 조직의 목표와 구조, 집단의 특성 등을 이해하는 체제이해능력, 업무의 특징과 업무 계획을 수립하는 업무이해능력, 다른 나라의 문화를 이해하고 효과적인 소통을 하며 국제동향을 파악하는 국제감각으로 구성되어 있다."""
    
    수리능력 = """수리능력이란 업무 상황에서 요구되는 사칙연산과 기초적인 통계를 이해하고, 도표 또는 자료(데이터)의 의미를 파악하거나, 도표 또는 자료(데이터)를 이용해서 합리적이고 객관적인 결과를 효과적으로 제시하는 능력을 의미한다. 이러한 수리능력은 업무 상황에서 필요한 기초적인 사칙연산과 계산방법을 이해하고 활용하는 기초연산능력, 업무 상황에서 평균, 합계, 빈도와 같은 기초적인 자료의 정리 요약 등을 실행하고 자료(데이터)의 특성과 경향성을 파악하는 기초통계능력(기술통계), 도표(그림, 표, 그래프 등)의 의미를 파악하고 필요한 정보를 해석하는 도표분석능력(추리통계), 도표(그림, 표, 그래프 등)를 이용하여 도표를 효과적으로 제시하는 도표작성능력으로 구성되어 있다."""
    
    자기개발능력 = """자기개발능력이란 직업인으로서 자신의 능력, 적성, 특성 등의 객관적 이해를 기초로 자기 발전 목표를 스스로 수립하고 자기관리를 통하여 성취해 나가는 능력을 의미한다. 이러한 자기개발능력은 직업인으로서 자신의 흥미, 적성, 특성 등의 이해에 기초하여 자기 정체감을 형성하는 자아인식능력, 자신의 행동 및 업무 수행을 통제하고 관리하며 합리적이고 균형적으로 정하는 자기관리능력, 자신의 진로에 대한 단계적 목표를 설정하고, 목표성취에 필요한 역량을 개발해 나가는 경력개발능력으로 구성된다."""
    
    대인관계능력 = """대인관계능력이란 직업생활에서 협조적인 관계를 유지하고 조직구성원들에게 도움을 줄 수 있으며 조직내부 및 외부의 갈등을 원만히 해결하고 고객의 요구를 충족시켜줄 수 있는 능력을 의미한다. 이에 따라 대인관계능력은 팀워크능력, 리더십능력, 갈등관리능력, 협상능력, 고객서비스능력으로 구분될 수 있다."""
    
    기술능력 = """기술능력이란 직업인으로서 일상적인 직업생활에 요구되는 수단, 도구, 조작 등에 관한 기술적인 요소들을 이해하고, 적절한 기술을 선택하며, 적용하는 능력을 의미한다. 이러한 기술능력은 직업생활에 필요한 기본적인 기술의 원리 및 절차를 이해하는 기술이해능력, 필요한 기술을 선택하는 기술선택능력, 그리고 선택한 어떤 기술을 실제 적용하는 기술적용능력으로 구성되어 있다.""" 
    
    직업윤리 = """직업윤리란 원만한 직업생활을 위해 필요한 마음가짐과 태도 및 올바른 직업관을 의미하며, 크게 근로윤리와 공동체윤리로 구분된다. 근로윤리는 일에 대한 존중을 바탕으로 근면, 성실하고 정직하게 업무에 임하는 자세이며, 공동체윤리는 인간 존중을 바탕으로 봉사하고, 책임감을 지니며, 규칙을 준수하면서도 예의바른 태도로 업무에 임하는 자세를 뜻한다.
    """

    의사소통능력_embedding = of.get_embedding(의사소통능력)
    자원관리능력_embedding = of.get_embedding(자원관리능력)
    문제해결능력_embedding = of.get_embedding(문제해결능력)
    정보능력_embedding = of.get_embedding(정보능력)
    조직이해능력_embedding = of.get_embedding(조직이해능력)
    수리능력_embedding = of.get_embedding(수리능력)
    자기개발능력_embedding = of.get_embedding(자기개발능력)
    대인관계능력_embedding = of.get_embedding(대인관계능력)
    기술능력_embedding = of.get_embedding(기술능력)
    직업윤리_embedding = of.get_embedding(직업윤리)
    
    norm_의사소통능력 = np.linalg.norm(의사소통능력_embedding)
    norm_자원관리능력 = np.linalg.norm(자원관리능력_embedding)
    norm_문제해결능력 = np.linalg.norm(문제해결능력_embedding)
    norm_정보능력 = np.linalg.norm(정보능력_embedding)
    norm_조직이해능력 = np.linalg.norm(조직이해능력_embedding)
    norm_수리능력 = np.linalg.norm(수리능력_embedding)
    norm_자기개발능력 = np.linalg.norm(자기개발능력_embedding)
    norm_대인관계능력 = np.linalg.norm(대인관계능력_embedding)
    norm_기술능력 = np.linalg.norm(기술능력_embedding)
    norm_직업윤리 = np.linalg.norm(직업윤리_embedding)
    
    prompt = st.chat_input("submit application form here.")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        합격자_embedding = of.get_embedding("""{"스타트업 환경에서의 문제 해결 및 전략적 기획 경험": 4, "이유": "지원자는 스타트업 환경에서 새로운 도전을 열정적으로 적극적으로 해결하고 모금 활동에 기여한 강력한 실적을 보여주었습니다. 국제 경영 회의에서의 경험은 전략적 사고와 혁신적인 문제 해결 능력을 선보였으며, 이는 KPMG RCS가 제공하는 컨설팅 서비스와 매우 관련이 높습니다."},
        
        {"신뢰할 수 있는 위험 컨설턴트가 되고자 하는 야망": 4, "이유": "지원자의 금융 분야에서 명망 있는 위험 컨설턴트가 되고자 하는 분명한 야망은 KPMG RCS가 제공하는 서비스와 잘 부합합니다. 위험 관리에 대한 통찰력과 지식을 습득하겠다는 명시된 목표는 ESG, 기후 요인, 규제 문제에 대한 초점과 함께 전문적 성장과 발전에 대한 강한 헌신을 강조합니다."},
        
        {"국제 경영 회의에서의 전략적 프로젝트 실행": 4, "이유": "지원자가 참여한 이차 전지 산업의 전략적 시장 진입 계획 프로젝트는 강력한 분석 기술과 중요한 문제를 식별하고 실현 가능한 해결책을 제안할 수 있는 능력을 보여줍니다. 시장 조사, 가치 사슬 분석 및 진입 전략 제안에 대한 초점은 높은 수준의 혁신성과 분석력을 보여줍니다."},
        
        {"적응적 시간 관리 및 과제 완수 능력": 3, "이유": "지원자는 변화하는 일정에 적응하고 압박 속에서 과제를 성공적으로 완수할 수 있는 능력을 투자 결정 및 설득력 있는 보고서 작성에 대한 인턴십 경험을 통해 보여주었습니다. 빠르게 변화하는 환경에서 과제를 완수하기 위한 적극적인 접근 방식과 효과적인 커뮤니케이션은 컨설팅 역할에 대한 귀중한 특성입니다."},
        {"효과적인 협업 및 설득력 있는 논쟁": 3, "이유": "지원자는 스타트업 창업자 및 이해관계자와 적극적으로 협력하여 후속 투자를 확보하고 재무 분석 및 ROI 계산에 기반한 설득력 있는 논쟁을 제시한 경험을 통해 강력한 팀워크와 설득력 있는 기술을 입증했습니다. 합의를 향해 노력하고 의사 결정을 긍정적으로 영향을 미칠 수 있는 능력은 지원자를 컨설팅 역할에 적합한 후보로 만듭니다."}
        
        {점수 합계: 18}
        
        {"회사와의 전반적인 적합성": 90, "이유": "지원자는 KPMG RCS가 제공하는 서비스와 높은 수준의 일치를 보여주며, 개인적 및 전문적 발전, 전략적 문제 해결 능력, 효과적인 커뮤니케이션 기술에 대한 강한 헌신을 보여줍니다. 지원자의 야망, 분석 능력, 팀워크 및 적응성은 KPMG RCS에서 컨설팅 역할에 대해 매우 유망한 적합성을 보여줍니다."}""")
        norm_합격자 = np.linalg.norm(합격자_embedding)
        
        similarity_의사소통능력_P = 200 * np.dot(합격자_embedding, 의사소통능력_embedding) / (norm_합격자 * norm_의사소통능력)
        similarity_자원관리능력_P = 200 * np.dot(합격자_embedding, 자원관리능력_embedding) / (norm_합격자 * norm_자원관리능력)
        similarity_문제해결능력_P = 200 * np.dot(합격자_embedding, 문제해결능력_embedding) / (norm_합격자 * norm_문제해결능력)
        similarity_정보능력_P = 200 * np.dot(합격자_embedding, 정보능력_embedding) / (norm_합격자 * norm_정보능력)
        similarity_조직이해능력_P = 200 * np.dot(합격자_embedding, 조직이해능력_embedding) / (norm_합격자 * norm_조직이해능력)
        similarity_수리능력_P = 200 * np.dot(합격자_embedding, 수리능력_embedding) / (norm_합격자 * norm_수리능력)
        similarity_자기개발능력_P = 200 * np.dot(합격자_embedding, 자기개발능력_embedding) / (norm_합격자 * norm_자기개발능력)
        similarity_대인관계능력_P = 200 * np.dot(합격자_embedding, 대인관계능력_embedding) / (norm_합격자 * norm_대인관계능력)
        similarity_기술능력_P = 200 * np.dot(합격자_embedding, 기술능력_embedding) / (norm_합격자 * norm_기술능력)
        similarity_직업윤리_P = 200 * np.dot(합격자_embedding, 직업윤리_embedding) / (norm_합격자 * norm_직업윤리)
        
        similarity_list_P = [similarity_의사소통능력_P, similarity_자원관리능력_P, similarity_문제해결능력_P, similarity_정보능력_P, similarity_조직이해능력_P, similarity_수리능력_P, similarity_자기개발능력_P, similarity_대인관계능력_P, similarity_기술능력_P, similarity_직업윤리_P]
        
        integer_list_P = [int(num) for num in similarity_list_P]
        
        thread = client.beta.threads.create()
        run = of.complete_run(of.create_run(activity_grader_id, thread, prompt), thread)
        
        model_response = of.get_response(thread)
        full_model_response = ""
        
        for i in range(1, len(model_response.data)):
            full_model_response += model_response.data[i].content[0].text.value
        
        application_embedding = of.get_embedding(full_model_response)
        norm_application = np.linalg.norm(application_embedding)
        
        similarity_의사소통능력 = 200 * np.dot(application_embedding, 의사소통능력_embedding) / (norm_application * norm_의사소통능력)
        similarity_자원관리능력 = 200 * np.dot(application_embedding, 자원관리능력_embedding) / (norm_application * norm_자원관리능력)
        similarity_문제해결능력 = 200 * np.dot(application_embedding, 문제해결능력_embedding) / (norm_application * norm_문제해결능력)
        similarity_정보능력 = 200 * np.dot(application_embedding, 정보능력_embedding) / (norm_application * norm_정보능력)
        similarity_조직이해능력 = 200 * np.dot(application_embedding, 조직이해능력_embedding) / (norm_application * norm_조직이해능력)
        similarity_수리능력 = 200 * np.dot(application_embedding, 수리능력_embedding) / (norm_application * norm_수리능력)
        similarity_자기개발능력 = 200 * np.dot(application_embedding, 자기개발능력_embedding) / (norm_application * norm_자기개발능력)
        similarity_대인관계능력 = 200 * np.dot(application_embedding, 대인관계능력_embedding) / (norm_application * norm_대인관계능력)
        similarity_기술능력 = 200 * np.dot(application_embedding, 기술능력_embedding) / (norm_application * norm_기술능력)
        similarity_직업윤리 = 200 * np.dot(application_embedding, 직업윤리_embedding) / (norm_application * norm_직업윤리)
        
        similarity_list = [similarity_의사소통능력, similarity_자원관리능력, similarity_문제해결능력, similarity_정보능력, similarity_조직이해능력, similarity_수리능력, similarity_자기개발능력, similarity_대인관계능력, similarity_기술능력, similarity_직업윤리]
        
        integer_list = [int(num) for num in similarity_list]
        
        labels = np.array(["communicating ability", "resource management ability", "problem solving ability", "information ability", "organizational understanding ability", "mathematical ability", "self-development ability", "interpersonal ability", "technical ability", "career ethics"])
        stats = np.array(similarity_list)
        num_vars = len(labels)
        
        angles = np.linspace(0, 2*np.pi, num_vars, endpoint=False).tolist()
        stats = np.concatenate((stats, [stats[0]]))
        angles += angles[:1]
        
        fig_applicant, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.fill(angles, stats, color="red", alpha=0.25)
        ax.plot(angles, stats, color="red", linewidth=2)
        
        ax.set_ylim(0,100)
        ax.set_yticklabels([])
        ax.set_xticklabels([labels])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        
        ax_p.set_title("Score of applicant", fontsize=14, fontweight='bold', color='blue', position=(0.5, 1.1))
        
        st.session_state.messages.append({"role": "assistant", "content": st.pyplot(fig_applicant)})
        
        with st.chat_message("assistant"):
            st.markdown(f"문제해결능력 : {int(similarity_문제해결능력)}, 의사소통능력 : {int(similarity_의사소통능력)}, 조직이해능력 : {int(similarity_조직이해능력)}, 자원관리능력 : {int(similarity_자원관리능력)}, 정보능력 : {int(similarity_정보능력)}, 수리능력 : {int(similarity_수리능력)}, 대인관계능력 : {int(similarity_대인관계능력)}, 기술능력 : {int(similarity_기술능력)}, 직업윤리 : {int(similarity_직업윤리)}, 자기개발능력 : {int(similarity_자기개발능력)}")
        

        stats_P = np.array(similarity_list_P)
        stats_P = np.concatenate((stats_P, [stats_P[0]]))
        angles = np.linspace(0, 2*np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]
        
        fig_passer, ax_p = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax_p.fill(angles, stats_P, color="red", alpha=0.25)
        ax_p.plot(angles, stats_P, color="red", linewidth=2)
        
        ax_p.set_ylim(0,100)
        ax_p.set_yticklabels([])
        ax_p.set_xticklabels([labels])
        ax_p.set_xticks(angles[:-1])
        ax_p.set_xticklabels(labels)
        
        ax_p.set_title("Score of passer", fontsize=14, fontweight='bold', color='blue', position=(0.5, 1.1))
        
        st.session_state.messages.append({"role": "assistant", "content": st.pyplot(fig_passer)})
        
        with st.chat_message("assistant"):
            st.markdown(f"문제해결능력 : {int(similarity_문제해결능력_P)}, 의사소통능력 : {int(similarity_의사소통능력_P)}, 조직이해능력 : {int(similarity_조직이해능력_P)}, 자원관리능력 : {int(similarity_자원관리능력_P)}, 정보능력 : {int(similarity_정보능력_P)}, 수리능력 : {int(similarity_수리능력_P)}, 대인관계능력 : {int(similarity_대인관계능력_P)}, 기술능력 : {int(similarity_기술능력_P)}, 직업윤리 : {int(similarity_직업윤리_P)}, 자기개발능력 : {int(similarity_자기개발능력_P)}")
    
        for i in range(0, 9):
            if similarity_list[i] < 50:
                st.session_state.messages.append({"role": "assistant", "content":f"""{labels[i]}수준 : 하
                                해당 영역의 NCS 가이드북의 기본, 보충, 심화 부분에 대한 학습을 통해 교육시키는 것을 추천함."""})
                with st.chat_message("assistant"):
                    st.markdown(f"""{labels[i]}수준 : 하
                                해당 영역의 NCS 가이드북의 기본, 보충, 심화 부분에 대한 학습을 통해 교육시키는 것을 추천함.""")
            if 50 <= similarity_list[i] < 80:
                st.session_state.messages.append({"role": "assistant", "content":f"""{labels[i]}수준 : 하
                                해당 영역의 NCS 가이드북의 기본,  심화 부분에 대한 학습을 통해 교육시키는 것을 추천함."""})
                with st.chat_message("assistant"):
                    st.markdown(f"""{label[i]}수준 : 중
                                해당 영역의 NCS 가이드북의 기본, 심화 부분에 대한 학습을 통해 교육시키는 것을 추천함""")
            if similarity_list >= 80:
                st.session_state.messages.append({"role": "assistant", "content":f"""{labels[i]}수준 : 하
                                해당 영역의 NCS 가이드북의 심화 부분에 대한 학습을 추천하며, 실무 중 부족한 부분이 드러날 경우 추가적 학습을 시키는 것을 추천함"""})
                with st.chat_message("assistant"):
                    st.markdown(f"""{label[i]}수준 : 상
                                해당 영역의 NCS 가이드북의 심화 부분에 대한 학습을 추천하며, 실무 중 부족한 부분이 드러날 경우 추가적 학습을 시키는 것을 추천함""")
    
if option == "부서별 적합도":
    RCS_text = """① 금융회사 계량리스크 관리(Financial Risk Management) Consulting
    - 신용/시장/보험리스크 관리체계 및 방법론 수립
    - ESG 리스크 관리체계 및 방법론 수립, 투자회사 ESG 실사 업무
    - 일반기업 및 금융기관 파생상품 공정가치평가
    - 기타 규제대응 체계(바젤, KICS,IFRS9/17 등 금융기관 재무회계 규제 대응 등)
    ② 금융회사 비계량리스크 관리(Non-Financial Risk Management) 및
    Compliance Consulting
    - 운영리스크 관리(Operational Risk Management)
    - 금융회사(지주) 내부통제 진단 및 개선 (Internal Control improvement)
    - 금융기관 자금세탁방지(Anti-Money Laundering) 체계 수립
    - 기타 규제 및 컴플라이언스 준수를 위한 준법/내부감사 프로그램 수립 등
    ③ 포렌식 컨설팅 서비스(Forensic Investigation, Advisory, Technology
    Services)
    - 회계부정 조사
    - 횡령 등 부정 조사
    - 반독점 등 규제준수 조사
    - 반부패, 전략물자관리등 비금융 및 금융 관련 준법자문업무
    - 부정위험관리 자문업무
    - 포렌식 Tech 자문업무
"""

    MCS_1_text = """
    1. 금융 전략
    - 금융사 비전 전략 수립, 성장 전략. 신사업 전략
    - Operation 전략. 고객 마케팅 실행 전략 수립, 채널전략, 해외진출 전략
    2. Financial Management
    - 경영계획-손익관리-성과관리 체계 수립
    - 금융 규제 대응(금리 Pricing, 규제비율 등)
    - 38 PI (Process Innovation)
    - ALM (금리 및 유동성리스크 관리)
    ③ Technology 기반 프로세스 혁신 (은행/카드/보험/Payment 등 금융 및 공공부문)
    - 디지털 기술 기반 전환 체계 수립 컨설팅 (Cloud, Aaile, Data platform, Analtics)
    - 데이터 플랫퐁 전략, 설계 및 데이터 Governance
    - 디지털 기술 기반 업무 프로세스 혁신
    - 모바일 등 디지털 채널 프로세스 개선 및 아키텍쳐 컨설팅
    - 데이터 기반 마케팅 플랫폼 전략 및 설계
    4. IT 전략, 거버넌스 수립 컨설팅
    - 정보화 전략계획 수림 (ISP), 아키텍처 전화/설계 컨설팅 (클라우드, MSA. OSS 등)
    - IT거버넌스 및 조직 운영모델 수립 컨설팅
    ⑤ IT 실행 지원 서비스
    - 대형 프로젯트 리스크 관리 및 사전 수행 전략 수립 (PMO)
    - IT 통합, 글로벌 금융사 차세대 구축 프로젝트 컨설팅 (BMO)
    """
    
    MCS_2_text = """
    1. Management Consulting (DT, PI, IT 컨설팅)
    - 제조 및 주요 서비스업 고객 대상 R&D, 영업/마케팅, SCM. 생산, 구매.
    물류부문 경영혁신전략 및 PI 컨설팅
    - Digital Transformation 및 IT 전략 실행방안 수립 컨설팅
    - 클라우드, OpenAI 기반 전략컨설팅
    ② 회계/재무/경영관리 컨설팅
    - 재무회계, 관리회계, 경영계획, 성과관리, 연결회계 프로세스 및 시스템 구축
    - 빌링/정산, Accounting Hub 프로세스 설계 및 시스템구축 컨설팅
    ③ 기업의 ERP 도입 전략, 설계 및 구축 컨설팅
    - SAP기반 PI 및 DT 컨설팅
    - SAP S4HANA ERP 설계 및 구축 컨설팅
    - Microsoft 기반 ERP, Cloud. DT 컨설팅
    """
    
    MCS_3_text = """
    ① Operations Strategy & Process Innovation 컨설팅
    - 제조/유통/서비스업 기업 대상 Value Chain 전반 경영 혁신
    - 재무/원가, R&D. 영업/마케팅, SCM (S80P), 생산/제조, 구매, 물류 혁신
    ② Digital Transformation 컨설팅
    - Dicital 신기술 (Al, Hyper Automation 등) 기반 경영 혁신
    ③ M&A 및 사모펀드 투자 기업 대상 경영 혁신 컨설팅
    - CDD / ITDD / PMI/ Turn Around 전략 수립 및 실행
    4. Enterprise Solution 구축 컨설팅
    - SAP ERP / Solution 및 물류 시스템 (WMS/OMS/TMS) 구축 
    5.글로벌 통상 전략 컨설팅
    - 수입규제 (반덤핑/상계관게/세이프가드) 조사 대응
    - 수입 규제 제도 활용 및 기업가치 극대화 전략
    - ESG 통상 자문 (탄소국경조정 등) 및 기타 수출입규제 대응 전략 등
    """
    
    MCS_4_text = """
    1. Technology 컨설팅
    - IT 중장기 전략 및 Digital 전환 계획 수립 (ISP/MP)
    - 프로세스 혁신을 통한 일하는 방식의 변화관리 수행 (Pl)
    - 차세대 ERP 구축을 위한 추진방안 수립 (SAP ERP)
    - Operation을 위한 IT시스템(ERP, SCM 등) 구축
    - 데이터 관리 및 품질 시스템(MDM/DOM) 구축
    ② Digital 컨설팅
    - 데이터 분석 기반 마케팅 고도화 전략 수립
    - ESG 데이터 관리를 위한 ESG Data Hub 구축
    - 스마트팩토리 등 제조 DT 시스템 구축
    - 시장/고객/채널 Market Trend / Insight 및 전사 전략방향 제시
    """
    
    RCS_embedding = of.get_embedding(RCS_text)
    MCS1_embedding = of.get_embedding(MCS_1_text)
    MCS2_embedding = of.get_embedding(MCS_2_text)
    MCS3_embedding = of.get_embedding(MCS_3_text)
    MCS4_embedding = of.get_embedding(MCS_4_text)
    
    norm_RCS = np.linalg.norm(RCS_embedding)
    norm_MCS1 = np.linalg.norm(MCS1_embedding)
    norm_MCS2 = np.linalg.norm(MCS2_embedding)
    norm_MCS3 = np.linalg.norm(MCS3_embedding)
    norm_MCS4 = np.linalg.norm(MCS4_embedding)
    
    prompt = st.chat_input("submit application form here.")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        thread = client.beta.threads.create()
        run = of.complete_run(of.create_run(activity_grader_id, thread, prompt), thread)
        model_response = of.get_response(thread)
        
        full_model_response = ""
        
        for i in range(1, len(model_response.data)):
            full_model_response += model_response.data[i].content[0].text.value
        
        application_embedding = of.get_embedding(full_model_response)
        norm_application = np.linalg.norm(application_embedding)
        
        similarity_RCS = 180 * np.dot(application_embedding, RCS_embedding) / (norm_application * norm_RCS)
        similarity_MCS1 = 180 * np.dot(application_embedding, MCS1_embedding) / (norm_application * norm_MCS1)
        similarity_MCS2 = 180 * np.dot(application_embedding, MCS2_embedding) / (norm_application * norm_MCS2)
        similarity_MCS3 = 180 * np.dot(application_embedding, MCS3_embedding) / (norm_application * norm_MCS3)
        similarity_MCS4 = 180 * np.dot(application_embedding, MCS4_embedding) / (norm_application * norm_MCS4)
        
        similarity_list = [similarity_RCS, similarity_MCS1, similarity_MCS2, similarity_MCS3, similarity_MCS4]
        integer_list = [int(num) for num in similarity_list]
        
        data = pd.DataFrame({
            '직무 적합도': similarity_list
        }, index=["RCS", "MCS1", "MCS2", "MCS3", "MCS4"]
        )
        
        st.session_state.messages.append({"role": "assistant", "content": st.bar_chart(data)})

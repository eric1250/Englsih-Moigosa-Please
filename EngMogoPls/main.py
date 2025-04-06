import streamlit as st
from google import genai
from google.genai import types
from testmake import test_make
st.set_page_config('English moigosa pls')



geminiModels = ["gemini-2.0-flash"]
type_list = ['글의 목적', '필자의 주장','밑줄의 의미', '글의 요지', '글의 주제', '글의 제목', '어법', '낱말의 쓰임', '빈칸 추론', '흐름', '순서', '문장 삽입', '요약']

    
def main():
    st.title('영어 모의고사 만들기!')
    
    with st.expander("English Moigosa Please에 대하여", expanded=False):
        st.write(
        """     
        - gemini를 활용함
        - streamlit을 이용해 페이지 구상함
        - 원하는 문제 유형을 선택 후 영어 지문을 보내 보세요.
        - 지문이 너무 짧거나 내용이 이상할 경우 잘 안먹힐수 있습니다.
        - ai가 잘못된 문제를 낼 수도 있어요 조심!
        """
        )
    
    with st.sidebar:
        api_key = st.text_input(label="API 키", placeholder="Enter Your API Key", value="", type="password")

        st.markdown("---")
        
        model = st.radio(label="ai 모델", options=geminiModels)
        if model in geminiModels and api_key:
            client = genai.Client(api_key=api_key)
        
        test_types = st.multiselect(label='유형', options=type_list)
        st.markdown("---")

        if st.button(label="초기화"):
            st.session_state["chat"] = []
            model = []
            st.session_state["check_reset"] = True

    engtext = st.chat_input('영어 지문을 입력해주세요.')
    
    if engtext:
        if model in geminiModels:
            test_make(engtext, test_types, client, model)



if __name__ == '__main__':
    main()

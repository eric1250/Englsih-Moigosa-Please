import streamlit as st
from google import genai
from google.genai import types
from testmake import test_make
st.set_page_config('English moigosa pls')

system_instruction = '''
너는 사용자가 영어 지문을 주면 유형에 맞게 한국 영어 모의고사 문제를 만드는 ai야.
만약 사용자가 준 영어 지문이 문제를 만들기에 부적절하다고 생각하면 그 이유를 말해줘.
입력된 질문에 맞는 문제를 만들어줘.
한국어선지라고 하면 한국어로 선지를 만들고 영어선지라고 하면 영어로 선지를 만들어줘.
선지는 5개고 한 선지마다 줄을 바꿔서 보여줘.
지문은 영어로 주고 질문은 한국어로 써줘.
답지는 맨 아래에 올려줘.
'''

def generate_exam(client:genai.Client, model, question, seunji_lang, engtext):
    return client.models.generate_content(
        model=model,
        config=types.GenerateContentConfig(system_instruction=system_instruction),
        contents=question + seunji_lang + engtext
    ).text


def test_make(engtext, type_list, client:genai.Client, model):
    exams = ''
    for test_type in type_list:
        seunji_lang = '영어선지'
        
        if test_type == '글의 목적':
            question = '다음 글의 목적으로 가장 적절한 것은?'
            seunji_lang = '한국어선지'
            exams += generate_exam(client, model, question, seunji_lang, engtext) +'\n'
        
        if test_type == '필자의 주장':
            question = '다음 글에서 필자가 주장하는 바로 가장 적절한 것은?'
            seunji_lang = '한국어선지'
            exams += generate_exam(client, model, question, seunji_lang, engtext) +'\n'
        
        if test_type == '밑줄의 의미':
            question = '밑줄 친 부분이 다음 글에서 의미하는 바로 가장 적절한 것은?'
            exams += generate_exam(client, model, question, seunji_lang, engtext) +'\n'
        
        if test_type == '글의 요지':
            question = '다음 글의 요지로 가장 적절한 것은?'
            seunji_lang = '한국어선지'
            exams += generate_exam(client, model, question, seunji_lang, engtext) +'\n'
        
        if test_type == '글의 주제':
            question = '다음 글의 주제로 가장 적절한 것은?'
            exams += generate_exam(client, model, question, seunji_lang, engtext) +'\n'
            
        if test_type == '글의 제목':
            question = '다음 글의 제목으로 가장 적절한 것은?'
            exams += generate_exam(client, model, question, seunji_lang, engtext) +'\n'
        
        if test_type == '어법':
            question = '다음 글의 밑줄 친 부분 중, 어법상 틀린 것은?'
            exams += generate_exam(client, model, question, seunji_lang, engtext) +'\n'
            
        if test_type == '낱말의 쓰임':
            question = '다음 글의 밑줄 친 부분 중, 문맥상 낱말의 쓰임이 적절하지 않은 것은?'
            exams += generate_exam(client, model, question, seunji_lang, engtext) +'\n'
        
        if test_type == '빈칸 추론':
            question = ' 다음 빈칸에 들어갈 말로 가장 적절한 것을 고르시오.'
            exams += generate_exam(client, model, question, seunji_lang, engtext) +'\n'
            
        if test_type == '흐름':
            question = '다음 글에서 전체 흐름과 관계 없는 문장은?'
            exams += generate_exam(client, model, question, seunji_lang, engtext) +'\n'
        
        if test_type == '순서':
            question = '주어진 글 다음에 이어질 글의 순서로 가장 적절한 것을 고르시오.'
            exams += generate_exam(client, model, question, seunji_lang, engtext) +'\n'
            
        if test_type == '문장 삽입':
            question = '글의 흐름으로 보아, 주어진 문장이 들어가기에 가장 적절한 곳을 고르시오.'
            exams += generate_exam(client, model, question, seunji_lang, engtext) +'\n'
            
        if test_type == '요약':
            question = '다음 글의 내용을 한 문장으로 요약하고자 한다. 빈칸 (A)와 (B)에 들어갈 말로 가장 적절한 것은?'
            exams += generate_exam(client, model, question, seunji_lang, engtext) +'\n'
            
        
        write(exams)


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

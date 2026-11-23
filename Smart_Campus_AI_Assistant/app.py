import streamlit as st
import pandas as pd
from pathlib import Path
from modules.analytics import load_students, class_summary
from modules.ml_model import train_model, predict_student
from modules.sentiment import analyze_feedback
from modules.chatbot import answer_question
from modules.rag import extract_pdf_text, retrieve_context
from modules.agent import create_study_plan

st.set_page_config(page_title="Smart Campus AI Assistant", page_icon="🎓", layout="wide")
st.title("🎓 Smart Campus AI Assistant")
st.caption("Data Science • Machine Learning • NLP • GenAI • RAG • Agentic AI")
df = load_students(Path("data/students.csv"))

page = st.sidebar.radio("Project modules", ["Overview","Student Analytics","Performance Prediction","Feedback Sentiment","AI Academic Chatbot","Chat with Study PDF","AI Study Plan Agent"])
if page == "Overview":
    a,b,c,d = st.columns(4)
    a.metric("Sample students",len(df)); b.metric("Average marks",f"{df.marks.mean():.1f}%")
    c.metric("Attendance",f"{df.attendance.mean():.1f}%"); d.metric("Courses",df.course.nunique())
    st.markdown("""
    This integrated project demonstrates:
    - **Data Science:** student data analysis and charts.
    - **Machine Learning:** Decision Tree performance category prediction.
    - **NLP:** feedback sentiment classification.
    - **GenAI:** Gemini academic chatbot (optional API key).
    - **RAG:** retrieve relevant passages from an uploaded PDF.
    - **Agentic AI:** tools analyse a student's progress and draft a study plan.
    """)
    st.info("Use fictional or anonymised data only. Predictions are educational demonstrations, not real academic decisions.")
    st.dataframe(df, use_container_width=True)
elif page == "Student Analytics":
    st.subheader("Student analytics")
    x,y = st.columns(2)
    x.bar_chart(df.groupby("course").marks.mean())
    y.scatter_chart(df,x="attendance",y="marks",color="course")
    st.dataframe(class_summary(df),use_container_width=True)
    st.download_button("Download sample CSV",df.to_csv(index=False),"students.csv","text/csv")
    up=st.file_uploader("Upload compatible CSV",type=["csv"])
    if up:
        try:
            custom=pd.read_csv(up)
            required={"student_id","course","marks","attendance","assignments"}
            if required.issubset(custom.columns):
                st.dataframe(class_summary(custom),use_container_width=True)
            else: st.error("Required columns: "+", ".join(sorted(required)))
        except Exception as e: st.error(str(e))
elif page == "Performance Prediction":
    model,acc,_=train_model(df)
    st.metric("Hold-out accuracy (small synthetic data)",f"{acc:.0%}")
    st.caption("This score is for classroom demonstration only.")
    with st.form("predict"):
        marks=st.slider("Previous marks",0,100,60)
        attendance=st.slider("Attendance %",0,100,75)
        assignments=st.slider("Assignments completed %",0,100,70)
        course=st.selectbox("Course",sorted(df.course.unique()))
        go=st.form_submit_button("Predict category")
    if go: st.success("Estimated category: "+predict_student(model,marks,attendance,assignments,course))
elif page == "Feedback Sentiment":
    msg=st.text_area("Student feedback","The Python practical sessions are useful and the examples are clear.")
    if st.button("Analyse"):
        label,score,note=analyze_feedback(msg)
        st.metric("Sentiment",label); st.write(f"Demo score: {score:.2f}"); st.caption(note)
elif page == "AI Academic Chatbot":
    q=st.text_area("Ask an academic question","Explain supervised machine learning with a simple example.")
    if st.button("Ask AI"):
        answer,src=answer_question(q); st.markdown(answer); st.caption(src)
elif page == "Chat with Study PDF":
    pdf=st.file_uploader("Upload a text-based PDF",type=["pdf"])
    q=st.text_input("Question about the PDF","Summarise the key ideas.")
    if pdf:
        try:
            doc=extract_pdf_text(pdf)
            if not doc.strip(): st.warning("No selectable text found. Scanned PDFs need OCR.")
            else:
                context=retrieve_context(doc,q)
                st.text_area("Retrieved passages",context,height=180)
                if st.button("Answer from PDF"):
                    ans,src=answer_question("Answer only from this context. If missing, say so.\n\n"+context+"\n\nQuestion: "+q)
                    st.markdown(ans); st.caption(src)
        except Exception as e: st.error(str(e))
else:
    sid=st.selectbox("Sample student",df.student_id.astype(str).tolist())
    goal=st.text_input("Learning goal","Improve Python and prepare for the next assessment")
    if st.button("Create study plan"):
        student=df[df.student_id.astype(str)==sid].iloc[0].to_dict()
        plan,log=create_study_plan(student,goal)
        st.markdown(plan)
        with st.expander("Agent tool-use trace"):
            for line in log: st.write("• "+line)

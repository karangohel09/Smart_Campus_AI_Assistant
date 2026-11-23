import pandas as pd
def load_students(path):
    df=pd.read_csv(path)
    required={"student_id","course","marks","attendance","assignments"}
    if not required.issubset(df.columns): raise ValueError(f"Missing columns: {required-set(df.columns)}")
    for c in ["marks","attendance","assignments"]:
        df[c]=pd.to_numeric(df[c],errors="coerce").fillna(0).clip(0,100)
    return df
def class_summary(df):
    return df.groupby("course",as_index=False).agg(students=("student_id","count"),average_marks=("marks","mean"),average_attendance=("attendance","mean"),average_assignments=("assignments","mean")).round(1)

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
def _label(r):
    s=.55*float(r.marks)+.25*float(r.attendance)+.20*float(r.assignments)
    return "Needs support" if s<45 else ("Developing" if s<65 else "On track")
def train_model(df):
    data=df.copy(); data["category"]=data.apply(_label,axis=1)
    X=data[["marks","attendance","assignments","course"]]; y=data.category
    prep=ColumnTransformer([("course",OneHotEncoder(handle_unknown="ignore"),["course"])],remainder="passthrough")
    model=Pipeline([("prep",prep),("tree",DecisionTreeClassifier(max_depth=4,random_state=42))])
    if len(data)>=8:
        Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,random_state=42,stratify=y)
        model.fit(Xtr,ytr); acc=accuracy_score(yte,model.predict(Xte))
    else: model.fit(X,y); acc=0
    model.fit(X,y)
    return model,acc,{}
def predict_student(model,marks,attendance,assignments,course):
    sample=pd.DataFrame([{"marks":marks,"attendance":attendance,"assignments":assignments,"course":course}])
    return model.predict(sample)[0]

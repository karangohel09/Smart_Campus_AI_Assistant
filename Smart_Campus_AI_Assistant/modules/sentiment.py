POS={"good","great","useful","excellent","clear","helpful","interesting","enjoy","love","easy","best"}
NEG={"bad","poor","slow","confusing","difficult","boring","waste","unclear","problem","worst"}
def analyze_feedback(text):
    words=[w.strip(".,!?;:()[]{}\\\"'").lower() for w in text.split()]
    p=sum(w in POS for w in words); n=sum(w in NEG for w in words)
    if p>n: return "Positive",min(.99,.55+(p-n)*.08),"Keyword-based demo; context and sarcasm may be missed."
    if n>p: return "Negative",min(.99,.55+(n-p)*.08),"Keyword-based demo; context and sarcasm may be missed."
    return "Neutral / unclear",.5,"No clear sentiment keywords detected."

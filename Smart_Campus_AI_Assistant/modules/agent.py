def create_study_plan(student,goal):
    # Explicit tool workflow: lookup -> analyse -> plan.
    profile={k:student[k] for k in ["student_id","course","marks","attendance","assignments"]}
    log=["Tool 1: lookup_student — retrieved the selected student's sample metrics."]
    issues=[]
    if float(profile["marks"])<50: issues.append("marks below 50%")
    if float(profile["attendance"])<75: issues.append("attendance below 75%")
    if float(profile["assignments"])<70: issues.append("assignment completion below 70%")
    log.append("Tool 2: analyse_progress — checked marks, attendance and assignments.")
    steps=[]
    if float(profile["marks"])<50: steps.append("Revise two recent topics and solve five guided questions daily.")
    else: steps.append("Maintain progress with one timed practice set every two days.")
    if float(profile["attendance"])<75: steps.append("Attend upcoming sessions and review notes for missed classes.")
    if float(profile["assignments"])<70: steps.append("Complete pending assignments in small daily tasks and request feedback.")
    steps.append("Take a weekly self-test and note topics that remain difficult.")
    plan=f"### Study plan for {profile['student_id']}\n\n**Goal:** {goal}\n\n**Course:** {profile['course']} | **Marks:** {profile['marks']}% | **Attendance:** {profile['attendance']}% | **Assignments:** {profile['assignments']}%\n\n**Areas to work on:** {', '.join(issues) if issues else 'No flags from the simple demo checks.'}\n\n**Recommended actions**\n"
    plan+="\n".join(f"{i+1}. {s}" for i,s in enumerate(steps))
    plan+="\n\nReview progress with a teacher after seven days. This is a learning suggestion, not an automated judgement."
    log.append("Planner: combined tool results into an explainable study plan.")
    return plan,log

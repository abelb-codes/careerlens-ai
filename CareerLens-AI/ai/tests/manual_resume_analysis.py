from ai.analyzer.analyzer import analyze_resume


resume = {
    "projects": [
        "CareerLens AI"
    ],

    "certifications": [
        "AWS Certified"
    ],

    "languages": [
        "English"
    ]
}


result = analyze_resume(resume)

print("\n===== CAREERLENS AI ANALYSIS =====")

print("Resume Score:", result["resume_score"])
print("ATS Score:", result["ats_score"])

print("\nStrengths:")
for item in result["strengths"]:
    print("-", item)

print("\nWeaknesses:")
for item in result["weaknesses"]:
    print("-", item)

print("\nSuggestions:")
for item in result["suggestions"]:
    print("-", item)
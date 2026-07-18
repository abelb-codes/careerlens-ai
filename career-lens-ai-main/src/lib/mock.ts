export const stats = [
  { label: "Resumes analyzed", value: "100+" },
  { label: "Enterprise teams", value: "10+" },
  { label: "Avg. time-to-shortlist", value: "3.2 min" },
  { label: "Bias reduction", value: "68%" },
];

export const features = [
  {
    icon: "Sparkles",
    title: "AI Resume Analysis",
    desc: "Deep parsing of skills, experience, and impact — with an explainable score, not a black box.",
  },
  {
    icon: "Target",
    title: "ATS Compatibility Score",
    desc: "Instant feedback on formatting, keywords, and structure that recruiter systems actually read.",
  },
  {
    icon: "Trophy",
    title: "Candidate Ranking",
    desc: "Semantic match against your job description. Ranked, weighted, and fully auditable.",
  },
  {
    icon: "MessageSquareText",
    title: "AI Interview Questions",
    desc: "Role-specific questions generated per candidate — behavioral, technical, and gap-focused.",
  },
  {
    icon: "ShieldCheck",
    title: "Bias-aware scoring",
    desc: "Transparent reasoning, entity extraction, and confidence intervals on every decision.",
  },
  {
    icon: "Workflow",
    title: "Evaluation Sessions",
    desc: "Upload a JD, drop 500 resumes, get a ranked shortlist with reasoning in under 5 minutes.",
  },
];

export const testimonials = [
  {
    quote:
      "We replaced three screening tools with CareerLens. Our recruiters ship shortlists the same day now.",
    name: "Priya Rao",
    role: "Head of Talent, Northwind",
  },
  {
    quote:
      "The reasoning panel is the killer feature. Every ranking is defensible in an audit.",
    name: "Marcus Weiss",
    role: "VP People, Kepler",
  },
  {
    quote:
      "My resume score jumped 34 points in one pass. I landed two interviews the same week.",
    name: "Sofia Alvarez",
    role: "Product Designer",
  },
];

export const faqs = [
  {
    q: "How does CareerLens rank candidates?",
    a: "We combine semantic similarity between the JD and each resume, weighted skill coverage, experience relevance, and ATS structure. Every score exposes its inputs.",
  },
  {
    q: "Is my resume data private?",
    a: "Resumes are encrypted at rest and never used to train third-party models. You control retention windows and deletion.",
  },
  {
    q: "Which file types are supported?",
    a: "PDF and DOCX up to 10MB. OCR handles scanned resumes automatically.",
  },
  {
    q: "Can I integrate my ATS?",
    a: "Yes — Greenhouse, Lever, Ashby and Workday via API. Custom webhooks on Enterprise.",
  },
];

export const pricing = [
  {
    name: "Applicant",
    price: "Free",
    period: "forever",
    desc: "For job seekers refining their resume.",
    features: [
      "5 resume analyses / month",
      "ATS compatibility score",
      "AI improvement suggestions",
      "Export PDF report",
    ],
    cta: "Analyze Resume",
    highlight: false,
  },
  {
    name: "Recruiter",
    price: "499 birr",
    period: "/ user / month",
    desc: "For hiring managers and small teams.",
    features: [
      "Unlimited resume screening",
      "Job description library",
      "Candidate ranking & leaderboards",
      "AI interview questions",
      "PDF & Excel exports",
    ],
    cta: "Start free trial",
    highlight: true,
  },
  {
    name: "Enterprise",
    price: "Custom",
    period: "",
    desc: "For large teams with compliance needs.",
    features: [
      "SSO / SAML",
      "ATS integrations",
      "Bias audits & reporting",
      "Dedicated CSM",
      "SOC 2, GDPR, DPA",
    ],
    cta: "Talk to sales",
    highlight: false,
  },
];

export const resumeHistory = [
  { id: "r-1042", name: "Abel_Bekele.pdf", date: "Oct 14, 2026", status: "Completed", ats: 92, match: 88 },
  { id: "r-1041", name: "Degaga_Emiru.pdf", date: "Oct 11, 2026", status: "Completed", ats: 84, match: 79 },
  { id: "r-1040", name: "Mock_data.docx", date: "Oct 04, 2026", status: "Completed", ats: 71, match: 66 },
  { id: "r-1039", name: "Tesfa.pdf", date: "Sep 28, 2026", status: "Completed", ats: 63, match: 58 },
  { id: "r-1038", name: "Mock_data2.pdf", date: "Sep 20, 2026", status: "Completed", ats: 52, match: 47 },
];

export const candidates = [
  { id: "c-01", name: "Abel_Bekele", role: "Senior Product Designer", ats: 96, match: 94, exp: "7y", edu: "MFA, RISD", rec: "Strong hire" },
  { id: "c-02", name: "Degaga_Emiru", role: "Product Designer", ats: 92, match: 91, exp: "6y", edu: "BFA, NID", rec: "Strong hire" },
  { id: "c-03", name: "Example1", role: "Senior UX Designer", ats: 89, match: 87, exp: "8y", edu: "MSc HCI, UCL", rec: "Hire" },
  { id: "c-04", name: "Example2", role: "Product Designer", ats: 84, match: 83, exp: "5y", edu: "BDes, Musashino", rec: "Hire" },
  { id: "c-05", name: "Tesfa", role: "Interaction Designer", ats: 81, match: 79, exp: "4y", edu: "BA, Central Saint Martins", rec: "Consider" },
  { id: "c-06", name: "Tesfa Michael", role: "Design Engineer", ats: 78, match: 76, exp: "6y", edu: "BSc CS, ITAM", rec: "Consider" },
  { id: "c-07", name: "Mock", role: "UX Researcher", ats: 74, match: 71, exp: "3y", edu: "MSc, KAIST", rec: "Consider" },
  { id: "c-08", name: "Mock2a", role: "Product Designer", ats: 68, match: 64, exp: "2y", edu: "BFA, USP", rec: "Weak" },
];

export const jobs = [
  { id: "j-101", title: "Senior Product Designer", team: "Design", applicants: 214, status: "Active", updated: "2d ago" },
  { id: "j-102", title: "Staff Frontend Engineer", team: "Engineering", applicants: 187, status: "Active", updated: "4h ago" },
  { id: "j-103", title: "Product Manager, Growth", team: "Product", applicants: 96, status: "Draft", updated: "1w ago" },
  { id: "j-104", title: "Data Scientist", team: "Data", applicants: 342, status: "Active", updated: "1d ago" },
  { id: "j-105", title: "Head of Marketing", team: "Marketing", applicants: 58, status: "Archived", updated: "3w ago" },
];

export const pipeline = [
  { stage: "Sourced", value: 1240 },
  { stage: "Screened", value: 640 },
  { stage: "AI Shortlist", value: 182 },
  { stage: "Interview", value: 54 },
  { stage: "Offer", value: 12 },
  { stage: "Hired", value: 8 },
];

export const skillRadar = [
  { skill: "React", A: 92 },
  { skill: "TypeScript", A: 88 },
  { skill: "System Design", A: 74 },
  { skill: "UX", A: 81 },
  { skill: "Testing", A: 65 },
  { skill: "Leadership", A: 70 },
];

export const applicationsTrend = [
  { day: "Mon", v: 42 }, { day: "Tue", v: 68 }, { day: "Wed", v: 91 },
  { day: "Thu", v: 74 }, { day: "Fri", v: 120 }, { day: "Sat", v: 55 }, { day: "Sun", v: 38 },
];
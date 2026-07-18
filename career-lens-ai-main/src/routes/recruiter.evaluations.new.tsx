import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { PageHeader } from "@/components/app/shell";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { CheckCircle2, Loader2, UploadCloud, ArrowRight, ArrowLeft, FileText, Sparkles } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";

export const Route = createFileRoute("/recruiter/evaluations/new")({
  head: () => ({ meta: [{ title: "New evaluation — CareerLens AI" }] }),
  component: NewEval,
});

const steps = ["Session", "Job Description", "Upload Resumes", "Run AI", "Results"];
const pipeline = [
  "Upload", "OCR", "Resume Parsing", "Skill Extraction", "Experience Extraction",
  "Keyword Matching", "Semantic Similarity", "ATS Analysis", "Ranking", "Interview Questions", "Final Report",
];

function NewEval() {
  const [step, setStep] = useState(0);
  const [progress, setProgress] = useState(0);
  const [runningIdx, setRunningIdx] = useState(0);
  const navigate = useNavigate();

  const runAi = () => {
    setStep(3);
    setProgress(0);
    setRunningIdx(0);
    const iv = setInterval(() => {
      setProgress((p) => {
        const next = p + 5;
        setRunningIdx(Math.min(pipeline.length - 1, Math.floor((next / 100) * pipeline.length)));
        if (next >= 100) { clearInterval(iv); setStep(4); toast.success("Evaluation complete"); return 100; }
        return next;
      });
    }, 200);
  };

  return (
    <div>
      <PageHeader eyebrow={`Step ${step + 1} of ${steps.length}`} title="Create evaluation session" description="A guided wizard to score & rank a batch of candidates." />

      <div className="mb-6">
        <div className="flex items-center gap-2">
          {steps.map((s, i) => (
            <div key={s} className="flex flex-1 items-center gap-2">
              <div className={`grid h-7 w-7 shrink-0 place-items-center rounded-full text-xs font-semibold ${
                i < step ? "bg-success/20 text-success" :
                i === step ? "bg-gradient-primary text-white shadow-glow" :
                "bg-secondary text-muted-foreground"
              }`}>{i < step ? <CheckCircle2 className="h-4 w-4" /> : i + 1}</div>
              <span className={`hidden text-xs sm:inline ${i === step ? "text-foreground" : "text-muted-foreground"}`}>{s}</span>
              {i < steps.length - 1 && <div className={`h-px flex-1 ${i < step ? "bg-success/40" : "bg-border"}`} />}
            </div>
          ))}
        </div>
      </div>

      <Card className="border-border/70 bg-gradient-card p-6">
        {step === 0 && (
          <div className="space-y-4">
            <div><Label>Session name</Label><Input defaultValue="Sr. Product Designer · Q4" className="mt-1.5" /></div>
            <div><Label>Description</Label><Textarea rows={3} defaultValue="Screening batch for Q4 hiring for the design team." className="mt-1.5" /></div>
          </div>
        )}
        {step === 1 && (
          <div className="space-y-4">
            <div><Label>Job title</Label><Input defaultValue="Senior Product Designer" className="mt-1.5" /></div>
            <div><Label>Job description</Label><Textarea rows={8} defaultValue="We're hiring a senior product designer..." className="mt-1.5" /></div>
          </div>
        )}
        {step === 2 && (
          <div>
            <div className="flex min-h-[240px] flex-col items-center justify-center rounded-xl border-2 border-dashed border-border bg-secondary/20 p-8 text-center">
              <div className="grid h-12 w-12 place-items-center rounded-2xl bg-gradient-primary shadow-glow"><UploadCloud className="h-5 w-5 text-white" /></div>
              <div className="mt-3 text-base font-semibold">Drop resumes here</div>
              <div className="text-xs text-muted-foreground">Up to 500 files · PDF or DOCX</div>
              <Button variant="outline" className="mt-4">Browse files</Button>
            </div>
            <div className="mt-4 grid gap-2 sm:grid-cols-2">
              {["Amelia_Chen.pdf", "Rahul_Menon.pdf", "Nora_Bakr.pdf", "Ken_Watanabe.docx"].map(n => (
                <div key={n} className="flex items-center gap-2 rounded-lg border border-border/60 bg-secondary/20 p-2.5">
                  <FileText className="h-4 w-4 text-primary" />
                  <span className="flex-1 truncate text-xs">{n}</span>
                  <Badge variant="secondary" className="text-[10px]">Ready</Badge>
                </div>
              ))}
            </div>
          </div>
        )}
        {step === 3 && (
          <div className="space-y-6">
            <div className="text-center">
              <div className="grid h-14 w-14 mx-auto place-items-center rounded-2xl bg-gradient-primary shadow-glow">
                <Sparkles className="h-6 w-6 animate-pulse text-white" />
              </div>
              <div className="mt-3 text-lg font-semibold">AI is evaluating 214 candidates...</div>
              <div className="text-xs text-muted-foreground">Real-time pipeline · estimated 3 min</div>
            </div>
            <Progress value={progress} className="h-1.5" />
            <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
              {pipeline.map((p, i) => {
                const state = i < runningIdx ? "done" : i === runningIdx ? "active" : "pending";
                return (
                  <div key={p} className={`flex items-center gap-2 rounded-lg border p-2.5 text-xs ${
                    state === "done" ? "border-success/30 bg-success/5 text-success" :
                    state === "active" ? "border-primary/40 bg-primary/5 text-foreground" :
                    "border-border/60 bg-secondary/20 text-muted-foreground"
                  }`}>
                    {state === "done" ? <CheckCircle2 className="h-3.5 w-3.5" /> :
                     state === "active" ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> :
                     <span className="h-3.5 w-3.5 rounded-full border border-current" />}
                    {p}
                  </div>
                );
              })}
            </div>
          </div>
        )}
        {step === 4 && (
          <div className="text-center">
            <div className="grid h-14 w-14 mx-auto place-items-center rounded-2xl bg-success/20 text-success"><CheckCircle2 className="h-6 w-6" /></div>
            <div className="mt-3 text-lg font-semibold">Evaluation complete</div>
            <p className="mt-1 text-sm text-muted-foreground">214 candidates ranked · 8 strong hires identified.</p>
            <div className="mt-6 flex justify-center gap-2">
              <Button variant="outline" onClick={() => navigate({ to: "/recruiter/evaluations" })}>Back to sessions</Button>
              <Button className="bg-gradient-primary text-white shadow-glow hover:opacity-90" onClick={() => navigate({ to: "/recruiter/evaluations/$id", params: { id: "eval_7f2" } })}>View leaderboard</Button>
            </div>
          </div>
        )}
      </Card>

      {step < 3 && (
        <div className="mt-4 flex justify-between">
          <Button variant="outline" disabled={step === 0} onClick={() => setStep(step - 1)}><ArrowLeft className="mr-1 h-4 w-4" />Back</Button>
          {step < 2 && <Button onClick={() => setStep(step + 1)}>Next<ArrowRight className="ml-1 h-4 w-4" /></Button>}
          {step === 2 && <Button className="bg-gradient-primary text-white shadow-glow hover:opacity-90" onClick={runAi}><Sparkles className="mr-1 h-4 w-4" />Run AI evaluation</Button>}
        </div>
      )}
    </div>
  );
}
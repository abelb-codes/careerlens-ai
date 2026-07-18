import { createFileRoute, Link } from "@tanstack/react-router";
import { PageHeader } from "@/components/app/shell";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Plus, ArrowUpRight, Workflow } from "lucide-react";

export const Route = createFileRoute("/recruiter/evaluations/")({
  head: () => ({ meta: [{ title: "Evaluation Sessions — CareerLens AI" }] }),
  component: Evaluations,
});

const sessions = [
  { id: "eval_7f2", job: "Senior Product Designer", cand: 214, status: "Completed", when: "2d ago" },
  { id: "eval_7f1", job: "Staff Frontend Engineer", cand: 187, status: "Running", when: "3h ago" },
  { id: "eval_7f0", job: "Data Scientist", cand: 342, status: "Running", when: "1h ago" },
  { id: "eval_6f9", job: "Product Manager, Growth", cand: 96, status: "Draft", when: "5d ago" },
];

function Evaluations() {
  return (
    <div>
      <PageHeader
        eyebrow="Sessions"
        title="Evaluation sessions"
        description="Upload a JD, drop resumes, get a ranked shortlist."
        actions={<Button asChild className="bg-gradient-primary text-white shadow-glow hover:opacity-90"><Link to="/recruiter/evaluations/new"><Plus className="mr-1 h-4 w-4" />New session</Link></Button>}
      />
      <div className="grid gap-3 md:grid-cols-2">
        {sessions.map((s) => (
          <Link key={s.id} to="/recruiter/evaluations/$id" params={{ id: s.id }}>
            <Card className="group border-border/70 bg-gradient-card p-5 transition hover:border-primary/40 hover:shadow-glow">
              <div className="flex items-start justify-between">
                <div>
                  <div className="text-xs font-mono text-muted-foreground">{s.id}</div>
                  <div className="mt-1 text-base font-semibold">{s.job}</div>
                  <div className="mt-1 text-xs text-muted-foreground">{s.cand} candidates · {s.when}</div>
                </div>
                <Badge className={
                  s.status === "Completed" ? "bg-success/15 text-success hover:bg-success/15" :
                  s.status === "Running" ? "bg-primary/15 text-primary hover:bg-primary/15" :
                  "bg-warning/15 text-warning hover:bg-warning/15"
                }>{s.status}</Badge>
              </div>
              <div className="mt-4 flex items-center gap-2 text-xs text-muted-foreground">
                <Workflow className="h-3.5 w-3.5" /> View leaderboard <ArrowUpRight className="ml-auto h-4 w-4 group-hover:text-foreground" />
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
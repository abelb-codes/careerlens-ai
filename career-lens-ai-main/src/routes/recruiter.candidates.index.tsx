import { createFileRoute, Link } from "@tanstack/react-router";
import { PageHeader } from "@/components/app/shell";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { candidates } from "@/lib/mock";
import { Search } from "lucide-react";

export const Route = createFileRoute("/recruiter/candidates/")({
  head: () => ({ meta: [{ title: "Candidates — CareerLens AI" }] }),
  component: CandidatesList,
});

function CandidatesList() {
  return (
    <div>
      <PageHeader eyebrow="People" title="Candidates" description="All candidates across active evaluations." />
      <div className="mb-4 relative max-w-md">
        <Search className="absolute left-2.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <Input placeholder="Search candidates..." className="h-9 bg-secondary/40 pl-8" />
      </div>
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {candidates.map((c) => (
          <Link key={c.id} to="/recruiter/candidates/$id" params={{ id: c.id }}>
            <Card className="group flex items-start gap-3 border-border/70 bg-gradient-card p-5 transition hover:border-primary/40 hover:shadow-glow">
              <div className="grid h-11 w-11 shrink-0 place-items-center rounded-full bg-gradient-primary text-sm font-semibold text-white">
                {c.name.split(" ").map(n => n[0]).join("")}
              </div>
              <div className="min-w-0 flex-1">
                <div className="truncate text-sm font-semibold">{c.name}</div>
                <div className="truncate text-xs text-muted-foreground">{c.role}</div>
                <div className="mt-3 flex flex-wrap gap-1.5">
                  <Badge className="bg-primary/15 text-primary hover:bg-primary/15">ATS {c.ats}</Badge>
                  <Badge className="bg-accent/15 text-accent hover:bg-accent/15">Match {c.match}%</Badge>
                </div>
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
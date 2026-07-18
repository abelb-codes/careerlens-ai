import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/app/shell";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Download, FileSpreadsheet, FileText, Users } from "lucide-react";

export const Route = createFileRoute("/recruiter/reports")({
  head: () => ({ meta: [{ title: "Reports — CareerLens AI" }] }),
  component: Reports,
});

function Reports() {
  const items = [
    { icon: FileText, title: "Session summary", desc: "Ranked leaderboard, AI reasoning, and top 10 shortlist.", type: "PDF" },
    { icon: FileSpreadsheet, title: "Candidate export", desc: "All candidates with scores, skills, and recommendations.", type: "Excel" },
    { icon: Users, title: "Comparison report", desc: "Side-by-side comparison of 2–5 candidates.", type: "PDF" },
  ];
  return (
    <div>
      <PageHeader eyebrow="Reports" title="Generate & export" description="Board-ready reports on any evaluation session." />
      <div className="grid gap-3 md:grid-cols-3">
        {items.map((it) => (
          <Card key={it.title} className="border-border/70 bg-gradient-card p-6">
            <div className="grid h-11 w-11 place-items-center rounded-xl bg-primary/10 text-primary ring-1 ring-primary/20"><it.icon className="h-5 w-5" /></div>
            <div className="mt-4 text-base font-semibold">{it.title}</div>
            <p className="mt-1 text-sm text-muted-foreground">{it.desc}</p>
            <Button className="mt-6 w-full" variant="outline"><Download className="mr-2 h-4 w-4" />Download {it.type}</Button>
          </Card>
        ))}
      </div>
    </div>
  );
}
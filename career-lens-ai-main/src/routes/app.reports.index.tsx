import { createFileRoute, Link } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { FileText, ArrowUpRight } from "lucide-react";
import api from "@/api/axios";
import { PageHeader } from "@/components/app/shell";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

type Resume = {
  id: string;
  filename: string;
  processing_status: "uploaded" | "processing" | "completed" | "failed";
  created_at: string;
};

export const Route = createFileRoute("/app/reports/")({
  head: () => ({ meta: [{ title: "Analysis Reports - CareerLens AI" }] }),
  component: Reports,
});

function Reports() {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    api
      .get<Resume[]>("/api/resumes/")
      .then(({ data }) => setResumes(data.filter((resume) => resume.processing_status === "completed")))
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <PageHeader
        eyebrow="Reports"
        title="AI analysis reports"
        description="Every resume gets a full report - scores, reasoning, and recommendations."
      />
      {loading ? (
        <div className="text-sm text-muted-foreground">Loading analysis reports...</div>
      ) : error ? (
        <div className="text-sm text-destructive">Could not load analysis reports. Please try again.</div>
      ) : resumes.length === 0 ? (
        <Card className="border-border/70 bg-gradient-card p-6 text-sm text-muted-foreground">
          No completed reports yet. Upload a resume to start an analysis.
        </Card>
      ) : (
        <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
          {resumes.map((resume) => (
            <Link key={resume.id} to="/app/reports/$id" params={{ id: resume.id }}>
              <Card className="group border-border/70 bg-gradient-card p-5 transition hover:border-primary/40 hover:shadow-glow">
                <div className="flex items-center justify-between">
                  <div className="grid h-9 w-9 place-items-center rounded-lg bg-primary/10 text-primary"><FileText className="h-4 w-4" /></div>
                  <ArrowUpRight className="h-4 w-4 text-muted-foreground transition group-hover:text-foreground" />
                </div>
                <div className="mt-4 truncate text-sm font-semibold">{resume.filename}</div>
                <div className="mt-1 text-xs text-muted-foreground">{new Date(resume.created_at).toLocaleDateString()}</div>
                <div className="mt-4 flex items-center gap-2">
                  <Badge className="bg-success/15 text-success hover:bg-success/15">Completed</Badge>
                </div>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}

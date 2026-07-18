import { createFileRoute, Link } from "@tanstack/react-router";
import { useEffect, useMemo, useState } from "react";
import { AlertCircle, ArrowUpRight, FileText, Upload as UploadIcon } from "lucide-react";
import api from "@/api/axios";
import { PageHeader, ScoreRing, StatCard } from "@/components/app/shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

type Resume = {
  id: string;
  filename: string;
  processing_status: "uploaded" | "processing" | "completed" | "failed";
  created_at: string;
};

type Analysis = {
  ats_score: number;
  quality_score: number;
  matching_score: number;
  suggestions: string[];
};

export const Route = createFileRoute("/app/")({
  component: AppDashboard,
});

function AppDashboard() {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [latestAnalysis, setLatestAnalysis] = useState<Analysis | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    let active = true;
    api
      .get<Resume[]>("/api/resumes/")
      .then(async ({ data }) => {
        if (!active) return;
        setResumes(data);
        const latestCompleted = data.find((resume) => resume.processing_status === "completed");
        if (latestCompleted) {
          const response = await api.get<Analysis>(`/api/analysis/${latestCompleted.id}/`);
          if (active) setLatestAnalysis(response.data);
        }
      })
      .catch(() => active && setError(true));
    return () => {
      active = false;
    };
  }, []);

  const completed = useMemo(
    () => resumes.filter((resume) => resume.processing_status === "completed"),
    [resumes],
  );
  const latest = resumes[0];
  const latestCompleted = completed[0];

  return (
    <div>
      <PageHeader
        eyebrow="Dashboard"
        title="Your resume insights"
        description="Upload a resume and track its AI analysis from one place."
        actions={
          <Button asChild className="bg-gradient-primary text-white shadow-glow hover:opacity-90">
            <Link to="/app/upload">
              <UploadIcon className="mr-2 h-4 w-4" />
              Upload resume
            </Link>
          </Button>
        }
      />

      {error && (
        <div className="mb-4 flex items-center gap-2 rounded-lg border border-destructive/30 bg-destructive/10 p-3 text-sm text-destructive">
          <AlertCircle className="h-4 w-4" />
          Could not load your dashboard. Please refresh and sign in again if needed.
        </div>
      )}

      <div className="grid gap-4 md:grid-cols-4">
        <StatCard label="Resumes uploaded" value={String(resumes.length)} hint="All time" />
        <StatCard
          label="Reports ready"
          value={String(completed.length)}
          hint="Completed analyses"
        />
        <StatCard
          label="Latest ATS score"
          value={latestAnalysis ? String(latestAnalysis.ats_score) : "—"}
          hint="Most recent completed report"
        />
        <StatCard
          label="Latest job match"
          value={latestAnalysis ? `${latestAnalysis.matching_score}%` : "—"}
          hint="Most recent completed report"
        />
      </div>

      {latestAnalysis && latestCompleted ? (
        <Card className="mt-6 border-border/70 bg-gradient-card p-6">
          <div className="grid gap-6 sm:grid-cols-[auto_1fr_auto] sm:items-center">
            <ScoreRing value={latestAnalysis.quality_score} size={112} label="Score" />
            <div>
              <div className="text-xs uppercase tracking-wider text-muted-foreground">
                Latest completed report
              </div>
              <div className="mt-1 text-lg font-semibold">{latestCompleted.filename}</div>
              <p className="mt-2 text-sm text-muted-foreground">
                ATS {latestAnalysis.ats_score} · Job match {latestAnalysis.matching_score}%
              </p>
            </div>
            <Button asChild variant="outline">
              <Link to="/app/reports/$id" params={{ id: latestCompleted.id }}>
                View report <ArrowUpRight className="ml-1 h-3.5 w-3.5" />
              </Link>
            </Button>
          </div>
        </Card>
      ) : (
        <Card className="mt-6 border-border/70 bg-gradient-card p-6 text-sm text-muted-foreground">
          {latest
            ? `Your latest upload, ${latest.filename}, is ${latest.processing_status}. The report will appear here when analysis is complete.`
            : "No resumes yet. Upload a PDF or DOCX to generate your first report."}
        </Card>
      )}

      <Card className="mt-6 border-border/70 bg-gradient-card p-6">
        <div className="mb-4 flex items-center justify-between">
          <div className="text-sm font-semibold">Recent uploads</div>
          <Button asChild variant="ghost" size="sm">
            <Link to="/app/history">View all</Link>
          </Button>
        </div>
        <div className="space-y-2">
          {resumes.slice(0, 5).map((resume) => (
            <div
              key={resume.id}
              className="flex items-center gap-3 rounded-lg border border-border/60 bg-secondary/20 p-3"
            >
              <FileText className="h-4 w-4 text-primary" />
              <div className="min-w-0 flex-1">
                <div className="truncate text-sm font-medium">{resume.filename}</div>
                <div className="text-xs text-muted-foreground">
                  {new Date(resume.created_at).toLocaleDateString()}
                </div>
              </div>
              <Badge variant="secondary">{resume.processing_status}</Badge>
            </div>
          ))}
          {!resumes.length && !error && (
            <div className="text-sm text-muted-foreground">
              Loading uploads, or no resumes have been uploaded yet.
            </div>
          )}
        </div>
      </Card>
    </div>
  );
}

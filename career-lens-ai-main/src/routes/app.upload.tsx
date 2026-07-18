import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { PageHeader } from "@/components/app/shell";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { UploadCloud, FileText, CheckCircle2, Loader2, X } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";
import api from "@/api/axios";

export const Route = createFileRoute("/app/upload")({
  head: () => ({ meta: [{ title: "Upload Resume — CareerLens AI" }] }),
  component: Upload,
});

const pipeline = ["Uploaded", "Extracting text", "Analyzing", "Generating report", "Completed"];

function Upload() {
  const navigate = useNavigate();
  const [file, setFile] = useState<string | null>(null);
  const [progress, setProgress] = useState(0);
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);

  const start = async (selectedFile: File) => {
    if (!selectedFile) return;

    setUploading(true);
    setFile(selectedFile.name);
    setProgress(10);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const { data } = await api.post("/api/resumes/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setProgress(100);
      toast.success(`Uploaded ${data.filename}`);
      navigate({ to: "/app/history" });
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : "Upload failed";
      toast.error(message);
      setProgress(0);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <PageHeader eyebrow="Upload" title="Analyze a resume" description="Drop a PDF or DOCX. We'll parse, score, and generate your report." />
      <div className="grid gap-4 lg:grid-cols-[1.4fr_1fr]">
        <Card
          onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
          onDragLeave={() => setDragging(false)}
          onDrop={(e) => { e.preventDefault(); setDragging(false); const selected = e.dataTransfer.files[0]; if (selected) void start(selected); }}
          className={`relative flex min-h-[320px] flex-col items-center justify-center border-2 border-dashed p-10 text-center transition ${dragging ? "border-primary bg-primary/5" : "border-border bg-secondary/20"}`}
        >
          <div className="grid h-14 w-14 place-items-center rounded-2xl bg-gradient-primary shadow-glow">
            <UploadCloud className="h-6 w-6 text-white" />
          </div>
          <div className="mt-4 text-lg font-semibold">Drop your resume here</div>
          <div className="mt-1 text-sm text-muted-foreground">PDF or DOCX up to 10MB</div>
          <div className="mt-5">
            <label className="cursor-pointer">
              <input type="file" accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document" className="hidden" onChange={(e) => { const f = e.target.files?.[0]; if (f) void start(f); }} />
              <span className="inline-flex h-9 items-center rounded-md bg-primary px-4 text-sm font-medium text-primary-foreground shadow-glow hover:opacity-90">Browse files</span>
            </label>
          </div>
          <div className="mt-5 text-xs text-muted-foreground">Files are encrypted at rest · GDPR compliant</div>
        </Card>

        <Card className="border-border/70 bg-gradient-card p-6">
          <div className="text-sm font-semibold">AI processing pipeline</div>
          <div className="mt-4 space-y-3">
            {pipeline.map((label, i) => {
              const status = !file ? "pending" : uploading ? (i < 2 ? "done" : i === 2 ? "active" : "pending") : "done";
              return (
              <div key={label} className="flex items-center gap-3">
                <div className={`grid h-6 w-6 place-items-center rounded-full text-xs ${
                  status === "done" ? "bg-success/20 text-success" :
                  status === "active" ? "bg-primary/20 text-primary" : "bg-secondary text-muted-foreground"
                }`}>
                  {status === "done" ? <CheckCircle2 className="h-3.5 w-3.5" /> :
                   status === "active" ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : (i + 1)}
                </div>
                <span className={`text-sm ${status === "pending" ? "text-muted-foreground" : ""}`}>{label}</span>
                {status === "active" && <Badge variant="secondary" className="ml-auto text-[10px]">In progress</Badge>}
              </div>
            )})}
          </div>
        </Card>
      </div>

      {file && (
        <Card className="mt-4 border-border/70 bg-gradient-card p-5">
          <div className="flex items-center gap-3">
            <div className="grid h-10 w-10 place-items-center rounded-lg bg-primary/10 text-primary"><FileText className="h-4 w-4" /></div>
            <div className="min-w-0 flex-1">
              <div className="truncate text-sm font-medium">{file}</div>
              <div className="mt-1 flex items-center gap-2">
                <Progress value={progress} className="h-1.5 flex-1" />
                <span className="text-xs tabular-nums text-muted-foreground">{progress}%</span>
              </div>
            </div>
            <Button size="icon" variant="ghost" onClick={() => { setFile(null); setProgress(0); }}><X className="h-4 w-4" /></Button>
          </div>
        </Card>
      )}

      <div className="mt-8">
        <div className="mb-3 text-sm font-semibold">Recent uploads</div>
        <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
          {["Sofia_v3.pdf", "Design_2026.docx", "PortfolioResume.pdf"].map((n) => (
            <Card key={n} className="flex items-center gap-3 border-border/70 bg-gradient-card p-3">
              <div className="grid h-8 w-8 place-items-center rounded-md bg-secondary"><FileText className="h-4 w-4 text-muted-foreground" /></div>
              <div className="flex-1 truncate text-sm">{n}</div>
              <Badge variant="secondary" className="text-[10px]">Ready</Badge>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}

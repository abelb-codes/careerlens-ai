import { createFileRoute, Link } from "@tanstack/react-router";
import { PageHeader } from "@/components/app/shell";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Search, Filter, ArrowUpRight, Download } from "lucide-react";
import { useEffect, useState } from "react";
import api from "@/api/axios";

type Resume = {
  id: string;
  filename: string;
  processing_status: "uploaded" | "processing" | "completed" | "failed";
  created_at: string;
};

export const Route = createFileRoute("/app/history")({
  head: () => ({ meta: [{ title: "Resume History — CareerLens AI" }] }),
  component: History,
});

function History() {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get<Resume[]>("/api/resumes/")
      .then(({ data }) => setResumes(data))
      .finally(() => setLoading(false));
  }, []);

  const statusStyle: Record<Resume["processing_status"], string> = {
    uploaded: "bg-secondary text-muted-foreground hover:bg-secondary",
    processing: "bg-primary/15 text-primary hover:bg-primary/15",
    completed: "bg-success/15 text-success hover:bg-success/15",
    failed: "bg-destructive/15 text-destructive hover:bg-destructive/15",
  };

  return (
    <div>
      <PageHeader eyebrow="History" title="All your resume analyses" description="Search, filter, and revisit past reports." />
      <Card className="border-border/70 bg-gradient-card p-4">
        <div className="mb-4 flex flex-wrap items-center gap-2">
          <div className="relative min-w-[220px] flex-1">
            <Search className="absolute left-2.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input placeholder="Search by filename" className="h-9 bg-secondary/40 pl-8" />
          </div>
          <Select defaultValue="all">
            <SelectTrigger className="h-9 w-[140px] bg-secondary/40"><SelectValue /></SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All status</SelectItem>
              <SelectItem value="done">Completed</SelectItem>
              <SelectItem value="proc">Processing</SelectItem>
            </SelectContent>
          </Select>
          <Select defaultValue="new">
            <SelectTrigger className="h-9 w-[140px] bg-secondary/40"><SelectValue /></SelectTrigger>
            <SelectContent>
              <SelectItem value="new">Newest</SelectItem>
              <SelectItem value="old">Oldest</SelectItem>
              <SelectItem value="score">By score</SelectItem>
            </SelectContent>
          </Select>
          <Button variant="outline" size="sm" className="h-9"><Filter className="mr-1.5 h-3.5 w-3.5" />More filters</Button>
        </div>
        <div className="overflow-hidden rounded-lg border border-border/60">
          <Table>
            <TableHeader>
              <TableRow className="border-border/60 bg-secondary/40 hover:bg-secondary/40">
                <TableHead>Resume</TableHead>
                <TableHead>Uploaded</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">ATS</TableHead>
                <TableHead className="text-right">Match</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {loading ? (
                <TableRow><TableCell colSpan={6} className="py-8 text-center text-muted-foreground">Loading resumes…</TableCell></TableRow>
              ) : resumes.length === 0 ? (
                <TableRow><TableCell colSpan={6} className="py-8 text-center text-muted-foreground">No resumes uploaded yet.</TableCell></TableRow>
              ) : resumes.map((r) => (
                <TableRow key={r.id} className="border-border/60">
                  <TableCell className="font-medium">{r.filename}</TableCell>
                  <TableCell className="text-muted-foreground">{new Date(r.created_at).toLocaleDateString()}</TableCell>
                  <TableCell><Badge className={statusStyle[r.processing_status]}>{r.processing_status}</Badge></TableCell>
                  <TableCell className="text-right tabular-nums">—</TableCell>
                  <TableCell className="text-right tabular-nums">—</TableCell>
                  <TableCell className="text-right">
                    <div className="flex justify-end gap-1">
                      <Button asChild variant="ghost" size="sm" disabled={r.processing_status !== "completed"}><Link to="/app/reports/$id" params={{ id: r.id }}>View <ArrowUpRight className="ml-1 h-3.5 w-3.5" /></Link></Button>
                      <Button variant="ghost" size="icon" disabled><Download className="h-3.5 w-3.5" /></Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
        <div className="mt-3 flex items-center justify-between text-xs text-muted-foreground">
          <span>Showing {resumes.length} resume{resumes.length === 1 ? "" : "s"}</span>
          <div className="flex gap-1">
            <Button variant="outline" size="sm" className="h-7">Previous</Button>
            <Button variant="outline" size="sm" className="h-7">Next</Button>
          </div>
        </div>
      </Card>
    </div>
  );
}

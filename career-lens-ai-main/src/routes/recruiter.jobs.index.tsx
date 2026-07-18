import { createFileRoute, Link } from "@tanstack/react-router";
import { PageHeader } from "@/components/app/shell";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { jobs } from "@/lib/mock";
import { Search, Plus, MoreHorizontal } from "lucide-react";

export const Route = createFileRoute("/recruiter/jobs/")({
  head: () => ({ meta: [{ title: "Job Descriptions — CareerLens AI" }] }),
  component: JobsList,
});

function JobsList() {
  return (
    <div>
      <PageHeader
        eyebrow="Roles"
        title="Job descriptions"
        description="Create, edit, and archive job posts. Each job is scored against candidates automatically."
        actions={<Button asChild className="bg-gradient-primary text-white shadow-glow hover:opacity-90"><Link to="/recruiter/jobs/new"><Plus className="mr-1 h-4 w-4" />Create job</Link></Button>}
      />
      <Card className="border-border/70 bg-gradient-card p-4">
        <div className="relative mb-4 max-w-sm">
          <Search className="absolute left-2.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input placeholder="Search jobs..." className="h-9 bg-secondary/40 pl-8" />
        </div>
        <div className="overflow-hidden rounded-lg border border-border/60">
          <Table>
            <TableHeader>
              <TableRow className="border-border/60 bg-secondary/40 hover:bg-secondary/40">
                <TableHead>Job title</TableHead>
                <TableHead>Team</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Applicants</TableHead>
                <TableHead>Updated</TableHead>
                <TableHead></TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {jobs.map((j) => (
                <TableRow key={j.id} className="border-border/60">
                  <TableCell className="font-medium">{j.title}</TableCell>
                  <TableCell className="text-muted-foreground">{j.team}</TableCell>
                  <TableCell>
                    <Badge className={
                      j.status === "Active" ? "bg-success/15 text-success hover:bg-success/15" :
                      j.status === "Draft" ? "bg-warning/15 text-warning hover:bg-warning/15" :
                      "bg-muted text-muted-foreground"
                    }>{j.status}</Badge>
                  </TableCell>
                  <TableCell className="text-right tabular-nums">{j.applicants}</TableCell>
                  <TableCell className="text-muted-foreground">{j.updated}</TableCell>
                  <TableCell className="text-right"><Button variant="ghost" size="icon"><MoreHorizontal className="h-4 w-4" /></Button></TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </Card>
    </div>
  );
}
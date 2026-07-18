import { createFileRoute, Link } from "@tanstack/react-router";
import { PageHeader } from "@/components/app/shell";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { candidates } from "@/lib/mock";
import { Search, Download, Filter, ArrowUpRight, Trophy } from "lucide-react";

export const Route = createFileRoute("/recruiter/evaluations/$id")({
  head: () => ({ meta: [{ title: "Leaderboard — CareerLens AI" }] }),
  component: Results,
});

function Results() {
  const { id } = Route.useParams();
  return (
    <div>
      <PageHeader
        eyebrow={`Session · ${id}`}
        title="Senior Product Designer · Leaderboard"
        description="214 candidates evaluated · 8 recommended for interview"
        actions={<><Button variant="outline"><Download className="mr-2 h-4 w-4" />Export</Button><Button className="bg-gradient-primary text-white shadow-glow hover:opacity-90"><Trophy className="mr-2 h-4 w-4" />Shortlist top 10</Button></>}
      />
      <Card className="border-border/70 bg-gradient-card p-4">
        <div className="mb-4 flex flex-wrap items-center gap-2">
          <div className="relative min-w-[240px] flex-1">
            <Search className="absolute left-2.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input placeholder="Search candidates..." className="h-9 bg-secondary/40 pl-8" />
          </div>
          <Button variant="outline" size="sm" className="h-9"><Filter className="mr-1.5 h-3.5 w-3.5" />Recommendation</Button>
          <Button variant="outline" size="sm" className="h-9"><Filter className="mr-1.5 h-3.5 w-3.5" />Experience</Button>
        </div>
        <div className="overflow-hidden rounded-lg border border-border/60">
          <Table>
            <TableHeader>
              <TableRow className="border-border/60 bg-secondary/40 hover:bg-secondary/40">
                <TableHead className="w-12">Rank</TableHead>
                <TableHead>Candidate</TableHead>
                <TableHead className="text-right">ATS</TableHead>
                <TableHead className="text-right">Match</TableHead>
                <TableHead>Experience</TableHead>
                <TableHead>Education</TableHead>
                <TableHead>Recommendation</TableHead>
                <TableHead></TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {candidates.map((c, i) => (
                <TableRow key={c.id} className="border-border/60">
                  <TableCell className="font-mono text-xs text-muted-foreground">#{i + 1}</TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2.5">
                      <div className="grid h-8 w-8 place-items-center rounded-full bg-gradient-primary text-xs font-semibold text-white">
                        {c.name.split(" ").map(n => n[0]).join("")}
                      </div>
                      <div>
                        <div className="text-sm font-medium">{c.name}</div>
                        <div className="text-xs text-muted-foreground">{c.role}</div>
                      </div>
                    </div>
                  </TableCell>
                  <TableCell className="text-right tabular-nums">{c.ats}</TableCell>
                  <TableCell className="text-right">
                    <div className="flex items-center justify-end gap-2">
                      <div className="h-1.5 w-16 overflow-hidden rounded-full bg-secondary"><div className="h-full bg-gradient-primary" style={{ width: `${c.match}%` }} /></div>
                      <span className="tabular-nums">{c.match}%</span>
                    </div>
                  </TableCell>
                  <TableCell className="text-muted-foreground">{c.exp}</TableCell>
                  <TableCell className="text-muted-foreground">{c.edu}</TableCell>
                  <TableCell>
                    <Badge className={c.rec === "Strong hire" ? "bg-success/15 text-success hover:bg-success/15" : c.rec === "Hire" ? "bg-primary/15 text-primary hover:bg-primary/15" : c.rec === "Consider" ? "bg-warning/15 text-warning hover:bg-warning/15" : "bg-destructive/15 text-destructive hover:bg-destructive/15"}>{c.rec}</Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    <Button asChild variant="ghost" size="sm"><Link to="/recruiter/candidates/$id" params={{ id: c.id }}>Open<ArrowUpRight className="ml-1 h-3.5 w-3.5" /></Link></Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </Card>
    </div>
  );
}
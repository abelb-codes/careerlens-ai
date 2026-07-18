import { createFileRoute, Link } from "@tanstack/react-router";
import { PageHeader, StatCard } from "@/components/app/shell";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { candidates, pipeline, applicationsTrend } from "@/lib/mock";
import { ArrowUpRight, Sparkles, Plus } from "lucide-react";
import { AreaChart, Area, ResponsiveContainer, XAxis, YAxis, Tooltip, BarChart, Bar, CartesianGrid } from "recharts";

export const Route = createFileRoute("/recruiter/")({
  component: RecruiterDashboard,
});

function RecruiterDashboard() {
  return (
    <div>
      <PageHeader
        eyebrow="Overview"
        title="Good morning, Priya."
        description="You have 3 evaluation sessions in progress and 41 new candidates today."
        actions={<Button asChild className="bg-gradient-primary text-white shadow-glow hover:opacity-90"><Link to="/recruiter/evaluations/new"><Plus className="mr-1 h-4 w-4" />New evaluation</Link></Button>}
      />
      <div className="grid gap-4 md:grid-cols-4">
        <StatCard label="Total Candidates" value="1,284" delta="+41" hint="Today" />
        <StatCard label="Avg. Match Score" value="72%" delta="+3%" hint="Last 30 days" />
        <StatCard label="Top Candidates" value="86" delta="+12" hint="Score ≥ 85" />
        <StatCard label="Active Evaluations" value="3" hint="2 completing today" />
      </div>

      <div className="mt-6 grid gap-4 lg:grid-cols-3">
        <Card className="border-border/70 bg-gradient-card p-6 lg:col-span-2">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <div className="text-xs uppercase tracking-widest text-muted-foreground">Applications</div>
              <div className="text-base font-semibold">This week</div>
            </div>
            <Badge className="bg-primary/15 text-primary hover:bg-primary/15">+38% WoW</Badge>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={applicationsTrend}>
                <defs>
                  <linearGradient id="a" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="oklch(0.66 0.19 258)" stopOpacity={0.6} />
                    <stop offset="100%" stopColor="oklch(0.66 0.19 258)" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid stroke="oklch(1 0 0 / 0.05)" vertical={false} />
                <XAxis dataKey="day" stroke="oklch(0.6 0.02 260)" fontSize={11} tickLine={false} axisLine={false} />
                <YAxis stroke="oklch(0.6 0.02 260)" fontSize={11} tickLine={false} axisLine={false} />
                <Tooltip contentStyle={{ background: "oklch(0.20 0.017 265)", border: "1px solid oklch(1 0 0 / 0.1)", borderRadius: 8 }} />
                <Area type="monotone" dataKey="v" stroke="oklch(0.66 0.19 258)" strokeWidth={2} fill="url(#a)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Card>

        <Card className="border-border/70 bg-gradient-card p-6">
          <div className="mb-4">
            <div className="text-xs uppercase tracking-widest text-muted-foreground">Hiring funnel</div>
            <div className="text-base font-semibold">Sr. Product Designer</div>
          </div>
          <div className="space-y-2.5">
            {pipeline.map((p, i) => {
              const pct = (p.value / pipeline[0].value) * 100;
              return (
                <div key={p.stage}>
                  <div className="mb-1 flex justify-between text-xs"><span className="text-muted-foreground">{p.stage}</span><span className="tabular-nums">{p.value}</span></div>
                  <div className="h-2 overflow-hidden rounded-full bg-secondary">
                    <div className="h-full bg-gradient-primary" style={{ width: `${pct}%`, opacity: 1 - i * 0.1 }} />
                  </div>
                </div>
              );
            })}
          </div>
        </Card>
      </div>

      <div className="mt-6 grid gap-4 lg:grid-cols-3">
        <Card className="border-border/70 bg-gradient-card p-6 lg:col-span-2">
          <div className="mb-4 flex items-center justify-between">
            <div className="text-sm font-semibold">Top candidates</div>
            <Button asChild variant="ghost" size="sm"><Link to="/recruiter/candidates">View all</Link></Button>
          </div>
          <div className="space-y-1.5">
            {candidates.slice(0, 5).map((c, i) => (
              <Link to="/recruiter/candidates/$id" params={{ id: c.id }} key={c.id} className="flex items-center gap-3 rounded-lg border border-border/60 bg-secondary/20 p-3 hover:border-primary/40 hover:bg-secondary/40">
                <div className="grid h-8 w-8 shrink-0 place-items-center rounded-lg bg-secondary text-xs font-semibold tabular-nums">#{i + 1}</div>
                <div className="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-gradient-primary text-xs font-semibold text-white">
                  {c.name.split(" ").map(n => n[0]).join("")}
                </div>
                <div className="min-w-0 flex-1">
                  <div className="truncate text-sm font-medium">{c.name}</div>
                  <div className="truncate text-xs text-muted-foreground">{c.role} · {c.exp} · {c.edu}</div>
                </div>
                <div className="hidden text-right text-xs text-muted-foreground sm:block">
                  <div>ATS <span className="tabular-nums text-foreground">{c.ats}</span></div>
                  <div>Match <span className="tabular-nums text-foreground">{c.match}%</span></div>
                </div>
                <Badge className={c.rec === "Strong hire" ? "bg-success/15 text-success hover:bg-success/15" : c.rec === "Hire" ? "bg-primary/15 text-primary hover:bg-primary/15" : "bg-warning/15 text-warning hover:bg-warning/15"}>{c.rec}</Badge>
              </Link>
            ))}
          </div>
        </Card>
        <Card className="border-border/70 bg-gradient-card p-6">
          <div className="mb-4 flex items-center gap-2 text-sm font-semibold"><Sparkles className="h-4 w-4 text-accent" />AI recruiter insights</div>
          <ul className="space-y-3 text-sm text-muted-foreground">
            <li>• 3 candidates above 90% match on <span className="text-foreground">Sr. Product Designer</span> — schedule interviews.</li>
            <li>• Job description for <span className="text-foreground">Data Scientist</span> uses jargon that reduces qualified applications by ~18%.</li>
            <li>• Consider adding "React 19" to <span className="text-foreground">Staff Frontend</span> — matches your top 5 candidates.</li>
          </ul>
        </Card>
      </div>

      <Card className="mt-6 border-border/70 bg-gradient-card p-6">
        <div className="mb-4 flex items-center justify-between">
          <div className="text-sm font-semibold">Top skills across shortlisted candidates</div>
          <Button variant="ghost" size="sm">Export</Button>
        </div>
        <div className="h-56">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={[
              { s: "React", v: 82 }, { s: "TypeScript", v: 76 }, { s: "Design Systems", v: 68 },
              { s: "Figma", v: 91 }, { s: "System Design", v: 54 }, { s: "GraphQL", v: 42 }, { s: "Testing", v: 61 },
            ]}>
              <CartesianGrid stroke="oklch(1 0 0 / 0.05)" vertical={false} />
              <XAxis dataKey="s" stroke="oklch(0.6 0.02 260)" fontSize={11} tickLine={false} axisLine={false} />
              <YAxis stroke="oklch(0.6 0.02 260)" fontSize={11} tickLine={false} axisLine={false} />
              <Tooltip contentStyle={{ background: "oklch(0.20 0.017 265)", border: "1px solid oklch(1 0 0 / 0.1)", borderRadius: 8 }} />
              <Bar dataKey="v" radius={[6, 6, 0, 0]} fill="oklch(0.62 0.22 295)" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </Card>

      <div className="mt-8 text-right text-xs text-muted-foreground">Powered by CareerLens AI · Real-time <ArrowUpRight className="ml-0.5 inline h-3 w-3" /></div>
    </div>
  );
}
import { createFileRoute } from "@tanstack/react-router";
import { PageHeader, StatCard } from "@/components/app/shell";
import { Card } from "@/components/ui/card";
import { BarChart, Bar, LineChart, Line, ResponsiveContainer, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

export const Route = createFileRoute("/recruiter/analytics")({
  head: () => ({ meta: [{ title: "Analytics — CareerLens AI" }] }),
  component: Analytics,
});

const monthly = [
  { m: "May", v: 220 }, { m: "Jun", v: 340 }, { m: "Jul", v: 480 },
  { m: "Aug", v: 620 }, { m: "Sep", v: 810 }, { m: "Oct", v: 1240 },
];
const exp = [
  { r: "0–2y", v: 128 }, { r: "3–5y", v: 342 }, { r: "6–8y", v: 264 },
  { r: "9–12y", v: 140 }, { r: "13y+", v: 62 },
];

function Analytics() {
  return (
    <div>
      <PageHeader eyebrow="Analytics" title="Hiring analytics" description="Platform-wide metrics across all evaluation sessions." />
      <div className="grid gap-4 md:grid-cols-4">
        <StatCard label="Applications" value="8,214" delta="+18%" hint="Last 90 days" />
        <StatCard label="Interviews" value="342" delta="+22%" />
        <StatCard label="Offers" value="41" delta="+9%" />
        <StatCard label="Time to shortlist" value="3.2m" delta="-42%" hint="vs. Q2" />
      </div>
      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        <Card className="border-border/70 bg-gradient-card p-6">
          <div className="mb-3 text-sm font-semibold">Applications trend</div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={monthly}>
                <CartesianGrid stroke="oklch(1 0 0 / 0.05)" vertical={false} />
                <XAxis dataKey="m" stroke="oklch(0.6 0.02 260)" fontSize={11} tickLine={false} axisLine={false} />
                <YAxis stroke="oklch(0.6 0.02 260)" fontSize={11} tickLine={false} axisLine={false} />
                <Tooltip contentStyle={{ background: "oklch(0.20 0.017 265)", border: "1px solid oklch(1 0 0 / 0.1)", borderRadius: 8 }} />
                <Line type="monotone" dataKey="v" stroke="oklch(0.66 0.19 258)" strokeWidth={2.5} dot={{ r: 3, fill: "oklch(0.66 0.19 258)" }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>
        <Card className="border-border/70 bg-gradient-card p-6">
          <div className="mb-3 text-sm font-semibold">Experience distribution</div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={exp}>
                <CartesianGrid stroke="oklch(1 0 0 / 0.05)" vertical={false} />
                <XAxis dataKey="r" stroke="oklch(0.6 0.02 260)" fontSize={11} tickLine={false} axisLine={false} />
                <YAxis stroke="oklch(0.6 0.02 260)" fontSize={11} tickLine={false} axisLine={false} />
                <Tooltip contentStyle={{ background: "oklch(0.20 0.017 265)", border: "1px solid oklch(1 0 0 / 0.1)", borderRadius: 8 }} />
                <Bar dataKey="v" radius={[6, 6, 0, 0]} fill="oklch(0.62 0.22 295)" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>
    </div>
  );
}
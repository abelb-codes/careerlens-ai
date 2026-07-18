import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/app/shell";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";

export const Route = createFileRoute("/recruiter/settings")({
  head: () => ({ meta: [{ title: "Recruiter Settings — CareerLens AI" }] }),
  component: Settings,
});

function Settings() {
  return (
    <div>
      <PageHeader eyebrow="Settings" title="Workspace settings" description="Team, integrations, and AI preferences." />
      <div className="grid gap-4 lg:grid-cols-2">
        <Card className="border-border/70 bg-gradient-card p-6">
          <div className="text-sm font-semibold">Workspace</div>
          <div className="mt-4 space-y-3">
            <div><Label>Company name</Label><Input defaultValue="Northwind" className="mt-1.5" /></div>
            <div><Label>Domain</Label><Input defaultValue="northwind.co" className="mt-1.5" /></div>
          </div>
        </Card>
        <Card className="border-border/70 bg-gradient-card p-6">
          <div className="text-sm font-semibold">AI preferences</div>
          {[
            { l: "Bias-aware scoring", d: "Reduce weight of demographic signals" },
            { l: "Verbose reasoning", d: "Show full AI reasoning on every candidate" },
            { l: "Auto-generate interview questions", d: "For every candidate above 70% match" },
          ].map((r, i) => (
            <div key={r.l} className={`flex items-center justify-between py-3 ${i > 0 ? "border-t border-border/60" : ""}`}>
              <div><div className="text-sm font-medium">{r.l}</div><div className="text-xs text-muted-foreground">{r.d}</div></div>
              <Switch defaultChecked />
            </div>
          ))}
        </Card>
      </div>
      <div className="mt-6 flex justify-end"><Button className="bg-gradient-primary text-white shadow-glow hover:opacity-90">Save changes</Button></div>
    </div>
  );
}
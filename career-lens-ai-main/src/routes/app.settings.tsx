import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/app/shell";
import { Card } from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";
import { Button } from "@/components/ui/button";

export const Route = createFileRoute("/app/settings")({
  head: () => ({ meta: [{ title: "Settings — CareerLens AI" }] }),
  component: Settings,
});

function Settings() {
  const rows = [
    { l: "Email notifications", d: "Get updates when a report is ready.", v: true },
    { l: "Weekly summary", d: "Every Monday, your career progress.", v: true },
    { l: "AI recommendations", d: "Personalized suggestions based on your resume.", v: false },
    { l: "Data retention (30 days)", d: "Auto-delete resumes after 30 days.", v: false },
  ];
  return (
    <div>
      <PageHeader eyebrow="Settings" title="Preferences" description="Notifications, privacy, and data." />
      <Card className="max-w-3xl border-border/70 bg-gradient-card">
        {rows.map((r, i) => (
          <div key={r.l} className={`flex items-center justify-between p-5 ${i > 0 ? "border-t border-border/60" : ""}`}>
            <div>
              <div className="text-sm font-medium">{r.l}</div>
              <div className="text-xs text-muted-foreground">{r.d}</div>
            </div>
            <Switch defaultChecked={r.v} />
          </div>
        ))}
        <div className="flex justify-between border-t border-border/60 p-5">
          <Button variant="outline">Delete account</Button>
          <Button className="bg-gradient-primary text-white shadow-glow hover:opacity-90">Save changes</Button>
        </div>
      </Card>
    </div>
  );
}
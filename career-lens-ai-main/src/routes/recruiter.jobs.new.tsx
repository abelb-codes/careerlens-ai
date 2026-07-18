import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { PageHeader } from "@/components/app/shell";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import { X } from "lucide-react";
import { useState } from "react";

export const Route = createFileRoute("/recruiter/jobs/new")({
  head: () => ({ meta: [{ title: "New Job — CareerLens AI" }] }),
  component: NewJob,
});

function NewJob() {
  const navigate = useNavigate();
  const [skills, setSkills] = useState<string[]>(["Figma", "Design Systems", "Prototyping"]);
  const [input, setInput] = useState("");
  return (
    <div>
      <PageHeader eyebrow="Create" title="New job description" description="Rich, structured, ATS-ready." />
      <div className="grid gap-4 lg:grid-cols-[1.4fr_1fr]">
        <Card className="border-border/70 bg-gradient-card p-6">
          <form onSubmit={(e) => { e.preventDefault(); toast.success("Job created"); navigate({ to: "/recruiter/jobs" }); }} className="space-y-4">
            <div><Label>Title</Label><Input required defaultValue="Senior Product Designer" className="mt-1.5" /></div>
            <div className="grid grid-cols-2 gap-3">
              <div><Label>Team</Label><Input defaultValue="Design" className="mt-1.5" /></div>
              <div><Label>Experience</Label><Input defaultValue="5+ years" className="mt-1.5" /></div>
            </div>
            <div><Label>Description</Label><Textarea rows={8} className="mt-1.5" defaultValue="We're looking for a senior product designer who's shipped end-to-end in B2B SaaS..." /></div>
            <div>
              <Label>Required skills</Label>
              <div className="mt-2 flex flex-wrap gap-2">
                {skills.map((s) => (
                  <Badge key={s} variant="secondary" className="gap-1 bg-secondary/60">
                    {s}
                    <button type="button" onClick={() => setSkills(skills.filter(x => x !== s))}><X className="h-3 w-3" /></button>
                  </Badge>
                ))}
                <Input
                  value={input} onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => { if (e.key === "Enter" && input) { e.preventDefault(); setSkills([...skills, input]); setInput(""); } }}
                  placeholder="Add skill and press Enter"
                  className="h-7 w-48 bg-secondary/40 text-xs"
                />
              </div>
            </div>
            <div className="flex justify-end gap-2 border-t border-border/60 pt-4">
              <Button variant="outline" type="button">Save draft</Button>
              <Button className="bg-gradient-primary text-white shadow-glow hover:opacity-90">Publish job</Button>
            </div>
          </form>
        </Card>
        <Card className="border-border/70 bg-gradient-card p-6">
          <div className="text-xs uppercase tracking-widest text-muted-foreground">Live preview</div>
          <div className="mt-1 text-lg font-semibold">Senior Product Designer</div>
          <div className="mt-1 text-xs text-muted-foreground">Design · 5+ years · Full-time</div>
          <div className="mt-4 text-sm leading-relaxed text-muted-foreground">
            We're looking for a senior product designer who's shipped end-to-end in B2B SaaS...
          </div>
          <div className="mt-4 flex flex-wrap gap-1.5">
            {skills.map(s => <Badge key={s} variant="secondary" className="bg-secondary/60">{s}</Badge>)}
          </div>
        </Card>
      </div>
    </div>
  );
}
import { createFileRoute, Link } from "@tanstack/react-router";
import { PageHeader, ScoreRing } from "@/components/app/shell";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { candidates } from "@/lib/mock";
import { Download, ArrowLeft, MessageSquareText, Sparkles, CheckCircle2, XCircle, Award, Briefcase, GraduationCap, FileText } from "lucide-react";

export const Route = createFileRoute("/recruiter/candidates/$id")({
  head: () => ({ meta: [{ title: "Candidate — CareerLens AI" }] }),
  component: Candidate,
});

function Candidate() {
  const { id } = Route.useParams();
  const c = candidates.find(x => x.id === id) ?? candidates[0];
  return (
    <div>
      <div className="mb-4"><Button asChild variant="ghost" size="sm"><Link to="/recruiter/candidates"><ArrowLeft className="mr-1 h-3.5 w-3.5" />All candidates</Link></Button></div>
      <div className="mb-6 grid grid-cols-[minmax(0,1fr)_auto] items-center gap-4 sm:flex sm:justify-between">
        <div className="flex min-w-0 items-center gap-4">
          <div className="grid h-14 w-14 shrink-0 place-items-center rounded-2xl bg-gradient-primary text-lg font-semibold text-white">
            {c.name.split(" ").map(n => n[0]).join("")}
          </div>
          <div className="min-w-0">
            <h1 className="truncate text-2xl font-semibold tracking-tight">{c.name}</h1>
            <p className="truncate text-sm text-muted-foreground">{c.role} · {c.exp} · {c.edu}</p>
          </div>
        </div>
        <div className="flex gap-2">
          <Button variant="outline"><Download className="mr-2 h-4 w-4" />Resume</Button>
          <Button className="bg-gradient-primary text-white shadow-glow hover:opacity-90"><MessageSquareText className="mr-2 h-4 w-4" />Move to interview</Button>
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-[280px_1fr]">
        <div className="space-y-4">
          <Card className="border-border/70 bg-gradient-card p-6 text-center">
            <ScoreRing value={c.match} size={120} label="Match" />
            <div className="mt-3 flex justify-center gap-2 text-xs">
              <Badge className="bg-primary/15 text-primary hover:bg-primary/15">ATS {c.ats}</Badge>
              <Badge className={c.rec === "Strong hire" ? "bg-success/15 text-success hover:bg-success/15" : c.rec === "Hire" ? "bg-primary/15 text-primary hover:bg-primary/15" : "bg-warning/15 text-warning hover:bg-warning/15"}>{c.rec}</Badge>
            </div>
          </Card>
          <Card className="border-border/70 bg-gradient-card p-5">
            <div className="mb-3 flex items-center gap-2 text-sm font-semibold"><Sparkles className="h-4 w-4 text-accent" />AI summary</div>
            <p className="text-sm text-muted-foreground">Seasoned designer with strong B2B SaaS scope. High signal on design systems. Weak signal on motion & prototyping tools.</p>
          </Card>
        </div>

        <div className="space-y-4">
          <Card className="border-border/70 bg-gradient-card p-6">
            <div className="mb-4 flex items-center gap-2 text-sm font-semibold"><FileText className="h-4 w-4 text-primary" />Resume preview</div>
            <div className="grid gap-4 rounded-lg border border-border/60 bg-secondary/20 p-6 text-sm">
              <div>
                <div className="text-lg font-semibold">{c.name}</div>
                <div className="text-xs text-muted-foreground">{c.role} · Lisbon, PT · candidate@studio.co</div>
              </div>
              <div>
                <div className="mb-1 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Summary</div>
                <p className="text-muted-foreground">Product designer with {c.exp} experience shipping B2B SaaS products in fintech and dev-tools.</p>
              </div>
              <div>
                <div className="mb-1 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Experience</div>
                <ul className="space-y-1 text-muted-foreground">
                  <li>• Kepler — Senior Product Designer, 2023–now</li>
                  <li>• Aperture — Product Designer, 2019–2023</li>
                </ul>
              </div>
            </div>
          </Card>

          <Tabs defaultValue="skills">
            <TabsList className="bg-secondary/40">
              <TabsTrigger value="skills"><Award className="mr-1.5 h-3.5 w-3.5" />Skills</TabsTrigger>
              <TabsTrigger value="exp"><Briefcase className="mr-1.5 h-3.5 w-3.5" />Experience</TabsTrigger>
              <TabsTrigger value="edu"><GraduationCap className="mr-1.5 h-3.5 w-3.5" />Education</TabsTrigger>
              <TabsTrigger value="ai"><Sparkles className="mr-1.5 h-3.5 w-3.5" />AI insights</TabsTrigger>
            </TabsList>
            <TabsContent value="skills" className="mt-4">
              <Card className="border-border/70 bg-gradient-card p-6">
                <div className="flex flex-wrap gap-2">
                  {["Figma", "Design Systems", "Tokens", "Prototyping", "UX Research", "B2B SaaS", "Notion"].map(s => <Badge key={s} variant="secondary" className="bg-secondary/60">{s}</Badge>)}
                </div>
              </Card>
            </TabsContent>
            <TabsContent value="exp" className="mt-4"><Card className="border-border/70 bg-gradient-card p-6 text-sm text-muted-foreground">6 years across Kepler, Aperture, and Helix.</Card></TabsContent>
            <TabsContent value="edu" className="mt-4"><Card className="border-border/70 bg-gradient-card p-6 text-sm text-muted-foreground">{c.edu}</Card></TabsContent>
            <TabsContent value="ai" className="mt-4">
              <Card className="border-border/70 bg-gradient-card p-6">
                <div className="grid gap-4 sm:grid-cols-2">
                  <div>
                    <div className="mb-2 flex items-center gap-2 text-sm font-semibold"><CheckCircle2 className="h-4 w-4 text-success" />Strengths</div>
                    <ul className="space-y-1 text-sm text-muted-foreground">
                      <li>• Design systems ownership at Kepler</li>
                      <li>• Strong impact metrics on onboarding</li>
                    </ul>
                  </div>
                  <div>
                    <div className="mb-2 flex items-center gap-2 text-sm font-semibold"><XCircle className="h-4 w-4 text-destructive" />Gaps</div>
                    <ul className="space-y-1 text-sm text-muted-foreground">
                      <li>• Limited motion / animation experience</li>
                      <li>• No mention of design QA</li>
                    </ul>
                  </div>
                </div>
                <div className="mt-6">
                  <div className="mb-2 flex items-center gap-2 text-sm font-semibold"><MessageSquareText className="h-4 w-4 text-accent" />Interview questions</div>
                  <ol className="space-y-2 text-sm text-muted-foreground">
                    <li>1. Walk me through your tokens architecture at Kepler.</li>
                    <li>2. How would you approach a Figma Variables migration?</li>
                    <li>3. Describe a time a rollout broke — how did you recover?</li>
                  </ol>
                </div>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
}
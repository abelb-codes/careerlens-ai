import { createFileRoute, Link } from "@tanstack/react-router";
import { PageHeader, ScoreRing } from "@/components/app/shell";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { skillRadar } from "@/lib/mock";
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, ResponsiveContainer } from "recharts";
import { CheckCircle2, XCircle, Sparkles, Download, ArrowLeft, MessageSquareText } from "lucide-react";
import { useEffect, useState } from "react";
import api from "@/api/axios";

type Analysis = {
  ats_score: number;
  quality_score: number;
  matching_score: number;
  extracted_skills: string[];
  suggestions: string[];
  interview_questions: string[];
};

export const Route = createFileRoute("/app/reports/$id")({
  head: () => ({ meta: [{ title: "Analysis report — CareerLens AI" }] }),
  component: Report,
});

function Report() {
  const { id } = Route.useParams();
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    api
      .get<Analysis>(`/api/analysis/${id}/`)
      .then(({ data }) => setAnalysis(data))
      .catch(() => setError(true));
  }, [id]);

  if (error) {
    return <div className="text-sm text-destructive">This report is not available yet. Please wait for analysis to finish and try again.</div>;
  }

  if (!analysis) {
    return <div className="text-sm text-muted-foreground">Loading analysis report…</div>;
  }

  return (
    <div>
      <div className="mb-4"><Button asChild variant="ghost" size="sm"><Link to="/app/reports"><ArrowLeft className="mr-1 h-3.5 w-3.5" />All reports</Link></Button></div>
      <PageHeader
        eyebrow={`Report · ${id}`}
        title="Resume analysis"
        description="AI-generated scores, skills, and recommendations."
        actions={<><Button variant="outline"><Download className="mr-2 h-4 w-4" />Export PDF</Button><Button className="bg-gradient-primary text-white shadow-glow hover:opacity-90"><Sparkles className="mr-2 h-4 w-4" />Re-analyze</Button></>}
      />

      <div className="grid gap-4 lg:grid-cols-[1fr_1fr_1fr]">
        <Card className="border-border/70 bg-gradient-card p-6 text-center">
          <div className="text-xs uppercase tracking-widest text-muted-foreground">Overall</div>
          <div className="mt-4 flex justify-center"><ScoreRing value={analysis.quality_score} size={140} label="Score" /></div>
          <div className="mt-4 text-sm text-muted-foreground">Resume quality score</div>
        </Card>
        <Card className="border-border/70 bg-gradient-card p-6 text-center">
          <div className="text-xs uppercase tracking-widest text-muted-foreground">ATS Compatibility</div>
          <div className="mt-4 flex justify-center"><ScoreRing value={analysis.ats_score} size={140} label="ATS" /></div>
          <div className="mt-4 text-sm text-muted-foreground">Job match: {analysis.matching_score}%</div>
        </Card>
        <Card className="border-border/70 bg-gradient-card p-6">
          <div className="text-xs uppercase tracking-widest text-muted-foreground">Skill radar</div>
          <div className="mt-2 h-52">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={skillRadar}>
                <PolarGrid stroke="oklch(1 0 0 / 0.08)" />
                <PolarAngleAxis dataKey="skill" tick={{ fill: "oklch(0.7 0.02 260)", fontSize: 11 }} />
                <Radar dataKey="A" stroke="oklch(0.62 0.22 295)" fill="oklch(0.62 0.22 295)" fillOpacity={0.35} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>

      <Tabs defaultValue="overview" className="mt-6">
        <TabsList className="bg-secondary/40">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="skills">Skills</TabsTrigger>
          <TabsTrigger value="keywords">Keywords</TabsTrigger>
          <TabsTrigger value="feedback">Feedback</TabsTrigger>
          <TabsTrigger value="interview">Interview</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="mt-4 grid gap-4 md:grid-cols-2">
          <Card className="border-border/70 bg-gradient-card p-6">
            <div className="mb-3 flex items-center gap-2 text-sm font-semibold"><CheckCircle2 className="h-4 w-4 text-success" />Strengths</div>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>• Clear impact metrics on the last 3 roles</li>
              <li>• Strong design systems and tokens work</li>
              <li>• Senior scope across B2B SaaS platforms</li>
              <li>• Case studies linked and readable</li>
            </ul>
          </Card>
          <Card className="border-border/70 bg-gradient-card p-6">
            <div className="mb-3 flex items-center gap-2 text-sm font-semibold"><XCircle className="h-4 w-4 text-destructive" />Weaknesses</div>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>• Motion prototyping not represented</li>
              <li>• No mention of Figma variables</li>
              <li>• Summary paragraph is 4 lines too long</li>
            </ul>
          </Card>
        </TabsContent>

        <TabsContent value="skills" className="mt-4">
          <Card className="border-border/70 bg-gradient-card p-6">
            <div className="mb-3 text-sm font-semibold">Extracted skills</div>
            <div className="flex flex-wrap gap-2">
              {analysis.extracted_skills.map(s => (
                <Badge key={s} variant="secondary" className="bg-secondary/60">{s}</Badge>
              ))}
            </div>
          </Card>
        </TabsContent>

        <TabsContent value="keywords" className="mt-4">
          <Card className="border-border/70 bg-gradient-card p-6">
            <div className="mb-4 text-sm font-semibold">Keyword coverage</div>
            <div className="space-y-3">
              {[{ k: "design systems", v: 96 }, { k: "product design", v: 91 }, { k: "B2B SaaS", v: 84 }, { k: "prototyping", v: 62 }, { k: "motion", v: 22 }].map(k => (
                <div key={k.k}>
                  <div className="mb-1 flex justify-between text-xs"><span className="text-muted-foreground">{k.k}</span><span className="tabular-nums">{k.v}%</span></div>
                  <Progress value={k.v} className="h-1.5" />
                </div>
              ))}
            </div>
          </Card>
        </TabsContent>

        <TabsContent value="feedback" className="mt-4 grid gap-4 md:grid-cols-2">
          <Card className="border-border/70 bg-gradient-card p-6">
            <div className="mb-3 text-sm font-semibold">Grammar & tone</div>
            <ul className="space-y-2 text-sm text-muted-foreground">{analysis.suggestions.map((suggestion) => <li key={suggestion}>• {suggestion}</li>)}</ul>
          </Card>
          <Card className="border-border/70 bg-gradient-card p-6">
            <div className="mb-3 text-sm font-semibold">Formatting</div>
            <p className="text-sm text-muted-foreground">Single-column layout, readable font, ATS-friendly headings. Great.</p>
          </Card>
        </TabsContent>

        <TabsContent value="interview" className="mt-4">
          <Card className="border-border/70 bg-gradient-card p-6">
            <div className="mb-4 flex items-center gap-2 text-sm font-semibold"><MessageSquareText className="h-4 w-4 text-accent" />AI-generated interview questions</div>
            <ol className="space-y-3 text-sm">
              {analysis.interview_questions.map((q, i) => (
                <li key={i} className="flex gap-3 rounded-lg border border-border/60 bg-secondary/20 p-3">
                  <div className="grid h-6 w-6 shrink-0 place-items-center rounded-full bg-primary/15 text-xs font-semibold text-primary">{i + 1}</div>
                  <span>{q}</span>
                </li>
              ))}
            </ol>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}

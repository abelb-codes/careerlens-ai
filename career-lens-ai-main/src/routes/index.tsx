import { createFileRoute } from "@tanstack/react-router";
import { Link } from "@tanstack/react-router";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { MarketingNav, MarketingFooter } from "@/components/marketing/nav";
import { stats, features, testimonials, faqs, pricing } from "@/lib/mock";
import {
  ArrowRight, Sparkles, Target, Trophy, MessageSquareText, ShieldCheck, Workflow,
  Check, Star, FileText, Zap, BarChart3,
} from "lucide-react";

const iconMap: Record<string, React.ComponentType<{ className?: string }>> = {
  Sparkles, Target, Trophy, MessageSquareText, ShieldCheck, Workflow,
};

export const Route = createFileRoute("/")({
  component: Landing,
});

function Landing() {
  return (
    <div className="relative min-h-screen bg-background">
      <div className="pointer-events-none absolute inset-x-0 top-0 h-[900px] bg-gradient-hero" />
      <div className="pointer-events-none absolute inset-x-0 top-0 h-[900px] grid-bg opacity-60" />
      <div className="relative">
        <MarketingNav />
        <Hero />
        <LogoStrip />
        <FeatureCards />
        <ProductShowcase />
        <StatsBand />
        <Testimonials />
        <Pricing />
        <FAQ />
        <CTA />
        <MarketingFooter />
      </div>
    </div>
  );
}

function Hero() {
  return (
    <section className="mx-auto max-w-6xl px-6 pt-20 pb-24 text-center sm:pt-28">
      <Badge variant="outline" className="mb-6 gap-1.5 border-border/80 bg-secondary/60 px-3 py-1 text-xs font-medium backdrop-blur">
        <span className="h-1.5 w-1.5 rounded-full bg-success animate-pulse" />
        New · Interview question generator v2
      </Badge>
      <h1 className="mx-auto max-w-4xl text-5xl font-semibold tracking-tight sm:text-6xl md:text-7xl">
        Hire the right people
        <br />
        <span className="font-display italic text-gradient">10x faster.</span>
      </h1>
      <p className="mx-auto mt-6 max-w-2xl text-lg text-muted-foreground">
        CareerLens AI reads resumes the way your best recruiter would — then ranks,
        scores, and explains every candidate. Applicants get honest feedback.
        Recruiters get a shortlist in minutes.
      </p>
      <div className="mt-9 flex flex-wrap items-center justify-center gap-3">
        <Button asChild size="lg" className="h-12 bg-gradient-primary px-6 text-white shadow-glow hover:opacity-90">
          <Link to="/app">Analyze my resume <ArrowRight className="ml-1 h-4 w-4" /></Link>
        </Button>
        <Button asChild size="lg" variant="outline" className="h-12 border-border bg-secondary/40 px-6 backdrop-blur">
          <Link to="/recruiter">Recruit smarter</Link>
        </Button>
      </div>
      <div className="mt-4 text-xs text-muted-foreground">No credit card required · SOC 2 Type II</div>

      <HeroPreview />
    </section>
  );
}

function HeroPreview() {
  return (
    <div className="relative mx-auto mt-16 max-w-5xl">
      <div className="absolute -inset-4 -z-10 rounded-[2rem] bg-gradient-primary opacity-30 blur-3xl" />
      <div className="glass overflow-hidden rounded-2xl border-border shadow-elegant">
        <div className="flex items-center gap-2 border-b border-border/70 bg-card/60 px-4 py-2.5">
          <div className="flex gap-1.5">
            <span className="h-2.5 w-2.5 rounded-full bg-destructive/70" />
            <span className="h-2.5 w-2.5 rounded-full bg-warning/70" />
            <span className="h-2.5 w-2.5 rounded-full bg-success/70" />
          </div>
          <div className="ml-4 flex-1 truncate rounded-md bg-secondary/60 px-3 py-1 text-xs text-muted-foreground">
            careerlens.ai/recruiter/evaluations/eval_7f2
          </div>
        </div>
        <div className="grid gap-6 p-6 md:grid-cols-[1.4fr_1fr]">
          <div>
            <div className="mb-4 flex items-center justify-between">
              <div>
                <div className="text-xs uppercase tracking-wider text-muted-foreground">Evaluation session</div>
                <div className="text-lg font-semibold">Senior Product Designer · 214 candidates</div>
              </div>
              <Badge className="bg-success/15 text-success hover:bg-success/15">Completed</Badge>
            </div>
            <div className="space-y-2">
              {[
                { rank: 1, name: "Amelia Chen", score: 96 },
                { rank: 2, name: "Rahul Menon", score: 92 },
                { rank: 3, name: "Nora Bakr", score: 89 },
                { rank: 4, name: "Ken Watanabe", score: 84 },
              ].map((c) => (
                <div key={c.rank} className="flex items-center gap-3 rounded-xl border border-border/60 bg-card/40 p-3">
                  <div className="grid h-8 w-8 place-items-center rounded-lg bg-secondary text-xs font-semibold">#{c.rank}</div>
                  <div className="flex-1 min-w-0">
                    <div className="truncate text-sm font-medium">{c.name}</div>
                    <div className="mt-1 h-1.5 overflow-hidden rounded-full bg-secondary">
                      <div className="h-full bg-gradient-primary" style={{ width: `${c.score}%` }} />
                    </div>
                  </div>
                  <div className="text-sm font-semibold tabular-nums">{c.score}</div>
                </div>
              ))}
            </div>
          </div>
          <div className="rounded-xl border border-border/60 bg-card/40 p-4">
            <div className="mb-3 flex items-center gap-2 text-xs uppercase tracking-wider text-muted-foreground">
              <Sparkles className="h-3.5 w-3.5 text-primary" /> AI reasoning
            </div>
            <p className="text-sm leading-relaxed">
              Amelia leads on <span className="text-foreground font-medium">design systems</span> (94%
              semantic match) and <span className="text-foreground font-medium">B2B SaaS</span>
              experience. Slight gap on <span className="text-warning">motion prototyping</span>.
            </p>
            <div className="mt-4 grid grid-cols-3 gap-2 text-center">
              {[
                { l: "ATS", v: 96, c: "text-primary" },
                { l: "Match", v: 94, c: "text-accent" },
                { l: "Confidence", v: 92, c: "text-success" },
              ].map((m) => (
                <div key={m.l} className="rounded-lg bg-secondary/60 p-2">
                  <div className={`text-lg font-semibold tabular-nums ${m.c}`}>{m.v}</div>
                  <div className="text-[10px] uppercase tracking-wider text-muted-foreground">{m.l}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function LogoStrip() {
  const logos = ["Northwind", "Kepler", "Aperture", "Monolith", "Helix", "Vellum"];
  return (
    <section className="mx-auto max-w-6xl px-6 pb-16">
      <div className="text-center text-xs uppercase tracking-widest text-muted-foreground">
        Trusted by talent teams at
      </div>
      <div className="mt-6 flex flex-wrap items-center justify-center gap-x-10 gap-y-4 opacity-70">
        {logos.map((l) => (
          <div key={l} className="font-display text-2xl italic tracking-tight text-foreground/70">{l}</div>
        ))}
      </div>
    </section>
  );
}

function FeatureCards() {
  return (
    <section className="mx-auto max-w-6xl px-6 py-24">
      <SectionHeading eyebrow="Platform" title={<>Every step of hiring, <span className="text-gradient font-display italic">reimagined.</span></>} />
      <div className="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {features.map((f) => {
          const Icon = iconMap[f.icon];
          return (
            <Card key={f.title} className="group relative overflow-hidden border-border/70 bg-gradient-card p-6 transition-all hover:border-primary/40 hover:shadow-glow">
              <div className="mb-4 grid h-10 w-10 place-items-center rounded-xl bg-primary/10 text-primary ring-1 ring-primary/20">
                <Icon className="h-5 w-5" />
              </div>
              <div className="text-base font-semibold">{f.title}</div>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{f.desc}</p>
            </Card>
          );
        })}
      </div>
    </section>
  );
}

function ProductShowcase() {
  const items = [
    { icon: FileText, title: "AI Resume Analysis", desc: "Parse, score, and explain every resume in seconds.", tint: "bg-primary/10 text-primary ring-primary/20" },
    { icon: Target, title: "ATS Score", desc: "Show applicants exactly what to fix, and why.", tint: "bg-accent/10 text-accent ring-accent/20" },
    { icon: Trophy, title: "Candidate Ranking", desc: "Semantic ranking with weighted skill coverage.", tint: "bg-success/10 text-success ring-success/20" },
    { icon: MessageSquareText, title: "AI Interview Questions", desc: "Per-candidate questions, tailored to gaps.", tint: "bg-warning/10 text-warning ring-warning/20" },
  ];
  return (
    <section className="mx-auto max-w-6xl px-6 py-8">
      <div className="grid gap-4 md:grid-cols-2">
        {items.map((it) => (
          <Card key={it.title} className="flex items-start gap-4 border-border/70 bg-gradient-card p-6">
            <div className={`grid h-11 w-11 shrink-0 place-items-center rounded-xl ring-1 ${it.tint}`}>
              <it.icon className="h-5 w-5" />
            </div>
            <div>
              <div className="text-base font-semibold">{it.title}</div>
              <p className="mt-1 text-sm text-muted-foreground">{it.desc}</p>
            </div>
          </Card>
        ))}
      </div>
    </section>
  );
}

function StatsBand() {
  return (
    <section className="mx-auto max-w-6xl px-6 py-24">
      <div className="glass grid gap-6 rounded-2xl p-10 sm:grid-cols-2 md:grid-cols-4">
        {stats.map((s) => (
          <div key={s.label} className="text-center">
            <div className="text-4xl font-semibold tracking-tight text-gradient">{s.value}</div>
            <div className="mt-2 text-xs uppercase tracking-wider text-muted-foreground">{s.label}</div>
          </div>
        ))}
      </div>
    </section>
  );
}

function Testimonials() {
  return (
    <section className="mx-auto max-w-6xl px-6 py-24">
      <SectionHeading eyebrow="Loved by teams" title={<>The <span className="font-display italic text-gradient">receipts.</span></>} />
      <div className="mt-12 grid gap-4 md:grid-cols-3">
        {testimonials.map((t) => (
          <Card key={t.name} className="border-border/70 bg-gradient-card p-6">
            <div className="flex gap-0.5 text-warning">
              {[...Array(5)].map((_, i) => <Star key={i} className="h-4 w-4 fill-current" />)}
            </div>
            <p className="mt-4 text-sm leading-relaxed text-foreground/90">"{t.quote}"</p>
            <div className="mt-6 flex items-center gap-3">
              <div className="grid h-9 w-9 place-items-center rounded-full bg-gradient-primary text-xs font-semibold text-white">
                {t.name.split(" ").map(n => n[0]).join("")}
              </div>
              <div>
                <div className="text-sm font-medium">{t.name}</div>
                <div className="text-xs text-muted-foreground">{t.role}</div>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </section>
  );
}

function Pricing() {
  return (
    <section id="pricing" className="mx-auto max-w-6xl px-6 py-24">
      <SectionHeading eyebrow="Pricing" title={<>Simple, <span className="font-display italic text-gradient">scale-friendly</span>.</>} />
      <div className="mt-12 grid gap-4 md:grid-cols-3">
        {pricing.map((p) => (
          <Card key={p.name} className={`relative flex flex-col border-border/70 bg-gradient-card p-8 ${p.highlight ? "border-primary/50 shadow-glow" : ""}`}>
            {p.highlight && (
              <Badge className="absolute -top-3 left-1/2 -translate-x-1/2 bg-gradient-primary text-white">Most popular</Badge>
            )}
            <div className="text-sm font-medium text-muted-foreground">{p.name}</div>
            <div className="mt-3 flex items-baseline gap-1">
              <div className="text-4xl font-semibold tracking-tight">{p.price}</div>
              <div className="text-sm text-muted-foreground">{p.period}</div>
            </div>
            <p className="mt-2 text-sm text-muted-foreground">{p.desc}</p>
            <ul className="mt-6 space-y-2.5 text-sm">
              {p.features.map((f) => (
                <li key={f} className="flex gap-2">
                  <Check className="mt-0.5 h-4 w-4 shrink-0 text-success" />
                  <span>{f}</span>
                </li>
              ))}
            </ul>
            <Button asChild className={`mt-8 w-full ${p.highlight ? "bg-gradient-primary text-white shadow-glow hover:opacity-90" : ""}`} variant={p.highlight ? "default" : "outline"}>
              <Link to="/register">{p.cta}</Link>
            </Button>
          </Card>
        ))}
      </div>
    </section>
  );
}

function FAQ() {
  return (
    <section className="mx-auto max-w-3xl px-6 py-24">
      <SectionHeading eyebrow="FAQ" title="Questions, answered." />
      <Accordion type="single" collapsible className="mt-10">
        {faqs.map((f, i) => (
          <AccordionItem key={i} value={`i-${i}`} className="border-border/70">
            <AccordionTrigger className="text-left text-base hover:no-underline">{f.q}</AccordionTrigger>
            <AccordionContent className="text-muted-foreground">{f.a}</AccordionContent>
          </AccordionItem>
        ))}
      </Accordion>
    </section>
  );
}

function CTA() {
  return (
    <section className="mx-auto max-w-6xl px-6 py-16">
      <div className="glass relative overflow-hidden rounded-3xl p-12 text-center shadow-elegant">
        <div className="absolute inset-0 -z-10 bg-gradient-hero opacity-70" />
        <Zap className="mx-auto mb-4 h-8 w-8 text-primary" />
        <h2 className="text-3xl font-semibold sm:text-4xl">Ready to see your first shortlist?</h2>
        <p className="mx-auto mt-3 max-w-xl text-muted-foreground">
          Start free. Upload a resume or a job description — get a full AI report in under 60 seconds.
        </p>
        <div className="mt-6 flex flex-wrap justify-center gap-3">
          <Button asChild size="lg" className="bg-gradient-primary text-white shadow-glow hover:opacity-90">
            <Link to="/register">Start free <ArrowRight className="ml-1 h-4 w-4" /></Link>
          </Button>
          <Button asChild size="lg" variant="outline">
            <Link to="/recruiter">See recruiter demo</Link>
          </Button>
        </div>
      </div>
    </section>
  );
}

function SectionHeading({ eyebrow, title }: { eyebrow: string; title: React.ReactNode }) {
  return (
    <div className="text-center">
      <div className="text-xs font-semibold uppercase tracking-widest text-primary">{eyebrow}</div>
      <h2 className="mt-3 text-4xl font-semibold tracking-tight sm:text-5xl">{title}</h2>
    </div>
  );
}

// tiny placeholder to satisfy TS about BarChart3 import
void BarChart3;

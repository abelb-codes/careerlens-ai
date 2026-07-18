import { createFileRoute, Link } from "@tanstack/react-router";
import { MarketingNav, MarketingFooter } from "@/components/marketing/nav";
import { features } from "@/lib/mock";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import * as Icons from "lucide-react";

export const Route = createFileRoute("/features")({
  head: () => ({ meta: [{ title: "Features — CareerLens AI" }] }),
  component: FeaturesPage,
});

function FeaturesPage() {
  return (
    <div className="relative min-h-screen bg-background">
      <div className="pointer-events-none absolute inset-x-0 top-0 h-[500px] bg-gradient-hero opacity-70" />
      <div className="relative">
        <MarketingNav />
        <section className="mx-auto max-w-4xl px-6 pt-20 pb-12 text-center">
          <div className="text-xs font-semibold uppercase tracking-widest text-primary">Features</div>
          <h1 className="mt-3 text-5xl font-semibold tracking-tight">Everything you need to hire, <span className="font-display italic text-gradient">and be hired.</span></h1>
          <p className="mx-auto mt-4 max-w-xl text-muted-foreground">An AI-first platform designed for both sides of the recruiting table.</p>
        </section>
        <section className="mx-auto grid max-w-6xl gap-4 px-6 pb-20 sm:grid-cols-2 lg:grid-cols-3">
          {features.map((f) => {
            const Icon = (Icons as unknown as Record<string, React.ComponentType<{ className?: string }>>)[f.icon];
            return (
              <Card key={f.title} className="border-border/70 bg-gradient-card p-6">
                <div className="mb-4 grid h-10 w-10 place-items-center rounded-xl bg-primary/10 text-primary ring-1 ring-primary/20">
                  {Icon && <Icon className="h-5 w-5" />}
                </div>
                <div className="text-base font-semibold">{f.title}</div>
                <p className="mt-2 text-sm text-muted-foreground">{f.desc}</p>
              </Card>
            );
          })}
        </section>
        <div className="mx-auto max-w-3xl px-6 pb-20 text-center">
          <Button asChild size="lg" className="bg-gradient-primary text-white shadow-glow hover:opacity-90"><Link to="/register">Try it free</Link></Button>
        </div>
        <MarketingFooter />
      </div>
    </div>
  );
}
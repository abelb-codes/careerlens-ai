import { createFileRoute, Link } from "@tanstack/react-router";
import { MarketingNav, MarketingFooter } from "@/components/marketing/nav";
import { pricing } from "@/lib/mock";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Check } from "lucide-react";

export const Route = createFileRoute("/pricing")({
  head: () => ({ meta: [{ title: "Pricing — CareerLens AI" }] }),
  component: PricingPage,
});

function PricingPage() {
  return (
    <div className="relative min-h-screen bg-background">
      <div className="pointer-events-none absolute inset-x-0 top-0 h-[500px] bg-gradient-hero opacity-70" />
      <div className="relative">
        <MarketingNav />
        <section className="mx-auto max-w-4xl px-6 pt-20 pb-8 text-center">
          <div className="text-xs font-semibold uppercase tracking-widest text-primary">Pricing</div>
          <h1 className="mt-3 text-5xl font-semibold tracking-tight">Fair, transparent, <span className="font-display italic text-gradient">no seats games.</span></h1>
        </section>
        <section className="mx-auto grid max-w-6xl gap-4 px-6 py-12 md:grid-cols-3">
          {pricing.map((p) => (
            <Card key={p.name} className={`relative flex flex-col border-border/70 bg-gradient-card p-8 ${p.highlight ? "border-primary/50 shadow-glow" : ""}`}>
              {p.highlight && <Badge className="absolute -top-3 left-1/2 -translate-x-1/2 bg-gradient-primary text-white">Most popular</Badge>}
              <div className="text-sm font-medium text-muted-foreground">{p.name}</div>
              <div className="mt-3 flex items-baseline gap-1">
                <div className="text-4xl font-semibold tracking-tight">{p.price}</div>
                <div className="text-sm text-muted-foreground">{p.period}</div>
              </div>
              <p className="mt-2 text-sm text-muted-foreground">{p.desc}</p>
              <ul className="mt-6 space-y-2.5 text-sm">
                {p.features.map((f) => (<li key={f} className="flex gap-2"><Check className="mt-0.5 h-4 w-4 shrink-0 text-success" /><span>{f}</span></li>))}
              </ul>
              <Button asChild className={`mt-8 w-full ${p.highlight ? "bg-gradient-primary text-white shadow-glow hover:opacity-90" : ""}`} variant={p.highlight ? "default" : "outline"}>
                <Link to="/register">{p.cta}</Link>
              </Button>
            </Card>
          ))}
        </section>
        <MarketingFooter />
      </div>
    </div>
  );
}
import { createFileRoute } from "@tanstack/react-router";
import { MarketingNav, MarketingFooter } from "@/components/marketing/nav";

export const Route = createFileRoute("/about")({
  head: () => ({ meta: [{ title: "About — CareerLens AI" }] }),
  component: About,
});

function About() {
  return (
    <div className="relative min-h-screen bg-background">
      <div className="pointer-events-none absolute inset-x-0 top-0 h-[500px] bg-gradient-hero opacity-70" />
      <div className="relative">
        <MarketingNav />
        <section className="mx-auto max-w-3xl px-6 pt-20 pb-24">
          <div className="text-xs font-semibold uppercase tracking-widest text-primary">About</div>
          <h1 className="mt-3 text-5xl font-semibold tracking-tight">Hiring should be <span className="font-display italic text-gradient">honest.</span></h1>
          <div className="mt-8 space-y-6 text-lg leading-relaxed text-muted-foreground">
            <p>CareerLens AI was built by ex-recruiters and ML engineers who were tired of black-box screening tools and resume parsers that couldn't read a table.</p>
            <p>We believe hiring works best when both sides — the applicant and the team — see the same signal. So every score we generate comes with reasoning, sources, and confidence.</p>
            <p>We serve 3,200 teams across 40 countries, processing over 1.4M resumes to date. And we've never — not once — sold candidate data.</p>
          </div>
        </section>
        <MarketingFooter />
      </div>
    </div>
  );
}
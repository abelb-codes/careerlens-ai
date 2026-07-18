import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/app/shell";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { toast } from "sonner";

export const Route = createFileRoute("/app/profile")({
  head: () => ({ meta: [{ title: "Profile — CareerLens AI" }] }),
  component: Profile,
});

function Profile() {
  return (
    <div>
      <PageHeader eyebrow="Profile" title="Your profile" description="Used to tailor AI recommendations." />
      <Card className="max-w-3xl border-border/70 bg-gradient-card p-6">
        <form onSubmit={(e) => { e.preventDefault(); toast.success("Profile saved"); }} className="grid gap-4 sm:grid-cols-2">
          <div><Label>Full name</Label><Input defaultValue="Sofia Alvarez" className="mt-1.5" /></div>
          <div><Label>Headline</Label><Input defaultValue="Senior Product Designer" className="mt-1.5" /></div>
          <div><Label>Email</Label><Input defaultValue="sofia@studio.co" className="mt-1.5" /></div>
          <div><Label>Location</Label><Input defaultValue="Lisbon, PT" className="mt-1.5" /></div>
          <div className="sm:col-span-2"><Label>Bio</Label><Textarea rows={4} defaultValue="Designer focused on B2B SaaS, design systems, and onboarding. Previously at Kepler and Aperture." className="mt-1.5" /></div>
          <div className="sm:col-span-2 flex justify-end gap-2"><Button variant="outline">Cancel</Button><Button className="bg-gradient-primary text-white shadow-glow hover:opacity-90">Save changes</Button></div>
        </form>
      </Card>
    </div>
  );
}
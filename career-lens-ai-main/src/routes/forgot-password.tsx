import { createFileRoute, Link } from "@tanstack/react-router";
import { AuthShell } from "@/components/marketing/auth-shell";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";

export const Route = createFileRoute("/forgot-password")({
  head: () => ({ meta: [{ title: "Reset password — CareerLens AI" }] }),
  component: Forgot,
});

function Forgot() {
  return (
    <AuthShell title="Reset your password" subtitle="We'll email you a secure link." footer={<Link to="/login" className="hover:text-foreground">Back to sign in</Link>}>
      <form onSubmit={(e) => { e.preventDefault(); toast.success("Check your inbox for a reset link."); }} className="space-y-4">
        <div className="space-y-1.5"><Label>Email</Label><Input type="email" required defaultValue="you@company.com" /></div>
        <Button className="w-full bg-gradient-primary text-white shadow-glow hover:opacity-90">Send reset link</Button>
      </form>
    </AuthShell>
  );
}
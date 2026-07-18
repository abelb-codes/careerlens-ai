import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { AuthShell } from "@/components/marketing/auth-shell";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { toast } from "sonner";
import { useState } from "react";
import api from "@/api/axios";
import { setTokens } from "@/lib/auth";

export const Route = createFileRoute("/register")({
  head: () => ({ meta: [{ title: "Create account — CareerLens AI" }] }),
  component: Register,
});

function Register() {
  const navigate = useNavigate();
  const [role, setRole] = useState<"applicant" | "recruiter">("applicant");
  const [loading, setLoading] = useState(false);
  const [firstName, setFirstName] = useState("Sofia");
  const [lastName, setLastName] = useState("Alvarez");
  const [email, setEmail] = useState("sofia@studio.co");
  const [password, setPassword] = useState("Password123!");
  const [password2, setPassword2] = useState("Password123!");

  const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);

    try {
      const { data } = await api.post("/api/auth/register/", {
        email,
        username: email,
        first_name: firstName,
        last_name: lastName,
        role: role === "recruiter" ? "recruiter" : "candidate",
        password,
        password2,
      });

      setTokens(data.access, data.refresh);
      toast.success("Account created");
      navigate({ to: role === "recruiter" ? "/recruiter" : "/app" });
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : "Registration failed";
      toast.error(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthShell
      title="Create your account"
      subtitle="Free forever for applicants. 14-day trial for teams."
      footer={<>Already have an account? <Link to="/login" className="text-foreground hover:underline">Sign in</Link></>}
    >
      <form onSubmit={onSubmit} className="space-y-4">
        <div className="grid grid-cols-2 gap-2">
          <div className="space-y-1.5"><Label>First name</Label><Input required value={firstName} onChange={(e) => setFirstName(e.target.value)} /></div>
          <div className="space-y-1.5"><Label>Last name</Label><Input required value={lastName} onChange={(e) => setLastName(e.target.value)} /></div>
        </div>
        <div className="space-y-1.5"><Label>Work email</Label><Input type="email" required value={email} onChange={(e) => setEmail(e.target.value)} /></div>
        <div className="space-y-1.5"><Label>Password</Label><Input type="password" required value={password} onChange={(e) => setPassword(e.target.value)} /></div>
        <div className="space-y-1.5"><Label>Confirm password</Label><Input type="password" required value={password2} onChange={(e) => setPassword2(e.target.value)} /></div>
        <div className="space-y-2">
          <Label>I am a</Label>
          <RadioGroup value={role} onValueChange={(v) => setRole(v as "applicant" | "recruiter")} className="grid grid-cols-2 gap-2">
            {(["applicant", "recruiter"] as const).map((r) => (
              <Label key={r} htmlFor={`r-${r}`} className={`flex cursor-pointer items-center gap-2 rounded-lg border p-3 text-sm capitalize transition ${role === r ? "border-primary bg-primary/5" : "border-border"}`}>
                <RadioGroupItem value={r} id={`r-${r}`} />
                {r}
              </Label>
            ))}
          </RadioGroup>
        </div>
        <Button type="submit" className="w-full bg-gradient-primary text-white shadow-glow hover:opacity-90" disabled={loading}>{loading ? "Creating account..." : "Create account"}</Button>
      </form>
    </AuthShell>
  );
}
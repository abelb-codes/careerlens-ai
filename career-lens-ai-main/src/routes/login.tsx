import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { AuthShell } from "@/components/marketing/auth-shell";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { Github, Chrome } from "lucide-react";
import { toast } from "sonner";
import { useState } from "react";
import api from "@/api/axios";
import { setTokens } from "@/lib/auth";

function getLoginErrorMessage(error: unknown): string {
  if (typeof error === "object" && error !== null && "response" in error) {
    const response = (
      error as {
        response?: { data?: { detail?: string; non_field_errors?: string[] } };
      }
    ).response;
    if (response?.data?.detail) return response.data.detail;
    if (response?.data?.non_field_errors?.[0]) return response.data.non_field_errors[0];
    return "Sign-in failed. Check your email and password.";
  }
  if (typeof error === "object" && error !== null && "request" in error) {
    return "CareerLens cannot reach the API. Start Django on http://127.0.0.1:8000 and try again.";
  }
  return "Sign-in failed. Please try again.";
}

export const Route = createFileRoute("/login")({
  head: () => ({ meta: [{ title: "Login — CareerLens AI" }] }),
  component: Login,
});

function Login() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [email, setEmail] = useState("demo@careerlens.ai");
  const [password, setPassword] = useState("demopass");

  const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);

    try {
      const { data } = await api.post("/api/auth/login/", { email, password });
      setTokens(data.access, data.refresh);
      toast.success("Signed in");
      navigate({ to: "/app" });
    } catch (error: unknown) {
      toast.error(getLoginErrorMessage(error));
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthShell
      title="Welcome back"
      subtitle="Log in to continue to your dashboard."
      footer={
        <>
          New here?{" "}
          <Link to="/register" className="text-foreground hover:underline">
            Create an account
          </Link>
        </>
      }
    >
      <form onSubmit={onSubmit} className="space-y-4">
        <div className="grid grid-cols-2 gap-2">
          <Button type="button" variant="outline" className="w-full">
            <Chrome className="mr-2 h-4 w-4" />
            Google
          </Button>
          <Button type="button" variant="outline" className="w-full">
            <Github className="mr-2 h-4 w-4" />
            GitHub
          </Button>
        </div>
        <div className="relative">
          <Separator />
          <span className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 bg-card px-2 text-xs text-muted-foreground">
            or
          </span>
        </div>
        <div className="space-y-1.5">
          <Label htmlFor="e">Email</Label>
          <Input
            id="e"
            type="email"
            required
            placeholder="you@company.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div className="space-y-1.5">
          <div className="flex items-center justify-between">
            <Label htmlFor="p">Password</Label>
            <Link
              to="/forgot-password"
              className="text-xs text-muted-foreground hover:text-foreground"
            >
              Forgot?
            </Link>
          </div>
          <Input
            id="p"
            type="password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <Button
          type="submit"
          className="w-full bg-gradient-primary text-white shadow-glow hover:opacity-90"
          disabled={loading}
        >
          {loading ? "Signing in..." : "Sign in"}
        </Button>
      </form>
    </AuthShell>
  );
}

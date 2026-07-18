import { createFileRoute, Outlet, redirect } from "@tanstack/react-router";
import { AppShell, type NavItem } from "@/components/app/shell";
import { LayoutDashboard, Briefcase, Workflow, Users, FileBarChart2, BarChart3, Settings } from "lucide-react";
import { isAuthenticated } from "@/lib/auth";

const nav: NavItem[] = [
  { to: "/recruiter", label: "Dashboard", icon: LayoutDashboard },
  { to: "/recruiter/jobs", label: "Job Descriptions", icon: Briefcase },
  { to: "/recruiter/evaluations", label: "Evaluation Sessions", icon: Workflow, badge: "New" },
  { to: "/recruiter/candidates", label: "Candidates", icon: Users },
  { to: "/recruiter/reports", label: "Reports", icon: FileBarChart2 },
  { to: "/recruiter/analytics", label: "Analytics", icon: BarChart3 },
  { to: "/recruiter/settings", label: "Settings", icon: Settings },
];

export const Route = createFileRoute("/recruiter")({
  head: () => ({ meta: [{ title: "Recruiter — CareerLens AI" }] }),
  beforeLoad: () => {
    if (typeof window !== "undefined" && !isAuthenticated()) {
      throw redirect({ to: "/login" });
    }
  },
  component: RecruiterLayout,
});

function RecruiterLayout() {
  return (
    <AppShell workspace="Northwind" role="Recruiter" nav={nav} user={{ name: "Priya Rao", email: "priya@northwind.co" }}>
      <Outlet />
    </AppShell>
  );
}

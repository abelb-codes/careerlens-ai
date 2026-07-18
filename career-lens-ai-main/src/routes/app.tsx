import { createFileRoute, Outlet, redirect } from "@tanstack/react-router";
import { AppShell, type NavItem } from "@/components/app/shell";
import {
  LayoutDashboard,
  Upload,
  History,
  FileBarChart2,
  User,
  Settings,
} from "lucide-react";
import { isAuthenticated } from "@/lib/auth";

const nav: NavItem[] = [
  { to: "/app/", label: "Dashboard", icon: LayoutDashboard },
  { to: "/app/upload", label: "Upload Resume", icon: Upload },
  { to: "/app/history", label: "Resume History", icon: History },
  { to: "/app/reports", label: "Analysis Reports", icon: FileBarChart2 },
  { to: "/app/profile", label: "Profile", icon: User },
  { to: "/app/settings", label: "Settings", icon: Settings },
];

export const Route = createFileRoute("/app")({
  head: () => ({
    meta: [{ title: "Dashboard — CareerLens AI" }],
  }),
  beforeLoad: () => {
    if (typeof window !== "undefined" && !isAuthenticated()) {
      throw redirect({ to: "/login" });
    }
  },
  component: AppLayout,
});

function AppLayout() {
  return (
    <AppShell
      workspace="CareerLens"
      role="Applicant"
      nav={nav}
      user={{
        name: "Sofia Alvarez",
        email: "sofia@studio.co",
      }}
    >
      <Outlet />
    </AppShell>
  );
}

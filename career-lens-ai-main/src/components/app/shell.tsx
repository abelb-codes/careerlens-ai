import { Link, useRouterState } from "@tanstack/react-router";
import type { ReactNode } from "react";
import { Sparkles, Bell, Search, ChevronDown } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";

export type NavItem = { to: string; label: string; icon: React.ComponentType<{ className?: string }>; badge?: string };

export function AppShell({
  workspace,
  role,
  nav,
  user,
  children,
}: {
  workspace: string;
  role: string;
  nav: NavItem[];
  user: { name: string; email: string };
  children: ReactNode;
}) {
  const pathname = useRouterState({ select: (s) => s.location.pathname });
  return (
    <div className="min-h-screen bg-background text-foreground">
      <div className="mx-auto flex min-h-screen w-full max-w-[1600px]">
        <aside className="sticky top-0 hidden h-screen w-64 shrink-0 border-r border-border/60 bg-sidebar md:flex md:flex-col">
          <div className="flex items-center gap-2 px-5 py-5">
            <div className="grid h-8 w-8 place-items-center rounded-lg bg-gradient-primary shadow-glow">
              <Sparkles className="h-4 w-4 text-white" />
            </div>
            <div className="min-w-0">
              <div className="truncate text-sm font-semibold">{workspace}</div>
              <div className="text-[10px] uppercase tracking-widest text-muted-foreground">{role}</div>
            </div>
          </div>
          <nav className="flex-1 space-y-0.5 px-3">
            {nav.map((item) => {
              const active = pathname === item.to || (item.to !== "/app" && item.to !== "/recruiter" && pathname.startsWith(item.to));
              return (
                <Link
                  key={item.to}
                  to={item.to}
                  className={`flex items-center gap-2.5 rounded-lg px-3 py-2 text-sm transition ${
                    active
                      ? "bg-primary/10 text-foreground shadow-inner ring-1 ring-primary/20"
                      : "text-muted-foreground hover:bg-sidebar-accent hover:text-foreground"
                  }`}
                >
                  <item.icon className={`h-4 w-4 ${active ? "text-primary" : ""}`} />
                  <span className="flex-1">{item.label}</span>
                  {item.badge && <Badge variant="secondary" className="h-5 px-1.5 text-[10px]">{item.badge}</Badge>}
                </Link>
              );
            })}
          </nav>
          <div className="border-t border-border/60 p-3">
            <div className="glass rounded-lg p-3">
              <div className="text-xs font-medium">Pro trial · 12 days left</div>
              <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-secondary">
                <div className="h-full bg-gradient-primary" style={{ width: "60%" }} />
              </div>
              <button className="mt-2 text-xs text-primary hover:underline">Upgrade →</button>
            </div>
          </div>
        </aside>
        <div className="flex min-w-0 flex-1 flex-col">
          <header className="sticky top-0 z-30 flex h-14 items-center gap-3 border-b border-border/60 bg-background/70 px-4 backdrop-blur md:px-6">
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-2.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input placeholder="Search resumes, candidates, jobs..." className="h-9 border-border/70 bg-secondary/40 pl-8 text-sm" />
              <kbd className="pointer-events-none absolute right-2 top-1/2 hidden -translate-y-1/2 rounded border border-border bg-background px-1.5 py-0.5 text-[10px] text-muted-foreground sm:inline">⌘K</kbd>
            </div>
            <button className="relative rounded-md p-2 text-muted-foreground hover:bg-secondary hover:text-foreground">
              <Bell className="h-4 w-4" />
              <span className="absolute right-1.5 top-1.5 h-1.5 w-1.5 rounded-full bg-primary" />
            </button>
            <DropdownMenu>
              <DropdownMenuTrigger className="flex items-center gap-2 rounded-md p-1 pr-2 text-sm hover:bg-secondary">
                <div className="grid h-7 w-7 place-items-center rounded-full bg-gradient-primary text-xs font-semibold text-white">
                  {user.name.split(" ").map(n => n[0]).join("")}
                </div>
                <span className="hidden md:inline">{user.name}</span>
                <ChevronDown className="h-3.5 w-3.5 text-muted-foreground" />
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-56">
                <DropdownMenuLabel>
                  <div className="text-sm">{user.name}</div>
                  <div className="text-xs text-muted-foreground">{user.email}</div>
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem asChild><Link to="/app/profile">Profile</Link></DropdownMenuItem>
                <DropdownMenuItem asChild><Link to="/app/settings">Settings</Link></DropdownMenuItem>
                <DropdownMenuItem asChild><Link to="/recruiter">Switch to recruiter</Link></DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem asChild><Link to="/">Log out</Link></DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </header>
          <main className="flex-1 p-4 md:p-8">{children}</main>
        </div>
      </div>
    </div>
  );
}

export function PageHeader({ eyebrow, title, description, actions }: { eyebrow?: string; title: string; description?: string; actions?: ReactNode }) {
  return (
    <div className="mb-8 flex flex-wrap items-end justify-between gap-4">
      <div>
        {eyebrow && <div className="text-xs font-semibold uppercase tracking-widest text-primary">{eyebrow}</div>}
        <h1 className="mt-1 text-2xl font-semibold tracking-tight sm:text-3xl">{title}</h1>
        {description && <p className="mt-1 text-sm text-muted-foreground">{description}</p>}
      </div>
      {actions && <div className="flex items-center gap-2">{actions}</div>}
    </div>
  );
}

export function StatCard({ label, value, delta, hint }: { label: string; value: string; delta?: string; hint?: string }) {
  const positive = delta?.startsWith("+");
  return (
    <div className="rounded-2xl border border-border/70 bg-gradient-card p-5">
      <div className="text-xs uppercase tracking-wider text-muted-foreground">{label}</div>
      <div className="mt-2 flex items-baseline gap-2">
        <div className="text-2xl font-semibold tabular-nums">{value}</div>
        {delta && <span className={`text-xs font-medium ${positive ? "text-success" : "text-destructive"}`}>{delta}</span>}
      </div>
      {hint && <div className="mt-1 text-xs text-muted-foreground">{hint}</div>}
    </div>
  );
}

export function ScoreRing({ value, size = 96, label }: { value: number; size?: number; label?: string }) {
  const stroke = 8;
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  const off = c - (value / 100) * c;
  return (
    <div className="relative inline-flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={r} strokeWidth={stroke} stroke="oklch(1 0 0 / 0.08)" fill="none" />
        <circle
          cx={size / 2} cy={size / 2} r={r} strokeWidth={stroke}
          stroke="url(#g)" fill="none"
          strokeDasharray={c} strokeDashoffset={off} strokeLinecap="round"
          style={{ transition: "stroke-dashoffset 800ms ease" }}
        />
        <defs>
          <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="oklch(0.66 0.19 258)" />
            <stop offset="100%" stopColor="oklch(0.62 0.22 295)" />
          </linearGradient>
        </defs>
      </svg>
      <div className="absolute text-center">
        <div className="text-xl font-semibold tabular-nums">{value}</div>
        {label && <div className="text-[10px] uppercase tracking-widest text-muted-foreground">{label}</div>}
      </div>
    </div>
  );
}
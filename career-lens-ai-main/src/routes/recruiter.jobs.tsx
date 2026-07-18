import { createFileRoute, Outlet } from "@tanstack/react-router";
export const Route = createFileRoute("/recruiter/jobs")({ component: () => <Outlet /> });
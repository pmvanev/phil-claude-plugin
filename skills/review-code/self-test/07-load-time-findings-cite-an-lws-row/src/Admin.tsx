import { lazy, Suspense } from "react";

export default function Admin() {
  const UsageChart = lazy(() => import("./UsageChart"));
  return (
    <Suspense fallback={<p>Loading usage…</p>}>
      <h1>Admin</h1>
      <UsageChart />
    </Suspense>
  );
}

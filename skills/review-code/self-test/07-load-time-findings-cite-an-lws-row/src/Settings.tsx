import { lazy, Suspense, useState } from "react";

const SettingsHelp = lazy(() => import("./SettingsHelp"));

export default function Settings() {
  const [showHelp, setShowHelp] = useState(false);
  return (
    <section>
      <h1>Settings</h1>
      <button type="button" onClick={() => setShowHelp(true)}>Help</button>
      {showHelp && (
        <Suspense fallback={<p>Loading help…</p>}>
          <SettingsHelp />
        </Suspense>
      )}
    </section>
  );
}

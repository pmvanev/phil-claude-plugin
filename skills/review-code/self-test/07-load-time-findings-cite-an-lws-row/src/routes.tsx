import { createBrowserRouter } from "react-router";

import Admin from "./Admin";
import Home from "./Home";
import Reports from "./Reports";
import Settings from "./Settings";

export const router = createBrowserRouter([
  { path: "/", Component: Home },
  { path: "/reports", Component: Reports },
  { path: "/settings", Component: Settings },
  { path: "/admin", Component: Admin },
]);

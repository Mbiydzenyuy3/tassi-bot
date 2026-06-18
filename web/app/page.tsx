import { redirect } from "next/navigation";

// Root redirects to French by default (SRS FR-CHAT-4)
export default function Root() {
  redirect("/fr");
}

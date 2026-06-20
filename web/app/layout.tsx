import type { Metadata, Viewport } from "next";
import { headers } from "next/headers";
import "./globals.css";

export const viewport: Viewport = {
  themeColor: "#052e16",
};

const icons: Metadata["icons"] = {
  icon: "/icon.svg",
  apple: "/apple-icon.svg",
};

export async function generateMetadata(): Promise<Metadata> {
  let pathname = "";
  try { pathname = (await headers()).get("x-pathname") ?? ""; } catch {}
  const isEn = pathname.startsWith("/en");

  if (isEn) {
    return {
      title: "Tassi — Simplified Tax Regime (RSI) on WhatsApp",
      icons,
      description:
        "Tassi calculates your RSI (Simplified Tax Regime) tax on WhatsApp. Get your RSI advance payment, CAC contribution, and total due in under 3 seconds. In French, English, or Pidgin. For Cameroon RSI businesses.",
      keywords: [
        "RSI Cameroon",
        "Simplified Tax Regime",
        "RSI WhatsApp calculator",
        "Cameroon tax WhatsApp",
        "acompte RSI",
        "Cameroon Tax Center",
      ],
      openGraph: {
        title: "Tassi — RSI Calculation on WhatsApp",
        description:
          "Your RSI (Simplified Tax Regime) tax calculated on WhatsApp. Free. Available 24/7 in French, English, and Pidgin.",
        type: "website",
        locale: "en_CM",
      },
      twitter: {
        card: "summary_large_image",
        title: "Tassi — RSI on WhatsApp",
        description:
          "Simplified Tax Regime (RSI) calculation on WhatsApp for Cameroonian businesses.",
      },
    };
  }

  return {
    title: "Tassi — Régime Simplifié d'Imposition (RSI) sur WhatsApp",
    icons,
    description:
      "Tassi calcule votre impôt RSI (Régime Simplifié d'Imposition) sur WhatsApp. Obtenez votre acompte RSI, votre part CAC et votre total à payer en moins de 3 secondes. En français, anglais ou pidgin. Pour les entreprises RSI du Cameroun.",
    keywords: [
      "RSI Cameroun",
      "Régime Simplifié d'Imposition",
      "calcul impôt RSI WhatsApp",
      "RSI calculator Cameroon",
      "Simplified Tax Regime Cameroon",
      "acompte RSI",
      "Centre des Impôts Cameroun",
    ],
    openGraph: {
      title: "Tassi — Calcul RSI sur WhatsApp",
      description:
        "Votre impôt RSI (Régime Simplifié d'Imposition) calculé sur WhatsApp. Gratuit. Disponible 24h/24 en français, anglais et pidgin.",
      type: "website",
      locale: "fr_CM",
    },
    twitter: {
      card: "summary_large_image",
      title: "Tassi — RSI sur WhatsApp",
      description:
        "Calcul du Régime Simplifié d'Imposition (RSI) sur WhatsApp pour les entreprises camerounaises.",
    },
  };
}

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  let pathname = "";
  try { pathname = (await headers()).get("x-pathname") ?? ""; } catch {}
  const lang = pathname.startsWith("/en") ? "en" : "fr";

  return (
    <html lang={lang} suppressHydrationWarning>
      <body className="font-sans antialiased bg-white text-gray-900" suppressHydrationWarning>
        <a href="#main-content" className="skip-to-content">
          Aller au contenu principal
        </a>
        <div id="main-content">
          {children}
        </div>
      </body>
    </html>
  );
}

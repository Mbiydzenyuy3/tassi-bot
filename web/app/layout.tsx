import type { Metadata, Viewport } from "next";
import "./globals.css";

export const viewport: Viewport = {
  themeColor: "#052e16",
};

export const metadata: Metadata = {
  title: "Tassi — Régime Simplifié d'Imposition (RSI) sur WhatsApp",
  icons: {
    icon: "/icon.svg",
    apple: "/apple-icon.svg",
  },
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

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr">
      <body className="font-sans antialiased bg-white text-gray-900">
        {children}
      </body>
    </html>
  );
}

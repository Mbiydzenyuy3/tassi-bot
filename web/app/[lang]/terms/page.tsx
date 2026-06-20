import Link from "next/link";
import type { Lang } from "@/lib/i18n";
import { notFound } from "next/navigation";

export function generateStaticParams() {
  return [{ lang: "fr" }, { lang: "en" }];
}

export default async function TermsPage({ params }: { params: Promise<{ lang: string }> }) {
  const { lang } = await params;
  if (lang !== "fr" && lang !== "en") notFound();

  const isFr = lang === "fr";

  return (
    <main className="min-h-screen bg-white">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 xl:px-8 py-24">
        <Link href={`/${lang}`} className="inline-flex items-center gap-2 text-forest-600 hover:text-forest-700 text-sm font-medium mb-10">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          {isFr ? "Retour à l'accueil" : "Back to home"}
        </Link>

        <h1 className="text-3xl xl:text-4xl font-extrabold text-gray-900 mb-3">
          {isFr ? "Conditions d'utilisation" : "Terms of Use"}
        </h1>
        <p className="text-gray-400 text-sm mb-10">{isFr ? "Dernière mise à jour : juin 2025" : "Last updated: June 2025"}</p>

        <div className="prose prose-gray max-w-none space-y-8 text-gray-600">
          <section>
            <h2 className="text-xl font-bold text-gray-900 mb-3">
              {isFr ? "Le service" : "The service"}
            </h2>
            <p>
              {isFr
                ? "Tassi est un assistant WhatsApp qui calcule l'acompte RSI (Régime Simplifié d'Imposition) pour les entreprises camerounaises. Les résultats sont basés sur le barème officiel publié par la Direction Générale des Impôts (DGI) du Cameroun."
                : "Tassi is a WhatsApp assistant that calculates the RSI acompte (Simplified Tax Regime) for Cameroonian businesses. Results are based on the official schedule published by Cameroon's Direction Générale des Impôts (DGI)."}
            </p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-gray-900 mb-3">
              {isFr ? "Limites de responsabilité" : "Limitations"}
            </h2>
            <p>
              {isFr
                ? "Tassi fournit un calcul indicatif basé sur les taux DGI en vigueur. Il ne remplace pas un conseiller fiscal agréé. Pour les situations complexes (activités multiples, changement de régime fiscal, contentieux), consultez un expert-comptable ou votre Centre des Impôts."
                : "Tassi provides an indicative calculation based on current DGI rates. It is not a substitute for a licensed tax adviser. For complex situations (multiple activities, regime changes, disputes), consult a certified accountant or your Centre des Impôts."}
            </p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-gray-900 mb-3">
              {isFr ? "Tassi Plus — abonnement" : "Tassi Plus — subscription"}
            </h2>
            <p>
              {isFr
                ? "Tassi Plus est un abonnement mensuel de 500 XAF payé via MTN MoMo ou Orange Money. Il se renouvelle automatiquement chaque mois. Pour annuler, envoyez ANNULER dans le chat WhatsApp. L'annulation prend effet à la fin du mois en cours."
                : "Tassi Plus is a monthly subscription of 500 XAF paid via MTN MoMo or Orange Money. It renews automatically each month. To cancel, send CANCEL in the WhatsApp chat. Cancellation takes effect at the end of the current billing month."}
            </p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-gray-900 mb-3">Contact</h2>
            <p>
              {isFr
                ? "Pour toute question sur ces conditions, contactez-nous directement via WhatsApp."
                : "For any question about these terms, contact us directly via WhatsApp."}
            </p>
          </section>
        </div>
      </div>
    </main>
  );
}

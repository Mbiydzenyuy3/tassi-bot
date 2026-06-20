import Link from "next/link";
import type { Lang } from "@/lib/i18n";
import { notFound } from "next/navigation";

export function generateStaticParams() {
  return [{ lang: "fr" }, { lang: "en" }];
}

export default async function PrivacyPage({ params }: { params: Promise<{ lang: string }> }) {
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
          {isFr ? "Politique de confidentialité" : "Privacy Policy"}
        </h1>
        <p className="text-gray-400 text-sm mb-10">{isFr ? "Dernière mise à jour : juin 2025" : "Last updated: June 2025"}</p>

        <div className="prose prose-gray max-w-none space-y-8 text-gray-600">
          <section>
            <h2 className="text-xl font-bold text-gray-900 mb-3">
              {isFr ? "Ce que nous collectons" : "What we collect"}
            </h2>
            <p>
              {isFr
                ? "Pour le plan Gratuit, Tassi ne conserve aucune donnée. Chaque calcul est traité en temps réel et immédiatement supprimé. Nous ne stockons ni votre numéro de téléphone, ni votre chiffre d'affaires, ni aucun résultat de calcul."
                : "On the Free plan, Tassi stores no data. Every calculation is processed in real time and immediately discarded. We do not store your phone number, your revenue, or any calculation result."}
            </p>
            <p className="mt-3">
              {isFr
                ? "Pour le plan Tassi Plus, nous conservons votre historique de calcul (chiffres d'affaires mensuel et résultats RSI) afin de vous permettre de le consulter. Ces données sont liées à votre numéro WhatsApp uniquement."
                : "On Tassi Plus, we retain your calculation history (monthly revenue figures and RSI results) so you can retrieve them. This data is linked to your WhatsApp number only."}
            </p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-gray-900 mb-3">
              {isFr ? "Comment nous utilisons vos données" : "How we use your data"}
            </h2>
            <p>
              {isFr
                ? "Vos données ne sont jamais vendues, partagées ou transmises à des tiers. Elles sont utilisées uniquement pour répondre à vos messages et, pour Tassi Plus, pour maintenir votre historique de calcul."
                : "Your data is never sold, shared, or transmitted to third parties. It is used only to respond to your messages and, for Tassi Plus, to maintain your calculation history."}
            </p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-gray-900 mb-3">
              {isFr ? "Supprimer vos données" : "Delete your data"}
            </h2>
            <p>
              {isFr
                ? "Pour demander la suppression de vos données (Tassi Plus uniquement), envoyez SUPPRIMER dans le chat WhatsApp. Vos données seront effacées dans les 24 heures."
                : "To request deletion of your data (Tassi Plus only), send DELETE in the WhatsApp chat. Your data will be erased within 24 hours."}
            </p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-gray-900 mb-3">Contact</h2>
            <p>
              {isFr
                ? "Pour toute question relative à la confidentialité, contactez-nous directement via WhatsApp."
                : "For any privacy-related question, contact us directly via WhatsApp."}
            </p>
          </section>
        </div>
      </div>
    </main>
  );
}

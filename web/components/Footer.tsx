import Link from "next/link";
import { WHATSAPP_URL } from "@/lib/constants";
import type { Copy, Lang } from "@/lib/i18n";

function TassiLogo() {
  return (
    <svg width="36" height="36" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="Tassi logo">
      {/* Outer arc */}
      <path
        d="M 31,6.14 A 16,16 0 1,0 31,33.86"
        stroke="white"
        strokeWidth="4"
        strokeLinecap="round"
      />
      {/* Inner arc */}
      <path
        d="M 28,11.34 A 10,10 0 1,0 28,28.66"
        stroke="white"
        strokeWidth="3.5"
        strokeLinecap="round"
      />
    </svg>
  );
}

export default function Footer({ t, lang }: { t: Copy["footer"]; lang: Lang }) {
  const dgiUrl = "https://www.impots.cm";

  const footerCols = [
    {
      heading: t.product,
      links: [
        { label: t.links.features, href: `/${lang}#features` },
        { label: t.links.howItWorks, href: `/${lang}#how-it-works` },
        { label: t.links.pricing, href: `/${lang}#pricing` },
      ],
    },
    {
      heading: t.support,
      links: [
        { label: t.links.chat, href: WHATSAPP_URL },
        { label: t.links.aboutRsi, href: `/${lang}#faq` },
      ],
    },
    {
      heading: t.legal,
      links: [
        { label: t.links.privacy, href: `/${lang}/privacy` },
        { label: t.links.terms, href: `/${lang}/terms` },
        { label: t.links.dgi, href: dgiUrl },
      ],
    },
  ];

  return (
    <footer
      className="relative overflow-hidden"
      style={{ background: "linear-gradient(165deg, #052e16, #14532d)" }}
    >
      {/* Top wave */}
      <div className="absolute top-0 left-0 right-0 overflow-hidden leading-none rotate-180">
        <svg viewBox="0 0 1440 40" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-full block" preserveAspectRatio="none">
          <path d="M0 40V20C360 0 720 40 1080 20 1260 10 1380 30 1440 20V40H0Z" fill="#052e16" />
        </svg>
      </div>

      {/* Shimmer blob */}
      <div
        className="absolute top-0 right-0 opacity-10 pointer-events-none"
        style={{ width: 600, height: 600, background: "radial-gradient(circle at 80% 10%, #4ade80, transparent 60%)" }}
      />

      <div className="max-w-7xl 3xl:max-w-9xl 4xl:max-w-11xl mx-auto px-4 sm:px-6 xl:px-8 3xl:px-12 4xl:px-28 pt-20 xl:pt-28 3xl:pt-36 4xl:pt-48 pb-10 xl:pb-14 4xl:pb-20 relative">
        <div className="grid md:grid-cols-[2fr_1fr_1fr_1fr] xl:grid-cols-[3fr_1fr_1fr_1fr] gap-10 md:gap-12 xl:gap-16 mb-12 xl:mb-16">
          {/* Brand column */}
          <div>
            <div className="flex items-center gap-2.5 mb-4">
              <TassiLogo />
              <span className="font-bold text-white text-xl xl:text-2xl 3xl:text-3xl tracking-tight">Tassi</span>
            </div>
            <p className="text-green-300 text-sm xl:text-base 3xl:text-lg leading-relaxed max-w-xs xl:max-w-sm mb-6">
              {t.tagline}
            </p>
            <a
              href={WHATSAPP_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 bg-white/10 hover:bg-white/20 border border-white/20 text-white text-sm xl:text-base font-semibold px-5 py-2.5 3xl:px-6 3xl:py-3 rounded-xl transition-colors"
            >
              <svg viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4 flex-shrink-0">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z" />
              </svg>
              {t.links.openWa}
            </a>
          </div>

          {/* Link columns */}
          {footerCols.map((col) => (
            <div key={col.heading}>
              <p className="text-white font-bold text-sm xl:text-base uppercase tracking-wider mb-4 xl:mb-5">
                {col.heading}
              </p>
              <ul className="space-y-2.5 xl:space-y-3">
                {col.links.map((l) => (
                  <li key={l.label}>
                    <Link
                      href={l.href}
                      className="text-green-300 text-sm xl:text-base hover:text-white transition-colors"
                      target={l.href.startsWith("http") ? "_blank" : undefined}
                      rel={l.href.startsWith("http") ? "noopener noreferrer" : undefined}
                    >
                      {l.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Bottom bar */}
        <div className="border-t border-white/10 pt-8 xl:pt-10 flex flex-col sm:flex-row items-center justify-between gap-3">
          <p className="text-green-400 text-xs xl:text-sm 3xl:text-base">
            {t.copy}
          </p>
          <div className="flex items-center gap-1.5 text-xs xl:text-sm 3xl:text-base text-green-500">
            <span className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" />
            {t.ratesNote}
          </div>
        </div>
      </div>
    </footer>
  );
}

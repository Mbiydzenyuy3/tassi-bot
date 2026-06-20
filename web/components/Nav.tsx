"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import Image from "next/image";
import { usePathname } from "next/navigation";
import { WHATSAPP_URL } from "@/lib/constants";
import type { Copy, Lang } from "@/lib/i18n";


const WaIcon = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4 flex-shrink-0">
    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z" />
  </svg>
);

export default function Nav({ t, lang }: { t: Copy["nav"]; lang: Lang }) {
  const [open, setOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const pathname = usePathname();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const links = [
    { href: `/${lang}#features`, label: t.features },
    { href: `/${lang}#how-it-works`, label: t.howItWorks },
    { href: `/${lang}#pricing`, label: t.pricing },
  ];

  const otherLang: Lang = lang === "fr" ? "en" : "fr";
  const otherPath = pathname.replace(`/${lang}`, `/${otherLang}`);

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${scrolled
        ? "bg-white/95 backdrop-blur-md shadow-sm border-b border-gray-100"
        : "bg-transparent"
        }`}
    >
      <nav className="max-w-7xl 3xl:max-w-9xl 4xl:max-w-11xl mx-auto px-4 sm:px-6 xl:px-8 3xl:px-12 4xl:px-28 h-16 xl:h-20 3xl:h-24 4xl:h-32 flex items-center justify-between">
        {/* Logo */}
        <Link
          href={`/${lang}`}
          className="flex flex-col items-start flex-shrink-0"
          aria-label="Tassi"
        >
          <Image
            src="/image/logo/logo-cropped.png"
            alt="Tassi"
            width={752}
            height={449}
            className="h-10 xl:h-14 3xl:h-16 4xl:h-24 w-auto"
            priority
          />
          {/* <span className="hidden sm:block text-[8px] xl:text-[9px] 3xl:text-[11px] text-gray-400 -mt-1 font-medium tracking-wide pl-0.5">
            {t.tagline}
          </span> */}
        </Link>

        {/* Desktop nav */}
        <div className="hidden md:flex items-center gap-6 xl:gap-8 3xl:gap-10">
          {links.map((l) => (
            <Link
              key={l.href}
              href={l.href}
              className="text-sm xl:text-base 3xl:text-lg font-medium text-gray-500 hover:text-forest-700 transition-colors"
            >
              {l.label}
            </Link>
          ))}
        </div>

        {/* Right controls */}
        <div className="hidden md:flex items-center gap-3 3xl:gap-4">
          <a
            href={otherPath}
            translate="no"
            className="inline-flex items-center gap-1.5 text-xs xl:text-sm font-semibold uppercase px-3 py-1.5 3xl:px-4 3xl:py-2 rounded-lg border border-gray-200 text-gray-500 hover:border-forest-300 hover:text-forest-700 transition-colors tracking-wider"
          >
            <span className="text-base leading-none">{otherLang === "en" ? "🇬🇧" : "🇫🇷"}</span>
            <span>{otherLang.toUpperCase()}</span>
          </a>
          <a
            href={WHATSAPP_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 btn-shimmer text-white text-sm xl:text-base 3xl:text-lg 4xl:text-xl px-5 py-2.5 3xl:px-7 3xl:py-3.5 4xl:px-9 4xl:py-5 rounded-xl font-semibold shadow-lg shadow-forest-200"
          >
            <WaIcon />
            {t.cta}
          </a>
        </div>

        {/* Hamburger — shown on mobile only */}
        <button
          onClick={() => setOpen(!open)}
          className="md:hidden p-2 rounded-lg text-gray-600 hover:bg-gray-50"
          aria-label="Toggle menu"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            {open ? (
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            ) : (
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            )}
          </svg>
        </button>
      </nav>

      {/* Mobile drawer */}
      <div
        className={`md:hidden overflow-hidden transition-all duration-300 bg-white border-t border-gray-100 ${open ? "max-h-80 opacity-100" : "max-h-0 opacity-0"
          }`}
      >
        <div className="px-4 py-4 space-y-1">
          {links.map((l) => (
            <Link
              key={l.href}
              href={l.href}
              onClick={() => setOpen(false)}
              className="block px-4 py-2.5 text-gray-700 font-medium rounded-lg hover:bg-forest-50 hover:text-forest-700 transition-colors"
            >
              {l.label}
            </Link>
          ))}
          <div className="flex gap-2 pt-2">
            <a
              href={otherPath}
              translate="no"
              className="flex-1 text-center py-3 rounded-xl border border-gray-200 text-sm font-bold uppercase text-gray-500"
            >
              {otherLang === "en" ? "🇬🇧 EN" : "🇫🇷 FR"}
            </a>
            <a
              href={WHATSAPP_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-[3] flex items-center justify-center gap-2 btn-shimmer text-white px-4 py-3 rounded-xl font-semibold"
            >
              <WaIcon />
              {t.cta}
            </a>
          </div>
        </div>
      </div>
    </header>
  );
}

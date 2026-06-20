"use client";

import { useState } from "react";
import { WHATSAPP_URL } from "@/lib/constants";
import type { Copy } from "@/lib/i18n";

const WaIcon = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4 flex-shrink-0">
    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z" />
  </svg>
);

export default function Faq({ t }: { t: Copy["faq"] }) {
  const [open, setOpen] = useState<number | null>(0);

  return (
    <section id="faq" className="py-20 xl:py-28 3xl:py-36 4xl:py-48 bg-white relative overflow-hidden">
      <div
        className="absolute inset-0 pointer-events-none opacity-[0.03]"
        style={{
          backgroundImage:
            "linear-gradient(#16a34a 1px, transparent 1px), linear-gradient(90deg, #16a34a 1px, transparent 1px)",
          backgroundSize: "56px 56px",
        }}
      />

      <div className="max-w-4xl xl:max-w-5xl 3xl:max-w-6xl 4xl:max-w-8xl mx-auto px-4 sm:px-6 xl:px-8 3xl:px-12 4xl:px-28 relative">
        <div className="text-center mb-12 xl:mb-16">
          <p className="text-sm xl:text-base font-bold uppercase tracking-widest text-forest-600 mb-3">
            {t.sectionLabel}
          </p>
          <h2 className="text-3xl xl:text-4xl 3xl:text-5xl 4xl:text-6xl font-extrabold text-gray-900 leading-tight">
            {t.h2}
          </h2>
        </div>

        <div className="space-y-3 xl:space-y-4">
          {t.items.map((item, i) => (
            <div
              key={i}
              className={`rounded-2xl border overflow-hidden transition-all duration-200 ${
                open === i
                  ? "border-forest-200 shadow-md shadow-forest-100/60"
                  : "border-gray-100 shadow-sm bg-white"
              }`}
            >
              <button
                onClick={() => setOpen(open === i ? null : i)}
                className={`w-full flex items-center justify-between px-6 xl:px-8 py-5 xl:py-6 text-left gap-4 transition-colors duration-200 ${
                  open === i ? "bg-forest-50" : "bg-white hover:bg-gray-50"
                }`}
                aria-expanded={open === i}
              >
                <span
                  className={`font-semibold text-base xl:text-lg 3xl:text-xl leading-snug transition-colors duration-200 ${
                    open === i ? "text-forest-800" : "text-gray-900"
                  }`}
                >
                  {item.q}
                </span>
                <span
                  className={`flex-shrink-0 flex items-center justify-center w-8 h-8 xl:w-9 xl:h-9 rounded-full border-2 transition-all duration-200 ${
                    open === i
                      ? "rotate-45 border-forest-400 bg-forest-100 text-forest-700"
                      : "border-gray-200 text-gray-400 bg-white"
                  }`}
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M12 5v14M5 12h14" />
                  </svg>
                </span>
              </button>

              <div
                className={`overflow-hidden transition-all duration-300 ease-in-out ${
                  open === i ? "max-h-[500px]" : "max-h-0"
                }`}
              >
                <div className="px-6 xl:px-8 pb-6 xl:pb-7 pt-1 bg-forest-50 border-t border-forest-100">
                  <p className="text-gray-600 text-sm xl:text-base 3xl:text-lg leading-relaxed">
                    {item.a}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-10 xl:mt-12 flex flex-col items-center gap-3 text-center">
          <a
            href={WHATSAPP_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2.5 bg-forest-600 hover:bg-forest-700 text-white font-semibold text-sm xl:text-base px-6 xl:px-8 py-3 xl:py-3.5 rounded-xl transition-colors shadow-sm"
          >
            <WaIcon />
            {t.ctaLabel}
          </a>
          <p className="text-gray-400 text-xs xl:text-sm">{t.ctaSub}</p>
        </div>
      </div>
    </section>
  );
}

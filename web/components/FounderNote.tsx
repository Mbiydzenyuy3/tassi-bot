import type { Copy } from "@/lib/i18n";

export default function FounderNote({ t }: { t: Copy["founderNote"] }) {
  return (
    <section className="py-16 xl:py-20 3xl:py-28 4xl:py-40" style={{ background: "linear-gradient(180deg, #f0fdf4 0%, #f9fffe 100%)" }}>
      <div className="max-w-2xl xl:max-w-3xl 3xl:max-w-4xl 4xl:max-w-5xl mx-auto px-4 sm:px-6 xl:px-8 3xl:px-12 text-center">

        {/* Section label */}
        <p className="text-xs xl:text-sm 3xl:text-base font-semibold uppercase tracking-widest text-forest-600 mb-4 xl:mb-5">
          {t.sectionLabel}
        </p>

        {/* Heading */}
        <h2 className="text-2xl xl:text-3xl 3xl:text-4xl 4xl:text-5xl font-extrabold text-gray-900 mb-8 xl:mb-10">
          {t.h2}
        </h2>

        {/* Decorative open-quote */}
        <div aria-hidden className="text-forest-200 text-7xl xl:text-8xl font-serif leading-none mb-2 select-none">
          &ldquo;
        </div>

        {/* Quote */}
        <blockquote className="text-base xl:text-lg 3xl:text-xl 4xl:text-2xl text-gray-600 leading-relaxed mb-10 xl:mb-12 max-w-xl xl:max-w-2xl mx-auto">
          {t.quote}
        </blockquote>

        {/* Attribution */}
        <div className="flex flex-col items-center gap-3">
          <div
            className="w-12 h-12 xl:w-14 xl:h-14 3xl:w-16 3xl:h-16 rounded-full flex items-center justify-center text-white font-bold text-lg xl:text-xl flex-shrink-0"
            style={{ background: "linear-gradient(135deg, #15803d, #166534)" }}
            aria-label={t.name}
          >
            E
          </div>
          <div>
            <p className="font-bold text-gray-900 text-sm xl:text-base 3xl:text-lg">{t.name}</p>
            <p className="text-xs xl:text-sm 3xl:text-base text-gray-500 mt-0.5">{t.role}</p>
          </div>
        </div>

      </div>
    </section>
  );
}

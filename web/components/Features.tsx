import type { Copy } from "@/lib/i18n";

const freeIcons = [
  <svg key={0} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} className="w-6 h-6">
    <rect x="4" y="2" width="16" height="20" rx="2" strokeLinecap="round" />
    <path d="M8 6h8M8 10h8M8 14h5" strokeLinecap="round" />
    <circle cx="17" cy="17" r="4" fill="#dcfce7" stroke="#16a34a" strokeWidth={1.5} />
    <path d="M15.5 17h3M17 15.5v3" stroke="#16a34a" strokeWidth={1.5} strokeLinecap="round" />
  </svg>,
  <svg key={1} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} className="w-6 h-6">
    <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2" strokeLinecap="round" />
    <rect x="9" y="3" width="6" height="4" rx="1" />
    <path d="M9 12l2 2 4-4" strokeLinecap="round" strokeLinejoin="round" />
  </svg>,
  <svg key={2} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} className="w-6 h-6">
    <circle cx="12" cy="12" r="10" />
    <path d="M12 6v6l4 2" strokeLinecap="round" strokeLinejoin="round" />
  </svg>,
  <svg key={3} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} className="w-6 h-6">
    <path d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" strokeLinecap="round" strokeLinejoin="round" />
  </svg>,
];

const plusIcons = [
  <svg key={0} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} className="w-6 h-6">
    <path d="M3 3h18v4H3zM3 11h18v4H3zM3 19h18" strokeLinecap="round" strokeLinejoin="round" />
    <path d="M7 7h2M7 15h2" strokeLinecap="round" />
    <circle cx="19" cy="19" r="4" fill="#fef3c7" stroke="#d97706" strokeWidth={1.5} />
    <path d="M17.5 19h3M19 17.5v3" stroke="#d97706" strokeWidth={1.5} strokeLinecap="round" />
  </svg>,
  <svg key={1} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} className="w-6 h-6">
    <path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" strokeLinecap="round" strokeLinejoin="round" />
  </svg>,
  <svg key={2} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} className="w-6 h-6">
    <rect x="3" y="4" width="18" height="18" rx="2" strokeLinecap="round" />
    <path d="M16 2v4M8 2v4M3 10h18" strokeLinecap="round" />
    <path d="M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01" strokeLinecap="round" strokeLinejoin="round" />
  </svg>,
  <svg key={3} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} className="w-6 h-6">
    <path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9" strokeLinecap="round" strokeLinejoin="round" />
    <path d="M13.73 21a2 2 0 01-3.46 0" strokeLinecap="round" />
  </svg>,
];

export default function Features({ t }: { t: Copy["features"] }) {
  const freeItems = t.items.filter((f) => f.tag === "Gratuit" || f.tag === "Free");
  const plusItems = t.items.filter((f) => f.tag === "Plus");

  return (
    <section id="features" className="py-24 xl:py-32 3xl:py-40 4xl:py-56 bg-white">
      <div className="max-w-7xl 3xl:max-w-9xl 4xl:max-w-11xl mx-auto px-4 sm:px-6 xl:px-8 3xl:px-12 4xl:px-28">
        <div className="text-center mb-16 xl:mb-20">
          <p className="text-sm xl:text-base font-bold uppercase tracking-widest text-forest-600 mb-3">{t.sectionLabel}</p>
          <h2 className="text-4xl xl:text-5xl 3xl:text-6xl 4xl:text-7xl font-extrabold text-gray-900 leading-tight mb-4">
            {t.h2a} <span className="gradient-text">{t.h2b}</span>
          </h2>
          <p className="text-lg xl:text-xl 3xl:text-2xl text-gray-500 max-w-xl xl:max-w-2xl mx-auto">{t.sub}</p>
        </div>

        {/* Free tier group */}
        <div className="mb-10 xl:mb-12">
          <div className="flex items-center gap-3 mb-6">
            <span className="inline-flex items-center gap-1.5 text-xs xl:text-sm font-bold uppercase tracking-widest text-forest-700 bg-forest-50 border border-forest-200 px-3 py-1.5 rounded-full">
              <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
              {t.freeSectionLabel}
            </span>
            <div className="flex-1 h-px bg-forest-100" />
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 xl:gap-6 3xl:gap-8">
            {freeItems.map((f, i) => (
              <div
                key={f.title}
                className="card-lift relative rounded-2xl border border-forest-100 bg-gradient-to-br from-forest-50 to-green-50 p-6 xl:p-7 overflow-hidden"
              >
                <div className="inline-flex items-center justify-center w-11 h-11 xl:w-13 xl:h-13 rounded-xl bg-forest-100 text-forest-700 mb-4">
                  {freeIcons[i]}
                </div>
                <h3 className="font-bold text-gray-900 text-base xl:text-lg 3xl:text-xl mb-2">{f.title}</h3>
                <p className="text-gray-500 text-sm xl:text-base leading-relaxed">{f.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Plus tier group */}
        <div>
          <div className="flex items-center gap-3 mb-6">
            <span className="inline-flex items-center gap-1.5 text-xs xl:text-sm font-bold uppercase tracking-widest text-amber-700 bg-amber-50 border border-amber-200 px-3 py-1.5 rounded-full">
              <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
              {t.plusSectionLabel}
            </span>
            <div className="flex-1 h-px bg-amber-100" />
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 xl:gap-6 3xl:gap-8">
            {plusItems.map((f, i) => (
              <div
                key={f.title}
                className="card-lift relative rounded-2xl border border-amber-200 bg-gradient-to-br from-amber-50 to-yellow-50 p-6 xl:p-8 overflow-hidden"
              >
                <div className="absolute top-0 right-0 w-32 h-32 opacity-5">
                  <svg viewBox="0 0 128 128" fill="#d97706"><circle cx="64" cy="64" r="64" /></svg>
                </div>
                <div className="inline-flex items-center justify-center w-11 h-11 xl:w-13 xl:h-13 rounded-xl bg-amber-100 text-amber-700 mb-4">
                  {plusIcons[i]}
                </div>
                <h3 className="font-bold text-gray-900 text-base xl:text-lg 3xl:text-xl mb-2">{f.title}</h3>
                <p className="text-gray-500 text-sm xl:text-base leading-relaxed">{f.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

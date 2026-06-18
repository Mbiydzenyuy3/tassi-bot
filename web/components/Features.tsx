import type { Copy } from "@/lib/i18n";

const icons = [
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
    <path d="M3 3h18v4H3zM3 11h18v4H3zM3 19h18" strokeLinecap="round" strokeLinejoin="round" />
    <path d="M7 7h2M7 15h2" strokeLinecap="round" />
    <circle cx="19" cy="19" r="4" fill="#fef3c7" stroke="#d97706" strokeWidth={1.5} />
    <path d="M17.5 19h3M19 17.5v3" stroke="#d97706" strokeWidth={1.5} strokeLinecap="round" />
  </svg>,
  <svg key={3} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} className="w-6 h-6">
    <path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" strokeLinecap="round" strokeLinejoin="round" />
  </svg>,
  <svg key={4} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} className="w-6 h-6">
    <circle cx="12" cy="12" r="10" />
    <path d="M12 6v6l4 2" strokeLinecap="round" strokeLinejoin="round" />
  </svg>,
  <svg key={5} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} className="w-6 h-6">
    <path d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" strokeLinecap="round" strokeLinejoin="round" />
  </svg>,
];

const cardStyles = [
  { color: "from-forest-50 to-forest-100", iconBg: "bg-forest-100 text-forest-700", accent: "border-forest-200", tagColor: "bg-forest-100 text-forest-700" },
  { color: "from-blue-50 to-indigo-50",    iconBg: "bg-blue-100 text-blue-700",     accent: "border-blue-200",   tagColor: "bg-blue-100 text-blue-700" },
  { color: "from-gold-50 to-amber-50",     iconBg: "bg-gold-100 text-gold-700",     accent: "border-gold-200",   tagColor: "bg-gold-100 text-gold-700" },
  { color: "from-purple-50 to-pink-50",    iconBg: "bg-purple-100 text-purple-700", accent: "border-purple-200", tagColor: "bg-gold-100 text-gold-700" },
  { color: "from-teal-50 to-cyan-50",      iconBg: "bg-teal-100 text-teal-700",     accent: "border-teal-200",   tagColor: "bg-forest-100 text-forest-700" },
  { color: "from-orange-50 to-red-50",     iconBg: "bg-orange-100 text-orange-700", accent: "border-orange-200", tagColor: "bg-forest-100 text-forest-700" },
];

export default function Features({ t }: { t: Copy["features"] }) {
  return (
    <section id="features" className="py-24 xl:py-32 3xl:py-40 bg-white">
      <div className="max-w-7xl 3xl:max-w-9xl mx-auto px-4 sm:px-6 xl:px-8 3xl:px-12">
        <div className="text-center mb-16 xl:mb-20">
          <p className="text-sm xl:text-base font-bold uppercase tracking-widest text-forest-600 mb-3">{t.sectionLabel}</p>
          <h2 className="text-4xl xl:text-5xl 3xl:text-6xl font-extrabold text-gray-900 leading-tight mb-4">
            {t.h2a} <span className="gradient-text">{t.h2b}</span>
          </h2>
          <p className="text-lg xl:text-xl 3xl:text-2xl text-gray-500 max-w-xl xl:max-w-2xl mx-auto">{t.sub}</p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 xl:gap-8 3xl:gap-10">
          {t.items.map((f, i) => {
            const s = cardStyles[i];
            return (
              <div
                key={f.title}
                className={`card-lift relative rounded-2xl border ${s.accent} bg-gradient-to-br ${s.color} p-6 xl:p-8 overflow-hidden`}
              >
                <span className={`absolute top-4 right-4 text-[10px] xl:text-xs font-bold px-2 py-0.5 rounded-full ${s.tagColor}`}>
                  {f.tag}
                </span>
                <div className={`inline-flex items-center justify-center w-12 h-12 xl:w-14 xl:h-14 rounded-xl ${s.iconBg} mb-4`}>
                  {icons[i]}
                </div>
                <h3 className="font-bold text-gray-900 text-lg xl:text-xl 3xl:text-2xl mb-2">{f.title}</h3>
                <p className="text-gray-500 text-sm xl:text-base 3xl:text-lg leading-relaxed">{f.description}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}

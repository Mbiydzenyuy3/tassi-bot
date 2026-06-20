import { WHATSAPP_URL } from "@/lib/constants";
import type { Copy } from "@/lib/i18n";

const WaIcon = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z" />
  </svg>
);

export default function HowItWorks({ t }: { t: Copy["howItWorks"] }) {
  return (
    <section id="how-it-works" className="py-24 xl:py-32 3xl:py-40 4xl:py-52 bg-white relative overflow-hidden">
      <div
        className="absolute top-0 right-0 opacity-20 pointer-events-none"
        style={{ width: 600, height: 600, background: "radial-gradient(circle at 80% 20%, #dcfce7, transparent 70%)" }}
      />

      <div className="max-w-7xl 3xl:max-w-9xl 4xl:max-w-11xl mx-auto px-4 sm:px-6 xl:px-8 3xl:px-12 4xl:px-20 relative">
        <div className="text-center mb-16 xl:mb-20 3xl:mb-24">
          <p className="text-sm xl:text-base 3xl:text-lg font-bold uppercase tracking-widest text-forest-600 mb-3">{t.sectionLabel}</p>
          <h2 className="text-4xl xl:text-5xl 3xl:text-6xl 4xl:text-7xl font-extrabold text-gray-900 leading-tight mb-4">
            {t.h2a} <span className="gradient-text">{t.h2b}</span>
          </h2>
          <p className="text-lg xl:text-xl 3xl:text-2xl text-gray-500 max-w-xl xl:max-w-2xl mx-auto">{t.sub}</p>
        </div>

        <div className="grid md:grid-cols-2 xl:grid-cols-4 gap-6 xl:gap-8 3xl:gap-10 mb-14 xl:mb-16">
          {t.steps.map((step, i) => (
            <div key={step.num} className="relative flex flex-col">
              {/* Connector line between cards on xl+ */}
              {i < t.steps.length - 1 && (
                <div className="hidden xl:block absolute top-10 left-[calc(100%_-_16px)] w-[calc(100%_-_32px)] h-px z-10">
                  <div
                    className="w-full h-full"
                    style={{ background: "repeating-linear-gradient(90deg, #16a34a 0, #16a34a 6px, transparent 6px, transparent 14px)" }}
                  />
                </div>
              )}
              <div className="bg-white rounded-2xl p-6 xl:p-7 3xl:p-9 border border-gray-100 shadow-sm card-lift flex-1 flex flex-col">
                <div className="flex items-center gap-3 mb-4">
                  <div
                    className="w-10 h-10 xl:w-12 xl:h-12 rounded-xl flex items-center justify-center font-black text-sm xl:text-base text-white flex-shrink-0"
                    style={{ background: "linear-gradient(135deg, #166534, #16a34a)" }}
                  >
                    {step.num}
                  </div>
                  <span className="text-2xl xl:text-3xl">{step.emoji}</span>
                </div>
                <h3 className="font-bold text-gray-900 text-lg xl:text-xl 3xl:text-2xl mb-2">{step.title}</h3>
                <p className="text-gray-500 text-sm xl:text-base 3xl:text-lg leading-relaxed flex-1">{step.description}</p>
                <div className="mt-4 inline-flex items-center gap-1.5 bg-forest-50 text-forest-700 text-[11px] xl:text-xs font-medium px-2.5 py-1 rounded-full self-start">
                  <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                  {step.detail}
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="text-center">
          <a
            href={WHATSAPP_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2.5 btn-shimmer text-white font-bold text-base xl:text-lg 3xl:text-xl px-8 xl:px-10 3xl:px-12 py-4 xl:py-5 3xl:py-6 rounded-2xl shadow-lg shadow-forest-200 hover:shadow-forest-300 hover:scale-[1.02] active:scale-[0.98] transition-all duration-200"
          >
            <WaIcon />
            {t.ctaLabel}
          </a>
          <p className="text-gray-400 text-sm xl:text-base mt-3">{t.ctaSub}</p>
        </div>
      </div>
    </section>
  );
}

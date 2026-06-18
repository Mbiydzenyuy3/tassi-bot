import { WHATSAPP_URL } from "@/lib/constants";
import type { Copy } from "@/lib/i18n";

const CheckIcon = () => (
  <svg className="w-4 h-4 text-forest-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
  </svg>
);

const GoldCheckIcon = () => (
  <svg className="w-4 h-4 text-white flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
  </svg>
);

const XIcon = () => (
  <svg className="w-4 h-4 text-gray-300 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
    <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
  </svg>
);

const WaIcon = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4">
    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z" />
  </svg>
);

export default function Pricing({ t }: { t: Copy["pricing"] }) {
  return (
    <section id="pricing" className="py-24 xl:py-32 3xl:py-40 4xl:py-52 bg-gray-50 relative overflow-hidden">
      <div
        className="absolute bottom-0 left-1/2 -translate-x-1/2 opacity-10 pointer-events-none"
        style={{ width: 900, height: 500, background: "radial-gradient(ellipse, #16a34a, transparent 70%)" }}
      />

      <div className="max-w-5xl xl:max-w-6xl 3xl:max-w-8xl 4xl:max-w-10xl mx-auto px-4 sm:px-6 xl:px-8 3xl:px-12 4xl:px-20 relative">
        <div className="text-center mb-14 xl:mb-18">
          <p className="text-sm xl:text-base font-bold uppercase tracking-widest text-forest-600 mb-3">{t.sectionLabel}</p>
          <h2 className="text-4xl xl:text-5xl 3xl:text-6xl 4xl:text-7xl font-extrabold text-gray-900 leading-tight mb-4">
            {t.h2a} <span className="gradient-text">{t.h2b}</span>
          </h2>
          <p className="text-lg xl:text-xl 3xl:text-2xl text-gray-500 max-w-lg xl:max-w-xl mx-auto">{t.sub}</p>
        </div>

        <div className="grid md:grid-cols-2 gap-6 xl:gap-8 3xl:gap-10 items-start">
          {/* Free */}
          <div className="bg-white rounded-2xl border border-gray-200 p-8 xl:p-10 3xl:p-12 shadow-sm">
            <div className="mb-6">
              <p className="text-sm xl:text-base font-bold uppercase tracking-wider text-gray-400 mb-1">{t.freeName}</p>
              <div className="flex items-end gap-1">
                <span className="text-5xl xl:text-6xl font-black text-gray-900">{t.freePrice}</span>
                <span className="text-xl xl:text-2xl font-bold text-gray-400 mb-1">XAF</span>
              </div>
              <p className="text-gray-400 text-sm xl:text-base mt-1">{t.freeSub}</p>
            </div>
            <a
              href={WHATSAPP_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center justify-center gap-2 w-full py-3 xl:py-4 rounded-xl border-2 border-forest-600 text-forest-700 font-bold text-sm xl:text-base hover:bg-forest-50 transition-colors mb-6"
            >
              <WaIcon />
              {t.freeCta}
            </a>
            <ul className="space-y-3 xl:space-y-4">
              {t.freeTier.map((item) => (
                <li key={item.label} className="flex items-center gap-3">
                  {item.included ? <CheckIcon /> : <XIcon />}
                  <span className={`text-sm xl:text-base ${item.included ? "text-gray-700" : "text-gray-300"}`}>
                    {item.label}
                  </span>
                </li>
              ))}
            </ul>
          </div>

          {/* Plus */}
          <div
            className="rounded-2xl p-8 xl:p-10 3xl:p-12 shadow-2xl shadow-forest-300/30 relative overflow-hidden"
            style={{ background: "linear-gradient(145deg, #166534, #16a34a 60%, #15803d)" }}
          >
            <div className="absolute top-5 right-5 bg-gold-500 text-white text-[10px] xl:text-xs font-black uppercase tracking-wider px-2.5 py-1 rounded-full">
              {t.popularBadge}
            </div>
            <div
              className="absolute inset-0 opacity-10 pointer-events-none"
              style={{ backgroundImage: "radial-gradient(ellipse at 20% 30%, white, transparent 60%)" }}
            />
            <div className="mb-6 relative">
              <p className="text-sm xl:text-base font-bold uppercase tracking-wider text-green-200 mb-1">{t.plusName}</p>
              <div className="flex items-end gap-1">
                <span className="text-5xl xl:text-6xl font-black text-white">500</span>
                <span className="text-xl xl:text-2xl font-bold text-green-200 mb-1">XAF</span>
              </div>
              <p className="text-green-300 text-sm xl:text-base mt-1">{t.plusSub}</p>
            </div>
            <a
              href={WHATSAPP_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center justify-center gap-2 w-full py-3.5 xl:py-4 rounded-xl font-bold text-sm xl:text-base text-forest-800 mb-6 relative hover:opacity-95 transition-opacity"
              style={{ background: "linear-gradient(135deg, #fbbf24, #f59e0b)" }}
            >
              <WaIcon />
              {t.plusCta}
            </a>
            <ul className="space-y-3 xl:space-y-4 relative">
              {t.plusTier.map((label) => (
                <li key={label} className="flex items-center gap-3">
                  <GoldCheckIcon />
                  <span className="text-sm xl:text-base text-green-100">{label}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <p className="text-center text-gray-400 text-sm xl:text-base mt-8">
          {t.finePrint}{" "}
          <span className="font-mono bg-gray-100 px-1.5 py-0.5 rounded text-gray-600">CANCEL</span>{" "}
          {t.finePrint2}
        </p>
      </div>
    </section>
  );
}

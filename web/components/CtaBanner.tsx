import { WHATSAPP_URL } from "@/lib/constants";
import type { Copy } from "@/lib/i18n";

const WaIcon = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" className="w-6 h-6 flex-shrink-0">
    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z" />
  </svg>
);

const CheckChip = ({ label }: { label: string }) => (
  <span className="inline-flex items-center gap-1.5 text-xs xl:text-sm text-forest-700 bg-forest-50 border border-forest-100 px-3 py-1.5 rounded-full font-medium">
    <svg className="w-3 h-3 flex-shrink-0 text-forest-500" fill="currentColor" viewBox="0 0 20 20">
      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
    </svg>
    {label}
  </span>
);

export default function CtaBanner({ t }: { t: Copy["ctaBanner"] }) {
  const isFr = t.deadline.startsWith("Les");

  const chips = isFr
    ? ["Résultat en < 3 secondes", "Barème DGI officiel 2024", "Sans inscription ni téléchargement"]
    : ["Result in < 3 seconds", "Official DGI 2024 rates", "No sign-up or download"];

  return (
    <section
      className="py-20 xl:py-28 3xl:py-36 4xl:py-48 relative overflow-hidden"
      style={{
        background: "linear-gradient(160deg, #f0fdf4 0%, #ffffff 45%, #fffbeb 100%)",
      }}
    >
      {/* Decorative radial glow — different from hero (centred, not top-right) */}
      <div
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 pointer-events-none opacity-[0.12]"
        style={{
          width: 900,
          height: 600,
          background: "radial-gradient(ellipse at center, #16a34a, transparent 65%)",
        }}
      />
      {/* Corner accent — top-right gold */}
      <div
        className="absolute top-0 right-0 pointer-events-none opacity-20"
        style={{
          width: 400,
          height: 400,
          background: "radial-gradient(circle at 80% 10%, #f59e0b, transparent 60%)",
        }}
      />

      <div className="max-w-3xl xl:max-w-4xl 3xl:max-w-5xl 4xl:max-w-8xl mx-auto px-4 sm:px-6 xl:px-8 4xl:px-20 text-center relative">

        {/* Deadline chip */}
        <div className="inline-flex items-center gap-2 bg-red-50 border border-red-100 text-red-600 px-4 py-2 rounded-full text-sm xl:text-base font-semibold mb-8 xl:mb-10">
          <svg className="w-4 h-4 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
          </svg>
          {t.deadline}
        </div>

        {/* Headline */}
        <h2 className="text-4xl xl:text-5xl 3xl:text-6xl 4xl:text-7xl font-extrabold text-gray-900 leading-tight mb-5 xl:mb-6">
          {t.h2a} <span className="gradient-text">{t.h2b}</span>
        </h2>

        <p className="text-lg xl:text-xl 3xl:text-2xl text-gray-500 mb-10 xl:mb-12 leading-relaxed max-w-xl xl:max-w-2xl mx-auto">
          {t.sub}
        </p>

        {/* CTA */}
        <a
          href={WHATSAPP_URL}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-3 btn-shimmer text-white font-bold text-lg xl:text-xl 3xl:text-2xl px-10 xl:px-14 py-5 xl:py-6 rounded-2xl shadow-2xl shadow-forest-200/50 hover:shadow-forest-300/60 hover:scale-[1.02] active:scale-[0.98] transition-all duration-200"
        >
          <WaIcon />
          {t.cta}
        </a>

        {/* Trust chips — new format, never shown anywhere else on page */}
        <div className="flex flex-wrap items-center justify-center gap-2 xl:gap-3 mt-8 xl:mt-10">
          {chips.map((label) => (
            <CheckChip key={label} label={label} />
          ))}
        </div>

        {/* Social proof line — number only, no recycled avatars */}
        <p className="text-gray-400 text-sm xl:text-base mt-5">
          <span className="font-semibold text-gray-600">473</span>{" "}
          {t.social}
        </p>
      </div>
    </section>
  );
}

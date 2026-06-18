import { WHATSAPP_URL } from "@/lib/constants";
import type { Copy } from "@/lib/i18n";

const WaIcon = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5 flex-shrink-0">
    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z" />
  </svg>
);

const CheckIcon = () => (
  <svg className="w-4 h-4 text-forest-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
  </svg>
);

function PhoneMockup() {
  return (
    <div className="relative mx-auto mt-16" style={{ width: 260 }}>
      <div
        className="absolute inset-0 rounded-full opacity-30 blur-3xl"
        style={{ background: "radial-gradient(circle, #4ade80, #16a34a)", transform: "scale(1.4) translateY(10%)" }}
      />
      <div
        className="relative mx-auto overflow-hidden shadow-2xl"
        style={{ width: 248, height: 500, borderRadius: 44, background: "#1a1a2e", border: "6px solid #111" }}
      >
        <div
          className="absolute left-1/2 -translate-x-1/2 bg-black z-10 flex items-center justify-center gap-1"
          style={{ top: 10, width: 88, height: 22, borderRadius: 11 }}
        >
          <div className="w-2 h-2 rounded-full bg-gray-700" />
          <div className="w-3 h-3 rounded-full bg-gray-600" />
        </div>
        <div className="absolute inset-0 flex flex-col">
          <div className="flex-shrink-0 pt-10">
            <div className="flex items-center gap-2.5 px-4 py-2.5" style={{ background: "#075e54" }}>
              <svg className="w-4 h-4 text-white opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M15 19l-7-7 7-7" />
              </svg>
              <div
                className="flex-shrink-0 flex items-center justify-center rounded-full font-bold text-xs text-white"
                style={{ width: 32, height: 32, background: "linear-gradient(135deg,#166534,#22c55e)" }}
              >
                T
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-white text-xs font-semibold leading-none">Tassi</p>
                <p className="text-green-300 text-[9px] mt-0.5">en ligne</p>
              </div>
            </div>
            <div className="flex items-center justify-center py-2" style={{ background: "#e5ddd5" }}>
              <span className="text-[8px] text-gray-500 px-2 py-0.5 rounded-full" style={{ background: "rgba(0,0,0,0.07)" }}>
                AUJOURD&apos;HUI
              </span>
            </div>
          </div>
          <div className="flex-1 px-2.5 py-2 space-y-2 overflow-hidden" style={{ background: "#e5ddd5" }}>
            <div className="flex chat-msg">
              <div className="max-w-[88%] px-2.5 py-2 shadow-sm" style={{ background: "white", borderRadius: "0 10px 10px 10px" }}>
                <p className="text-gray-800 leading-relaxed" style={{ fontSize: 8 }}>
                  Bonjour ! Je suis <strong>Tassi</strong>. Choisissez votre langue :
                </p>
                <p className="text-gray-700 mt-1" style={{ fontSize: 8 }}>1️⃣ Français &nbsp; 2️⃣ English &nbsp; 3️⃣ Pidgin</p>
                <p className="text-gray-400 text-right mt-0.5" style={{ fontSize: 7 }}>09:03</p>
              </div>
            </div>
            <div className="flex justify-end chat-msg">
              <div className="px-2.5 py-1.5 shadow-sm" style={{ background: "#dcf8c6", borderRadius: "10px 10px 0 10px" }}>
                <p className="text-gray-800" style={{ fontSize: 8 }}>1</p>
                <p className="text-gray-400 text-right" style={{ fontSize: 7 }}>09:03 ✓✓</p>
              </div>
            </div>
            <div className="flex chat-msg">
              <div className="max-w-[80%] px-2.5 py-2 shadow-sm" style={{ background: "white", borderRadius: "0 10px 10px 10px" }}>
                <p className="text-gray-800" style={{ fontSize: 8 }}>Quel est votre chiffre d&apos;affaires ce mois-ci ?</p>
                <p className="text-gray-400 text-right mt-0.5" style={{ fontSize: 7 }}>09:04</p>
              </div>
            </div>
            <div className="flex justify-end chat-msg">
              <div className="px-2.5 py-1.5 shadow-sm" style={{ background: "#dcf8c6", borderRadius: "10px 10px 0 10px" }}>
                <p className="text-gray-800" style={{ fontSize: 8 }}>2 350 000 frs</p>
                <p className="text-gray-400 text-right" style={{ fontSize: 7 }}>09:04 ✓✓</p>
              </div>
            </div>
            <div className="flex chat-msg">
              <div className="max-w-[92%] shadow-sm" style={{ background: "white", borderRadius: "0 10px 10px 10px", overflow: "hidden" }}>
                <div className="px-2.5 py-1.5" style={{ background: "#f0fdf4", borderBottom: "1px solid #dcfce7" }}>
                  <p className="font-bold text-forest-800" style={{ fontSize: 8 }}>Calcul RSI</p>
                </div>
                <div className="px-2.5 py-1.5 space-y-0.5">
                  <div className="flex justify-between">
                    <p className="text-gray-500" style={{ fontSize: 7 }}>CA :</p>
                    <p className="text-gray-700 font-medium" style={{ fontSize: 7 }}>2 350 000 XAF</p>
                  </div>
                  <div className="flex justify-between">
                    <p className="text-gray-500" style={{ fontSize: 7 }}>Acompte RSI (5,5 %) :</p>
                    <p className="text-gray-700 font-medium" style={{ fontSize: 7 }}>129 250 XAF</p>
                  </div>
                  <div className="flex justify-between pt-1 mt-1" style={{ borderTop: "1px solid #f0fdf4" }}>
                    <p className="text-forest-700 font-bold" style={{ fontSize: 8 }}>Total :</p>
                    <p className="text-forest-700 font-bold" style={{ fontSize: 8 }}>129 250 XAF</p>
                  </div>
                </div>
                <p className="text-gray-400 text-right px-2.5 pb-1.5" style={{ fontSize: 7 }}>09:04</p>
              </div>
            </div>
          </div>
          <div className="flex-shrink-0 flex items-center gap-2 px-2.5 py-2" style={{ background: "#f0f0f0" }}>
            <div className="flex-1 flex items-center bg-white rounded-full px-3 py-1.5">
              <p className="text-gray-400" style={{ fontSize: 8 }}>Message</p>
            </div>
            <div className="flex-shrink-0 flex items-center justify-center rounded-full" style={{ width: 28, height: 28, background: "#075e54" }}>
              <svg viewBox="0 0 24 24" fill="white" style={{ width: 13, height: 13 }}>
                <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
              </svg>
            </div>
          </div>
        </div>
      </div>
      <div className="absolute glass rounded-2xl px-3 py-2 shadow-xl animate-float" style={{ top: 80, right: -32, animationDelay: "0s" }}>
        <p className="text-[10px] font-bold text-gray-700">⚡ &lt; 3 sec</p>
        <p className="text-[8px] text-gray-400">résultat immédiat</p>
      </div>
      <div className="absolute glass rounded-2xl px-3 py-2 shadow-xl animate-float" style={{ bottom: 110, left: -32, animationDelay: "1.8s" }}>
        <p className="text-[10px] font-bold text-gray-700">Gratuit</p>
        <p className="text-[8px] text-gray-400">sans inscription</p>
      </div>
      <div className="absolute glass rounded-2xl px-3 py-2 shadow-xl animate-float" style={{ bottom: 200, right: -28, animationDelay: "0.9s" }}>
        <p className="text-[10px] font-bold text-forest-700">RSI 2024</p>
        <p className="text-[8px] text-gray-400">barème DGI</p>
      </div>
    </div>
  );
}

export default function Hero({ t }: { t: Copy["hero"] }) {
  return (
    <section className="relative min-h-screen flex items-center pt-16 xl:pt-20 3xl:pt-24 pb-16 overflow-hidden">
      <div className="absolute inset-0 bg-hero-gradient" />
      <div
        className="absolute top-0 right-0 opacity-40"
        style={{ width: 700, height: 700, background: "radial-gradient(circle at 70% 20%, #dcfce7 0%, transparent 70%)" }}
      />
      <div
        className="absolute bottom-0 left-0 opacity-30"
        style={{ width: 500, height: 500, background: "radial-gradient(circle at 30% 80%, #fef3c7 0%, transparent 70%)" }}
      />
      <div
        className="absolute inset-0 opacity-[0.025]"
        style={{
          backgroundImage: "linear-gradient(#16a34a 1px, transparent 1px), linear-gradient(90deg, #16a34a 1px, transparent 1px)",
          backgroundSize: "48px 48px",
        }}
      />

      <div className="relative w-full max-w-7xl 3xl:max-w-9xl mx-auto px-4 sm:px-6 xl:px-8 3xl:px-12">
        <div className="grid lg:grid-cols-[1fr_auto] gap-10 lg:gap-16 xl:gap-20 3xl:gap-28 items-center">
          <div className="animate-slide-up text-center lg:text-left max-w-2xl xl:max-w-3xl 3xl:max-w-4xl mx-auto lg:mx-0">
            <div className="inline-flex items-center gap-2 mb-6 rounded-full border border-forest-200 bg-forest-50 px-4 py-1.5 text-sm xl:text-base 3xl:text-lg font-medium text-forest-700">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-forest-400 opacity-75" />
                <span className="relative inline-flex rounded-full h-2 w-2 bg-forest-500" />
              </span>
              {t.badge}
            </div>

            <h1 className="text-[46px] sm:text-6xl xl:text-7xl 3xl:text-8xl font-extrabold leading-[1.05] tracking-tight mb-5 xl:mb-7">
              <span className="text-gray-900">{t.h1a}</span>
              <br />
              <span className="gradient-text">{t.h1b}</span>
            </h1>

            <p className="text-lg xl:text-xl 3xl:text-2xl text-gray-500 leading-relaxed mb-8 xl:mb-10 text-balance">
              {t.sub}
            </p>

            <div className="flex flex-col sm:flex-row items-center gap-3 xl:gap-4 justify-center lg:justify-start mb-8">
              <a
                href={WHATSAPP_URL}
                target="_blank"
                rel="noopener noreferrer"
                className="group inline-flex items-center justify-center gap-2.5 btn-shimmer text-white font-bold text-base xl:text-lg 3xl:text-xl px-8 xl:px-10 py-4 xl:py-5 rounded-2xl shadow-xl shadow-forest-200/60 hover:shadow-forest-300/70 hover:scale-[1.02] active:scale-[0.98] transition-all duration-200 w-full sm:w-auto"
              >
                <WaIcon />
                {t.primaryCta}
                <svg className="w-4 h-4 ml-0.5 group-hover:translate-x-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </a>
              <a
                href="#how-it-works"
                className="inline-flex items-center gap-2 text-gray-600 font-semibold text-base xl:text-lg px-6 xl:px-8 py-4 xl:py-5 rounded-2xl border border-gray-200 hover:border-gray-300 hover:bg-gray-50 transition-all duration-200 w-full sm:w-auto justify-center"
              >
                {t.secondaryCta}
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </a>
            </div>

            <div className="flex flex-wrap items-center gap-x-5 gap-y-2 justify-center lg:justify-start text-sm xl:text-base text-gray-400">
              {t.trust.map((item) => (
                <span key={item} className="flex items-center gap-1.5">
                  <CheckIcon />
                  {item}
                </span>
              ))}
            </div>
          </div>

          <div className="flex justify-center lg:justify-end animate-fade-in">
            <div className="scale-100 xl:scale-110 3xl:scale-[1.3] origin-center">
              <PhoneMockup />
            </div>
          </div>
        </div>
      </div>

      <div className="absolute bottom-0 left-0 right-0 overflow-hidden leading-none">
        <svg viewBox="0 0 1440 60" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-full block" preserveAspectRatio="none">
          <path d="M0 60V30C360 0 720 60 1080 30 1260 15 1380 45 1440 30V60H0Z" fill="white" />
        </svg>
      </div>
    </section>
  );
}

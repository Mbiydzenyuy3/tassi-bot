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

function PhoneMockup({ isEn }: { isEn: boolean }) {
  const lang = isEn ? "en" : "fr";
  const content = {
    fr: {
      today: "AUJOURD'HUI",
      greeting: "Bonjour ! Je suis Tassi 👋",
      langChoice: "Choisissez votre langue :\n1️⃣ Français   2️⃣ English   3️⃣ Pidgin",
      reply1: "1",
      questionMonth: "Parfait 🇫🇷 Pour quel mois calculez-vous votre RSI ?",
      replyMonth: "Décembre",
      questionCA: "Quel est votre chiffre d'affaires de Décembre ?",
      replyCA: "2 350 000 frs",
      resultTitle: "📊 Calcul RSI — Décembre 2024",
      ca: "CA déclaré :",
      caVal: "2 350 000 XAF",
      rsi: "Acompte RSI (5,5 %) :",
      rsiVal: "129 250 XAF",
      cac: "Part CAC (10 %) :",
      cacVal: "12 925 XAF",
      total: "Total à payer :",
      totalVal: "142 175 XAF",
      reminder: "✅ Déclarez avant le 15 janvier. Tapez AIDE pour toute question.",
      online: "en ligne",
      badge1: { top: "⚡ < 3 sec", sub: "résultat immédiat" },
      badge2: { top: "Gratuit", sub: "sans inscription" },
      badge3: { top: "RSI 2024", sub: "barème DGI" },
    },
    en: {
      today: "TODAY",
      greeting: "Hello! I'm Tassi 👋",
      langChoice: "Choose your language:\n1️⃣ Français   2️⃣ English   3️⃣ Pidgin",
      reply1: "2",
      questionMonth: "Great 🇬🇧 Which month are you filing RSI for?",
      replyMonth: "December",
      questionCA: "What is your revenue for December?",
      replyCA: "2,350,000 frs",
      resultTitle: "📊 RSI Calculation — Dec 2024",
      ca: "Revenue declared:",
      caVal: "2,350,000 XAF",
      rsi: "RSI acompte (5.5%):",
      rsiVal: "129,250 XAF",
      cac: "CAC portion (10%):",
      cacVal: "12,925 XAF",
      total: "Total due:",
      totalVal: "142,175 XAF",
      reminder: "✅ File before January 15. Type HELP for questions.",
      online: "online",
      badge1: { top: "⚡ < 3 sec", sub: "instant result" },
      badge2: { top: "Free", sub: "no sign-up" },
      badge3: { top: "RSI 2024", sub: "DGI rates" },
    },
  }[lang];

  return (
    <div
      className="relative mx-auto w-[260px] xl:w-[300px] 3xl:w-[340px] 4xl:w-[440px]"
      role="img"
      aria-label={isEn ? "Tassi on WhatsApp — RSI calculation conversation" : "Aperçu de Tassi sur WhatsApp — conversation de calcul RSI"}
    >
      <div
        className="absolute inset-0 rounded-full opacity-30 blur-3xl"
        style={{ background: "radial-gradient(circle, #4ade80, #16a34a)", transform: "scale(1.4) translateY(10%)" }}
      />
      <div
        className="relative mx-auto overflow-hidden shadow-2xl"
        style={{ width: "100%", aspectRatio: "248/500", borderRadius: 44, background: "#1a1a2e", border: "6px solid #111" }}
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
            <div className="flex items-center gap-2.5 px-4 py-2" style={{ background: "#075e54" }}>
              <svg className="w-4 h-4 text-white opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M15 19l-7-7 7-7" />
              </svg>
              <div
                className="flex-shrink-0 flex items-center justify-center rounded-full font-bold text-xs text-white"
                style={{ width: 28, height: 28, background: "linear-gradient(135deg,#166534,#22c55e)" }}
              >
                T
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-white text-xs font-semibold leading-none">Tassi</p>
                <p className="text-green-300 text-[9px] mt-0.5">{content.online}</p>
              </div>
            </div>
            <div className="flex items-center justify-center py-1.5" style={{ background: "#e5ddd5" }}>
              <span className="text-[8px] text-gray-500 px-2 py-0.5 rounded-full" style={{ background: "rgba(0,0,0,0.07)" }}>
                {content.today}
              </span>
            </div>
          </div>

          {/* Chat track — 8 messages, overflow-y-auto with scrollbar hidden */}
          <div
            className="flex-1 px-2 py-1.5 space-y-1.5 overflow-y-auto scrollbar-hide"
            style={{ background: "#e5ddd5" }}
          >
            {/* 1 — Tassi greeting */}
            <div className="flex chat-msg">
              <div className="max-w-[88%] px-2 py-1.5 shadow-sm" style={{ background: "white", borderRadius: "0 8px 8px 8px" }}>
                <p className="text-gray-800 font-medium" style={{ fontSize: 8 }}>{content.greeting}</p>
                <p className="text-gray-600 mt-0.5 whitespace-pre-line leading-relaxed" style={{ fontSize: 7.5 }}>{content.langChoice}</p>
                <p className="text-gray-400 text-right mt-0.5" style={{ fontSize: 6.5 }}>09:02</p>
              </div>
            </div>

            {/* 2 — User picks language */}
            <div className="flex justify-end chat-msg">
              <div className="px-2 py-1 shadow-sm" style={{ background: "#dcf8c6", borderRadius: "8px 8px 0 8px" }}>
                <p className="text-gray-800" style={{ fontSize: 8 }}>{content.reply1}</p>
                <p className="text-gray-400 text-right" style={{ fontSize: 6.5 }}>09:02 ✓✓</p>
              </div>
            </div>

            {/* 3 — Tassi asks month */}
            <div className="flex chat-msg">
              <div className="max-w-[88%] px-2 py-1.5 shadow-sm" style={{ background: "white", borderRadius: "0 8px 8px 8px" }}>
                <p className="text-gray-800 leading-relaxed" style={{ fontSize: 7.5 }}>{content.questionMonth}</p>
                <p className="text-gray-400 text-right mt-0.5" style={{ fontSize: 6.5 }}>09:02</p>
              </div>
            </div>

            {/* 4 — User answers month */}
            <div className="flex justify-end chat-msg">
              <div className="px-2 py-1 shadow-sm" style={{ background: "#dcf8c6", borderRadius: "8px 8px 0 8px" }}>
                <p className="text-gray-800" style={{ fontSize: 8 }}>{content.replyMonth}</p>
                <p className="text-gray-400 text-right" style={{ fontSize: 6.5 }}>09:03 ✓✓</p>
              </div>
            </div>

            {/* 5 — Tassi asks CA */}
            <div className="flex chat-msg">
              <div className="max-w-[85%] px-2 py-1.5 shadow-sm" style={{ background: "white", borderRadius: "0 8px 8px 8px" }}>
                <p className="text-gray-800" style={{ fontSize: 7.5 }}>{content.questionCA}</p>
                <p className="text-gray-400 text-right mt-0.5" style={{ fontSize: 6.5 }}>09:03</p>
              </div>
            </div>

            {/* 6 — User gives revenue */}
            <div className="flex justify-end chat-msg">
              <div className="px-2 py-1 shadow-sm" style={{ background: "#dcf8c6", borderRadius: "8px 8px 0 8px" }}>
                <p className="text-gray-800" style={{ fontSize: 8 }}>{content.replyCA}</p>
                <p className="text-gray-400 text-right" style={{ fontSize: 6.5 }}>09:03 ✓✓</p>
              </div>
            </div>

            {/* 7 — Tassi result card */}
            <div className="flex chat-msg">
              <div className="max-w-[95%] shadow-sm" style={{ background: "white", borderRadius: "0 8px 8px 8px", overflow: "hidden" }}>
                <div className="px-2 py-1" style={{ background: "#f0fdf4", borderBottom: "1px solid #dcfce7" }}>
                  <p className="font-bold text-forest-800" style={{ fontSize: 7 }}>{content.resultTitle}</p>
                </div>
                <div className="px-2 py-1 space-y-0.5">
                  <div className="flex justify-between gap-2">
                    <p className="text-gray-500" style={{ fontSize: 6.5 }}>{content.ca}</p>
                    <p className="text-gray-700 font-medium" style={{ fontSize: 6.5 }}>{content.caVal}</p>
                  </div>
                  <div className="flex justify-between gap-2">
                    <p className="text-gray-500" style={{ fontSize: 6.5 }}>{content.rsi}</p>
                    <p className="text-gray-700 font-medium" style={{ fontSize: 6.5 }}>{content.rsiVal}</p>
                  </div>
                  <div className="flex justify-between gap-2">
                    <p className="text-gray-500" style={{ fontSize: 6.5 }}>{content.cac}</p>
                    <p className="text-gray-700 font-medium" style={{ fontSize: 6.5 }}>{content.cacVal}</p>
                  </div>
                  <div className="flex justify-between gap-2 pt-1 mt-0.5" style={{ borderTop: "1px solid #dcfce7" }}>
                    <p className="text-forest-700 font-bold" style={{ fontSize: 7.5 }}>{content.total}</p>
                    <p className="text-forest-700 font-bold" style={{ fontSize: 7.5 }}>{content.totalVal}</p>
                  </div>
                </div>
                <p className="text-gray-400 text-right px-2 pb-1" style={{ fontSize: 6.5 }}>09:04</p>
              </div>
            </div>

            {/* 8 — Tassi deadline reminder */}
            <div className="flex chat-msg">
              <div className="max-w-[88%] px-2 py-1.5 shadow-sm" style={{ background: "white", borderRadius: "0 8px 8px 8px" }}>
                <p className="text-gray-800 leading-relaxed" style={{ fontSize: 7.5 }}>{content.reminder}</p>
                <p className="text-gray-400 text-right mt-0.5" style={{ fontSize: 6.5 }}>09:04</p>
              </div>
            </div>
          </div>

          <div className="flex-shrink-0 flex items-center gap-2 px-2 py-1.5" style={{ background: "#f0f0f0" }}>
            <div className="flex-1 flex items-center bg-white rounded-full px-2.5 py-1">
              <p className="text-gray-400" style={{ fontSize: 7.5 }}>Message</p>
            </div>
            <div className="flex-shrink-0 flex items-center justify-center rounded-full" style={{ width: 26, height: 26, background: "#075e54" }}>
              <svg viewBox="0 0 24 24" fill="white" style={{ width: 12, height: 12 }}>
                <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
              </svg>
            </div>
          </div>
        </div>
      </div>
      <div className="hidden sm:block absolute glass rounded-2xl px-3 py-2 shadow-xl animate-float" style={{ top: 80, right: -36, animationDelay: "0s" }}>
        <p className="text-[10px] font-bold text-gray-700">{content.badge1.top}</p>
        <p className="text-[8px] text-gray-400">{content.badge1.sub}</p>
      </div>
      <div className="hidden sm:block absolute glass rounded-2xl px-3 py-2 shadow-xl animate-float" style={{ bottom: 110, left: -36, animationDelay: "1.8s" }}>
        <p className="text-[10px] font-bold text-gray-700">{content.badge2.top}</p>
        <p className="text-[8px] text-gray-400">{content.badge2.sub}</p>
      </div>
      <div className="hidden sm:block absolute glass rounded-2xl px-3 py-2 shadow-xl animate-float" style={{ bottom: 200, right: -32, animationDelay: "0.9s" }}>
        <p className="text-[10px] font-bold text-forest-700">{content.badge3.top}</p>
        <p className="text-[8px] text-gray-400">{content.badge3.sub}</p>
      </div>
    </div>
  );
}

export default function Hero({ t, isEn }: { t: Copy["hero"]; isEn: boolean }) {
  return (
    <section className="relative min-h-screen flex items-center pt-24 xl:pt-28 3xl:pt-32 4xl:pt-48 pb-16 4xl:pb-28">
      {/* Richer background with diagonal sweep */}
      <div className="absolute inset-0" style={{ background: "linear-gradient(160deg, #f0fdf4 0%, #ffffff 40%, #fffbeb 100%)" }} />
      <div
        className="absolute top-0 right-0 opacity-50"
        style={{ width: 900, height: 900, background: "radial-gradient(circle at 70% 10%, #bbf7d0 0%, transparent 60%)" }}
      />
      <div
        className="absolute bottom-0 left-0 opacity-25"
        style={{ width: 600, height: 600, background: "radial-gradient(circle at 20% 90%, #fef3c7 0%, transparent 65%)" }}
      />
      <div
        className="absolute inset-0 opacity-[0.03]"
        style={{
          backgroundImage: "linear-gradient(#16a34a 1px, transparent 1px), linear-gradient(90deg, #16a34a 1px, transparent 1px)",
          backgroundSize: "48px 48px",
        }}
      />

      <div className="relative w-full max-w-7xl 3xl:max-w-9xl 4xl:max-w-11xl mx-auto px-4 sm:px-6 xl:px-8 3xl:px-12 4xl:px-28">
        <div className="grid lg:grid-cols-[1fr_360px] xl:grid-cols-[1fr_420px] 3xl:grid-cols-[1fr_500px] 4xl:grid-cols-[1fr_660px] gap-10 lg:gap-16 xl:gap-20 3xl:gap-28 4xl:gap-48 items-center">
          <div className="animate-slide-up text-center lg:text-left max-w-2xl xl:max-w-3xl 3xl:max-w-4xl mx-auto lg:mx-0">
            <div className="inline-flex items-center gap-2 mb-6 rounded-full border border-forest-200 bg-forest-50 px-4 py-1.5 text-sm xl:text-base 3xl:text-lg font-medium text-forest-700">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-forest-400 opacity-75" />
                <span className="relative inline-flex rounded-full h-2 w-2 bg-forest-500" />
              </span>
              {t.badge}
            </div>

            <h1 className="text-[40px] sm:text-5xl xl:text-6xl 3xl:text-7xl 3xl:text-[130px] font-extrabold leading-[1.05] tracking-tight mb-5 xl:mb-7 4xl:mb-10">
              <span className="text-gray-900">{t.h1a}</span>
              <br />
              <span className="gradient-text">{t.h1b}</span>
            </h1>

            <p className="text-lg xl:text-xl 3xl:text-2xl 4xl:text-3xl text-gray-500 leading-relaxed mb-8 xl:mb-10 4xl:mb-14 text-balance">
              {t.sub}
            </p>

            {/* Above-fold social proof */}
            <div className="flex items-center gap-2 mb-6 xl:mb-8 justify-center lg:justify-start">
              <div className="flex -space-x-1.5">
                {["A", "E", "C", "F", "M"].map((l, i) => (
                  <div
                    key={i}
                    className={`w-7 h-7 xl:w-8 xl:h-8 rounded-full border-2 border-white flex items-center justify-center text-white font-bold text-[10px] xl:text-xs flex-shrink-0 ${["bg-forest-700", "bg-gold-600", "bg-blue-600", "bg-teal-600", "bg-purple-600"][i]}`}
                  >
                    {l}
                  </div>
                ))}
              </div>
              <p className="text-sm xl:text-base text-gray-500">
                <span className="font-semibold text-gray-700">⭐ 4.9</span>{" "}
                <span className="text-gray-400">·</span>{" "}
                {t.socialProof}
              </p>
            </div>

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
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
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
            <PhoneMockup isEn={isEn} />
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

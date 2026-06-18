import type { Copy } from "@/lib/i18n";

export default function Testimonial({ t }: { t: Copy["testimonials"] }) {
  return (
    <section className="py-24 xl:py-32 3xl:py-40 4xl:py-52 bg-white">
      <div className="max-w-7xl 3xl:max-w-9xl 4xl:max-w-11xl mx-auto px-4 sm:px-6 xl:px-8 3xl:px-12 4xl:px-20">
        <div className="text-center mb-14 xl:mb-18 3xl:mb-20">
          <p className="text-sm xl:text-base font-bold uppercase tracking-widest text-forest-600 mb-3">{t.sectionLabel}</p>
          <h2 className="text-4xl xl:text-5xl 3xl:text-6xl 4xl:text-7xl font-extrabold text-gray-900 leading-tight">
            {t.h2a} <span className="gradient-text">{t.h2b}</span>
          </h2>
        </div>

        <div className="grid md:grid-cols-3 gap-6 xl:gap-8 3xl:gap-10">
          {t.items.map((item) => (
            <div key={item.name} className="card-lift bg-white rounded-2xl border border-gray-100 shadow-sm p-6 xl:p-8 3xl:p-10 flex flex-col">
              <div className="flex gap-0.5 mb-4">
                {Array.from({ length: 5 }).map((_, i) => (
                  <svg key={i} className="w-4 h-4 xl:w-5 xl:h-5 text-gold-500" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                ))}
              </div>
              <blockquote className="text-gray-600 text-sm xl:text-base 3xl:text-lg leading-relaxed flex-1">
                &ldquo;{item.quote}&rdquo;
              </blockquote>
              <div className="flex items-center gap-3 mt-5 pt-5 border-t border-gray-100">
                <div className={`w-9 h-9 xl:w-11 xl:h-11 rounded-full flex items-center justify-center text-white font-bold text-sm xl:text-base flex-shrink-0 bg-gradient-to-br ${item.color}`}>
                  {item.avatar}
                </div>
                <div>
                  <p className="font-semibold text-gray-900 text-sm xl:text-base">{item.name}</p>
                  <p className="text-gray-400 text-xs xl:text-sm">{item.role}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

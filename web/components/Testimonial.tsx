"use client";

import { useState, useRef, useCallback, useEffect } from "react";
import type { Copy } from "@/lib/i18n";

const StarIcon = ({ filled }: { filled: boolean }) => (
  <svg
    className={`w-4 h-4 xl:w-[18px] xl:h-[18px] ${filled ? "text-gold-500" : "text-gray-200"}`}
    fill="currentColor"
    viewBox="0 0 20 20"
  >
    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
  </svg>
);

const ChevronLeft = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M15 19l-7-7 7-7" />
  </svg>
);

const ChevronRight = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M9 5l7 7-7 7" />
  </svg>
);

export default function Testimonial({ t }: { t: Copy["testimonials"] }) {
  const isFr = t.sectionLabel === "Témoignages";
  const verifiedLabel = isFr ? "Utilisateur vérifié via WhatsApp" : "Verified Tassi user via WhatsApp";
  const total = t.items.length;
  const avgRating = (t.items.reduce((s, item) => s + (item.stars ?? 5), 0) / total).toFixed(1);

  const trackRef = useRef<HTMLDivElement>(null);
  const [activeDot, setActiveDot] = useState(0);
  const [canPrev, setCanPrev] = useState(false);
  const [canNext, setCanNext] = useState(true);

  const getCardWidth = useCallback((): number => {
    const el = trackRef.current;
    if (!el || !el.children.length) return 0;
    return (el.children[0] as HTMLElement).getBoundingClientRect().width;
  }, []);

  const syncState = useCallback(() => {
    const el = trackRef.current;
    if (!el) return;
    const maxScroll = el.scrollWidth - el.clientWidth;
    setCanPrev(el.scrollLeft > 4);
    setCanNext(el.scrollLeft < maxScroll - 4);
    const cardW = getCardWidth();
    if (cardW > 0) setActiveDot(Math.round(el.scrollLeft / cardW));
  }, [getCardWidth]);

  useEffect(() => {
    syncState();
    window.addEventListener("resize", syncState, { passive: true });
    return () => window.removeEventListener("resize", syncState);
  }, [syncState]);

  const slide = useCallback((dir: 1 | -1) => {
    const el = trackRef.current;
    if (!el) return;
    const cardW = getCardWidth();
    if (cardW > 0) el.scrollBy({ left: dir * cardW, behavior: "smooth" });
  }, [getCardWidth]);

  const scrollToIndex = useCallback((index: number) => {
    const el = trackRef.current;
    if (!el) return;
    const cardW = getCardWidth();
    if (cardW > 0) el.scrollTo({ left: index * cardW, behavior: "smooth" });
  }, [getCardWidth]);

  return (
    <section className="py-24 xl:py-32 3xl:py-40 4xl:py-56 bg-white">
      <div className="max-w-7xl 3xl:max-w-9xl 4xl:max-w-11xl mx-auto px-4 sm:px-6 xl:px-8 3xl:px-12 4xl:px-28">

        {/* Header */}
        <div className="text-center mb-12 xl:mb-16 4xl:mb-24">
          <p className="text-sm xl:text-base 4xl:text-xl font-bold uppercase tracking-widest text-forest-600 mb-3">
            {t.sectionLabel}
          </p>
          <h2 className="text-4xl xl:text-5xl 3xl:text-6xl 4xl:text-7xl font-extrabold text-gray-900 leading-tight mb-6">
            {t.h2a} <span className="gradient-text">{t.h2b}</span>
          </h2>
          {/* Aggregate rating */}
          <div className="inline-flex items-center gap-2.5 bg-forest-50 border border-forest-100 px-5 py-2.5 rounded-full">
            <div className="flex gap-0.5">
              {[1, 2, 3, 4, 5].map((i) => <StarIcon key={i} filled />)}
            </div>
            <span className="font-bold text-gray-900 text-sm xl:text-base">{avgRating} / 5</span>
            <span className="text-gray-300 select-none">·</span>
            <span className="text-gray-500 text-xs xl:text-sm">{t.aggregateLabel} — {t.aggregateCount}</span>
          </div>
        </div>

        {/* Slider wrapper — positions the floating nav buttons */}
        <div className="relative">
          {/* Prev button */}
          <button
            onClick={() => slide(-1)}
            disabled={!canPrev}
            aria-label={isFr ? "Témoignage précédent" : "Previous testimonial"}
            className={`
              absolute left-0 top-1/2 -translate-y-1/2 -translate-x-3 sm:-translate-x-5 xl:-translate-x-7
              z-10 w-10 h-10 xl:w-12 xl:h-12 rounded-full bg-white shadow-lg border
              flex items-center justify-center transition-all duration-200
              ${canPrev
                ? "border-gray-200 text-gray-700 hover:border-forest-400 hover:text-forest-700 hover:shadow-xl hover:shadow-forest-100/60 hover:scale-105"
                : "border-gray-100 text-gray-300 cursor-not-allowed opacity-50"
              }
            `}
          >
            <ChevronLeft />
          </button>

          {/* Scrollable track */}
          <div
            ref={trackRef}
            onScroll={syncState}
            className="scrollbar-hide flex overflow-x-auto snap-x snap-mandatory gap-4 xl:gap-5 3xl:gap-6 4xl:gap-8"
            style={{ scrollbarWidth: "none", msOverflowStyle: "none" }}
          >
            {t.items.map((item) => {
              const stars = item.stars ?? 5;
              return (
                <div
                  key={item.name}
                  className="
                    flex-shrink-0 snap-start
                    w-[82vw] sm:w-[calc(50%-8px)] lg:w-[calc(33.333%-11px)] xl:w-[calc(33.333%-14px)] 3xl:w-[calc(33.333%-16px)] 4xl:w-[calc(33.333%-22px)]
                    card-lift bg-white rounded-2xl border border-gray-100 border-l-4 border-l-forest-200
                    shadow-sm p-6 xl:p-8 3xl:p-10 flex flex-col
                  "
                >
                  {/* Verified badge */}
                  <div className="inline-flex items-center gap-1.5 bg-green-50 border border-green-100 text-green-700 px-2.5 py-1 rounded-full mb-4 self-start">
                    <svg className="w-3 h-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    <span className="text-[9px] xl:text-[10px] font-semibold tracking-wide">{verifiedLabel}</span>
                  </div>

                  {/* Stars */}
                  <div className="flex gap-0.5 mb-4">
                    {[1, 2, 3, 4, 5].map((i) => <StarIcon key={i} filled={i <= stars} />)}
                  </div>

                  {/* Quote */}
                  <blockquote className="text-gray-600 text-sm xl:text-[15px] 3xl:text-base leading-relaxed flex-1">
                    &ldquo;{item.quote}&rdquo;
                  </blockquote>

                  {/* Author */}
                  <div className="flex items-center gap-3 mt-5 pt-5 border-t border-gray-100">
                    <div
                      className={`w-9 h-9 xl:w-11 xl:h-11 rounded-full flex items-center justify-center text-white font-bold text-sm xl:text-base flex-shrink-0 bg-gradient-to-br ${item.color}`}
                    >
                      {item.avatar}
                    </div>
                    <div>
                      <p className="font-semibold text-gray-900 text-sm xl:text-base">{item.name}</p>
                      <p className="text-gray-400 text-xs xl:text-sm">{item.role}</p>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Next button */}
          <button
            onClick={() => slide(1)}
            disabled={!canNext}
            aria-label={isFr ? "Témoignage suivant" : "Next testimonial"}
            className={`
              absolute right-0 top-1/2 -translate-y-1/2 translate-x-3 sm:translate-x-5 xl:translate-x-7
              z-10 w-10 h-10 xl:w-12 xl:h-12 rounded-full bg-white shadow-lg border
              flex items-center justify-center transition-all duration-200
              ${canNext
                ? "border-gray-200 text-gray-700 hover:border-forest-400 hover:text-forest-700 hover:shadow-xl hover:shadow-forest-100/60 hover:scale-105"
                : "border-gray-100 text-gray-300 cursor-not-allowed opacity-50"
              }
            `}
          >
            <ChevronRight />
          </button>
        </div>

        {/* Dot indicators */}
        <div className="flex items-center justify-center gap-2 mt-8 xl:mt-10">
          {t.items.map((_, i) => (
            <button
              key={i}
              onClick={() => scrollToIndex(i)}
              aria-label={`${isFr ? "Témoignage" : "Testimonial"} ${i + 1}`}
              className={`rounded-full transition-all duration-300 ease-out ${
                activeDot === i
                  ? "w-7 h-2 bg-forest-600"
                  : "w-2 h-2 bg-gray-200 hover:bg-gray-400"
              }`}
            />
          ))}
        </div>

        {/* Swipe hint on mobile */}
        <p className="text-center text-gray-400 text-xs mt-3 sm:hidden">
          {isFr ? "Glissez pour voir plus" : "Swipe to see more"}
        </p>
      </div>
    </section>
  );
}

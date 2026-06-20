"use client";

import { useRef, useEffect, useState, useCallback } from "react";
import type { Copy } from "@/lib/i18n";

function parseStat(value: string): { prefix: string; num: number; suffix: string } {
  const match = value.match(/^([^0-9]*)(\d+)(.*)$/);
  if (!match) return { prefix: "", num: 0, suffix: value };
  return { prefix: match[1], num: parseInt(match[2], 10), suffix: match[3] };
}

function easeOutCubic(t: number): number {
  return 1 - Math.pow(1 - t, 3);
}

function AnimatedStat({
  value,
  label,
  delay,
}: {
  value: string;
  label: string;
  delay: number;
}) {
  const { prefix, num, suffix } = parseStat(value);
  const [display, setDisplay] = useState(0);
  const [fired, setFired] = useState(false);
  const cellRef = useRef<HTMLDivElement>(null);
  const rafRef = useRef<number>(0);

  const animate = useCallback(() => {
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reducedMotion) {
      setDisplay(num);
      return;
    }

    const duration = 1500;
    const startTime = performance.now() + delay;

    const tick = (now: number) => {
      if (now < startTime) {
        rafRef.current = requestAnimationFrame(tick);
        return;
      }
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = easeOutCubic(progress);
      setDisplay(Math.round(eased * num));
      if (progress < 1) {
        rafRef.current = requestAnimationFrame(tick);
      }
    };

    rafRef.current = requestAnimationFrame(tick);
  }, [num, delay]);

  useEffect(() => {
    const el = cellRef.current;
    if (!el) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !fired) {
          setFired(true);
          animate();
        }
      },
      { threshold: 0.4 }
    );

    observer.observe(el);
    return () => {
      observer.disconnect();
      cancelAnimationFrame(rafRef.current);
    };
  }, [fired, animate]);

  return (
    <div
      ref={cellRef}
      className="flex flex-col items-center justify-center py-8 xl:py-10 3xl:py-14 4xl:py-20 px-4 text-center"
    >
      <p
        className="text-3xl xl:text-4xl 3xl:text-5xl 4xl:text-7xl font-extrabold gradient-text-gold leading-tight tabular-nums"
        aria-label={value}
      >
        {prefix}
        {display}
        {suffix}
      </p>
      <p className="text-sm xl:text-base 3xl:text-lg 4xl:text-xl text-gray-400 mt-2 font-medium">{label}</p>
    </div>
  );
}

function PillsStat({
  pills,
  label,
}: {
  pills: readonly string[];
  label: string;
}) {
  return (
    <div className="flex flex-col items-center justify-center py-8 xl:py-10 3xl:py-14 4xl:py-20 px-4 text-center">
      <div className="flex items-center gap-1.5" aria-label={pills.join(" · ")}>
        {pills.map((pill, i) => (
          <span key={pill}>
            <span className="bg-green-100 text-green-800 text-xs font-semibold px-2 py-0.5 rounded-full">
              {pill}
            </span>
            {i < pills.length - 1 && (
              <span className="text-gray-300 text-xs ml-1.5">·</span>
            )}
          </span>
        ))}
      </div>
      <p className="text-sm xl:text-base 3xl:text-lg 4xl:text-xl text-gray-400 mt-2 font-medium">{label}</p>
    </div>
  );
}

export default function StatsBar({ stats }: { stats: Copy["stats"] }) {
  return (
    <section
      className="relative bg-white"
      style={{
        borderTop: "1px solid #fef3c7",
        borderBottom: "1px solid #fef3c7",
        background: "linear-gradient(180deg, #fffbeb 0%, #ffffff 60%)",
        boxShadow: "inset 0 1px 0 #fde68a, inset 0 -1px 0 #fde68a",
      }}
    >
      <div className="max-w-7xl 3xl:max-w-9xl 4xl:max-w-11xl mx-auto px-4 sm:px-6 xl:px-8 3xl:px-12 4xl:px-28">
        <div className="grid grid-cols-2 md:grid-cols-4 divide-x divide-y md:divide-y-0 divide-forest-50">
          {stats.map((s, i) =>
            "pills" in s && s.pills ? (
              <PillsStat key={s.label} pills={s.pills} label={s.label} />
            ) : (
              <AnimatedStat key={s.label} value={s.value} label={s.label} delay={i * 120} />
            )
          )}
        </div>
      </div>
    </section>
  );
}

import type { Copy } from "@/lib/i18n";

export default function StatsBar({ stats }: { stats: Copy["stats"] }) {
  return (
    <section className="bg-white border-y border-gray-100">
      <div className="max-w-7xl 3xl:max-w-9xl mx-auto px-4 sm:px-6 xl:px-8 3xl:px-12">
        <div className="grid grid-cols-2 md:grid-cols-4 divide-x divide-y md:divide-y-0 divide-gray-100">
          {stats.map((s) => (
            <div key={s.label} className="flex flex-col items-center justify-center py-8 xl:py-10 3xl:py-14 px-4 text-center">
              <p className="text-3xl xl:text-4xl 3xl:text-5xl font-extrabold gradient-text leading-tight">{s.value}</p>
              <p className="text-sm xl:text-base 3xl:text-lg text-gray-400 mt-1 font-medium">{s.label}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

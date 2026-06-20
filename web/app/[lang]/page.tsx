import { notFound } from "next/navigation";
import { copy, type Lang } from "@/lib/i18n";
import Nav from "@/components/Nav";
import Hero from "@/components/Hero";
import StatsBar from "@/components/StatsBar";
import Features from "@/components/Features";
import HowItWorks from "@/components/HowItWorks";
import Testimonial from "@/components/Testimonial";
import Faq from "@/components/Faq";
import Pricing from "@/components/Pricing";
import CtaBanner from "@/components/CtaBanner";
import Footer from "@/components/Footer";

export function generateStaticParams() {
  return [{ lang: "fr" }, { lang: "en" }];
}

export default async function LangPage({
  params,
}: {
  params: Promise<{ lang: string }>;
}) {
  const { lang } = await params;
  if (lang !== "fr" && lang !== "en") notFound();
  const t = copy[lang as Lang];

  return (
    <main className="min-h-screen overflow-x-hidden">
      <Nav t={t.nav} lang={lang as Lang} />
      <Hero t={t.hero} isEn={lang === "en"} />
      <StatsBar stats={t.stats} />
      <Features t={t.features} />
      <HowItWorks t={t.howItWorks} />
      <Testimonial t={t.testimonials} />
      <Faq t={t.faq} />
      <Pricing t={t.pricing} />
      <CtaBanner t={t.ctaBanner} />
      <Footer t={t.footer} lang={lang as Lang} />
    </main>
  );
}

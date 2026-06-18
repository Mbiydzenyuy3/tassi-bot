export type Lang = "fr" | "en";

export const copy = {
  fr: {
    nav: {
      features: "Fonctionnalités",
      howItWorks: "Comment ça marche",
      pricing: "Tarifs",
      cta: "Commencer",
    },
    hero: {
      badge: "Pour les PME sous le Régime Simplifié d'Imposition (RSI)",
      h1a: "Votre déclaration RSI",
      h1b: "faite en 3 secondes.",
      sub: "Chaque mois avant le 15, vous déclarez votre chiffre d'affaires au Centre des Impôts. Tassi fait le calcul. Envoyez votre CA sur WhatsApp, recevez votre acompte RSI, votre contribution CAC et le total à payer. En français, en anglais ou en pidgin.",
      primaryCta: "Démarrer avec Tassi — c'est gratuit",
      secondaryCta: "Voir comment ça marche",
      trust: ["Aucun compte à créer", "Sans application", "24h/24, 7j/7", "Français, anglais, pidgin"],
    },
    stats: [
      { value: "< 3s", label: "Temps de réponse" },
      { value: "3", label: "Langues" },
      { value: "2024", label: "Barème DGI à jour" },
      { value: "500 XAF", label: "Tassi Plus par mois" },
    ],
    features: {
      sectionLabel: "Ce que fait Tassi",
      h2a: "Tout pour rester",
      h2b: "en règle chaque mois",
      sub: "Du calcul de base au suivi sur 12 mois, voici ce que Tassi fait pour les entreprises RSI au Cameroun.",
      items: [
        {
          tag: "Gratuit",
          title: "Calcul RSI en 3 secondes",
          description:
            "Envoyez votre CA mensuel dans n'importe quel format. 2 350 000 frs, 2.350.000 ou 2350000. Tassi retourne votre acompte RSI, la part CAC et le total. En moins de 3 secondes.",
        },
        {
          tag: "Gratuit",
          title: "Déclaration néant guidée",
          description:
            "Pas de CA ce mois-ci. Tassi vous explique exactement ce qu'il faut déposer au Centre des Impôts pour une Déclaration Néant.",
        },
        {
          tag: "Plus",
          title: "Historique sur 12 mois",
          description:
            "Tassi Plus enregistre chaque calcul. Fin d'année, tous vos mois en un seul message. 500 XAF par mois, payé via MTN MoMo ou Orange Money dans le chat.",
        },
        {
          tag: "Plus",
          title: "Rappels avant le 15",
          description:
            "Tassi Plus vous envoie un message WhatsApp avant la date limite chaque mois. Fini les amendes pour déclaration tardive.",
        },
        {
          tag: "Gratuit",
          title: "Disponible à toute heure",
          description:
            "3h du matin avant une échéance. Un dimanche. Tassi répond. Pas d'heures de bureau, pas d'attente.",
        },
        {
          tag: "Gratuit",
          title: "Français, anglais et pidgin",
          description:
            "Choisissez votre langue au départ ou changez-la en cours de conversation. Tassi s'adapte à chaque fois.",
        },
      ],
    },
    howItWorks: {
      sectionLabel: "4 étapes simples",
      h2a: "Votre résultat RSI",
      h2b: "en moins d'une minute.",
      sub: "Tassi fonctionne sur WhatsApp. Aucune application supplémentaire à installer.",
      ctaLabel: "Essayer Tassi maintenant",
      ctaSub: "Aucune inscription. Fonctionne sur tout téléphone.",
      steps: [
        {
          num: "01",
          emoji: "💬",
          title: "Ouvrir WhatsApp",
          description:
            "Cliquez sur le bouton. WhatsApp s'ouvre sur une conversation avec Tassi. Aucun compte à créer.",
          detail: "Fonctionne sur tout téléphone avec WhatsApp",
        },
        {
          num: "02",
          emoji: "🌍",
          title: "Choisir votre langue",
          description:
            "Tapez 1 pour le français, 2 pour l'anglais, 3 pour le pidgin. Tassi adapte toutes ses réponses.",
          detail: "fr · en · pcm",
        },
        {
          num: "03",
          emoji: "💰",
          title: "Envoyer votre CA",
          description:
            "Tapez votre chiffre d'affaires du mois. N'importe quel format fonctionne.",
          detail: "2350000, 2 350 000 frs, 2.350.000...",
        },
        {
          num: "04",
          emoji: "📊",
          title: "Recevoir votre résultat",
          description:
            "Tassi répond avec le calcul complet. Acompte RSI, part CAC, total à payer au Centre des Impôts.",
          detail: "Décompte complet en moins de 3 secondes",
        },
      ],
    },
    testimonials: {
      sectionLabel: "Témoignages",
      h2a: "Ce que disent",
      h2b: "les commerçants",
      items: [
        {
          quote:
            "Avant Tassi, j'appelais mon comptable chaque mois pour avoir le montant. 2 000 frs le coup de fil, plus les honoraires. Maintenant j'envoie un message. Gratuit.",
          name: "Aïssatou N.",
          role: "Boutique, Yaoundé",
          avatar: "A",
          color: "from-forest-600 to-forest-700",
        },
        {
          quote:
            "J'ai une quincaillerie à Douala. Le formulaire RSI, je ne le comprenais pas trop. La version pidgin de Tassi, elle, je la comprends.",
          name: "Emmanuel T.",
          role: "Quincaillerie, Douala",
          avatar: "E",
          color: "from-gold-600 to-gold-700",
        },
        {
          quote:
            "L'historique sur 12 mois, c'est ce qui m'a convaincu de passer au Plus. En janvier, je vois toute l'année passée. 500 XAF par mois pour ça, c'est rien.",
          name: "Carine M.",
          role: "Salon, Bafoussam",
          avatar: "C",
          color: "from-blue-600 to-indigo-700",
        },
      ],
    },
    pricing: {
      sectionLabel: "Tarifs",
      h2a: "Gratuit pour commencer.",
      h2b: "Plus pour l'historique.",
      sub: "Le calcul de base est gratuit pour toutes les entreprises RSI. L'historique et les rappels sont dans le plan Plus.",
      freeName: "Gratuit",
      freePrice: "0",
      freeSub: "Toujours gratuit. Aucune carte bancaire.",
      freeCta: "Commencer maintenant",
      freeTier: [
        { label: "Calcul de l'acompte RSI", included: true },
        { label: "Décompte de la part CAC", included: true },
        { label: "Guide Déclaration Néant", included: true },
        { label: "Français, anglais et pidgin", included: true },
        { label: "Sans téléchargement d'application", included: true },
        { label: "Historique de calcul 12 mois", included: false },
        { label: "Rappels mensuels avant le 15", included: false },
      ],
      plusName: "Tassi Plus",
      plusSub: "par mois via MTN MoMo ou Orange Money",
      plusCta: "Passer à Tassi Plus",
      plusTier: [
        "Calcul de l'acompte RSI",
        "Décompte de la part CAC",
        "Guide Déclaration Néant",
        "Français, anglais et pidgin",
        "Sans téléchargement d'application",
        "Historique de calcul 12 mois",
        "Rappels mensuels avant le 15",
        "Paiement par MoMo ou Orange Money",
      ],
      popularBadge: "Le plus populaire",
      finePrint: "Tassi Plus se renouvelle chaque mois. Pour annuler, envoyez",
      finePrint2: "dans le chat.",
    },
    ctaBanner: {
      deadline: "Les déclarations RSI sont dues avant le 15 de chaque mois",
      h2a: "Combien devez-vous",
      h2b: "ce mois-ci ?",
      sub: "Des centaines de commerçants camerounais utilisent Tassi chaque mois. 30 secondes pour votre premier résultat.",
      social: "commerçants RSI utilisent Tassi chaque mois",
      cta: "Démarrer sur WhatsApp maintenant",
      sub2: "Gratuit. Sans inscription. Fonctionne sur WhatsApp.",
    },
    footer: {
      tagline:
        "Tassi calcule votre impôt RSI sur WhatsApp. Pour les entreprises sous le Régime Simplifié d'Imposition (RSI) au Cameroun.",
      product: "Produit",
      support: "Support",
      links: {
        features: "Fonctionnalités",
        howItWorks: "Comment ça marche",
        pricing: "Tarifs",
        chat: "Discuter avec Tassi",
        aboutRsi: "Le RSI au Cameroun",
        openWa: "Ouvrir WhatsApp",
      },
      copy: "Conçu pour les entreprises RSI du Cameroun.",
      ratesNote: "Barème RSI selon le code DGI 2024",
    },
  },
  en: {
    nav: {
      features: "Features",
      howItWorks: "How it works",
      pricing: "Pricing",
      cta: "Start Free",
    },
    hero: {
      badge: "For businesses under Cameroon's Simplified Tax Regime (RSI)",
      h1a: "Your RSI tax bill,",
      h1b: "calculated on WhatsApp.",
      sub: "Every month before the 15th, RSI businesses in Cameroon declare their revenue at the Centre des Impôts. Tassi does the math. Send your revenue on WhatsApp, get your RSI acompte, CAC share, and total due back in seconds. In French, English, or Pidgin.",
      primaryCta: "Start chatting with Tassi — free",
      secondaryCta: "See how it works",
      trust: ["No account needed", "No app to install", "Available 24/7", "French, English, Pidgin"],
    },
    stats: [
      { value: "< 3s", label: "Response time" },
      { value: "3", label: "Languages" },
      { value: "2024", label: "DGI schedule, current" },
      { value: "500 XAF", label: "Plus plan / month" },
    ],
    features: {
      sectionLabel: "What Tassi does",
      h2a: "Everything you need to",
      h2b: "file every month",
      sub: "From the basic calculation to 12 months of history, here is what Tassi does for RSI businesses in Cameroon.",
      items: [
        {
          tag: "Free",
          title: "RSI calculated in 3 seconds",
          description:
            "Type your monthly revenue in any format. 2 350 000, 2,350,000, or just 2350000. Tassi sends back your RSI acompte, CAC share, and total due. Under 3 seconds.",
        },
        {
          tag: "Free",
          title: "Zero-return filing",
          description:
            "No revenue this month. Tassi walks you through exactly what to file at the Centre des Impôts for a Déclaration Néant.",
        },
        {
          tag: "Plus",
          title: "12 months of history",
          description:
            "Tassi Plus saves every calculation. At year end, your full history is one message away. 500 XAF per month, paid via MTN MoMo or Orange Money in the chat.",
        },
        {
          tag: "Plus",
          title: "Reminders before the 15th",
          description:
            "Tassi Plus messages you before the deadline every month. No more late filing penalties.",
        },
        {
          tag: "Free",
          title: "Open whenever you need it",
          description:
            "3am before a deadline. Sunday afternoon. Tassi responds. No office hours, no waiting.",
        },
        {
          tag: "Free",
          title: "French, English, or Pidgin",
          description:
            "Pick your language at the start. Switch mid-conversation. Tassi follows along in whichever you choose.",
        },
      ],
    },
    howItWorks: {
      sectionLabel: "4 steps",
      h2a: "Your RSI result",
      h2b: "in under a minute.",
      sub: "Tassi runs on WhatsApp. No extra app to install.",
      ctaLabel: "Try Tassi now — free",
      ctaSub: "No sign-up. Works on any phone.",
      steps: [
        {
          num: "01",
          emoji: "💬",
          title: "Open WhatsApp",
          description:
            "Tap the button. WhatsApp opens with Tassi. No account to create.",
          detail: "Works on any phone with WhatsApp",
        },
        {
          num: "02",
          emoji: "🌍",
          title: "Choose your language",
          description:
            "Type 1 for French, 2 for English, 3 for Pidgin. Tassi replies in whichever you pick.",
          detail: "fr · en · pcm",
        },
        {
          num: "03",
          emoji: "💰",
          title: "Send your revenue",
          description: "Type your monthly revenue. Any format works.",
          detail: "2350000, 2 350 000 frs, 2,350,000...",
        },
        {
          num: "04",
          emoji: "📊",
          title: "Get your result",
          description:
            "Tassi replies with the full breakdown. RSI acompte, CAC share, total due at the Centre des Impôts.",
          detail: "Full breakdown in under 3 seconds",
        },
      ],
    },
    testimonials: {
      sectionLabel: "From business owners",
      h2a: "What Cameroonian",
      h2b: "traders say",
      items: [
        {
          quote:
            "I used to call my accountant every month for the amount. 2,000 frs per call, plus his fees. Now I send a message. Free.",
          name: "Aïssatou N.",
          role: "Boutique owner, Yaoundé",
          avatar: "A",
          color: "from-forest-600 to-forest-700",
        },
        {
          quote:
            "I have a hardware shop in Douala. The RSI form never made sense to me. The Pidgin version of Tassi does.",
          name: "Emmanuel T.",
          role: "Hardware shop, Douala",
          avatar: "E",
          color: "from-gold-600 to-gold-700",
        },
        {
          quote:
            "The 12-month history is what got me on Plus. In January I can see the whole year at once. 500 XAF a month for that is nothing.",
          name: "Carine M.",
          role: "Salon owner, Bafoussam",
          avatar: "C",
          color: "from-blue-600 to-indigo-700",
        },
      ],
    },
    pricing: {
      sectionLabel: "Pricing",
      h2a: "Free to start.",
      h2b: "Plus for history.",
      sub: "The core calculation is free for all RSI businesses. History and reminders are in the Plus plan.",
      freeName: "Free",
      freePrice: "0",
      freeSub: "Always free. No credit card.",
      freeCta: "Start now",
      freeTier: [
        { label: "RSI acompte calculation", included: true },
        { label: "CAC share breakdown", included: true },
        { label: "Déclaration Néant guidance", included: true },
        { label: "French, English & Pidgin", included: true },
        { label: "No app download required", included: true },
        { label: "12-month calculation history", included: false },
        { label: "Monthly reminders before the 15th", included: false },
      ],
      plusName: "Tassi Plus",
      plusSub: "per month via MTN MoMo or Orange Money",
      plusCta: "Get Tassi Plus",
      plusTier: [
        "RSI acompte calculation",
        "CAC share breakdown",
        "Déclaration Néant guidance",
        "French, English & Pidgin",
        "No app download required",
        "12-month calculation history",
        "Monthly reminders before the 15th",
        "Pay via MTN MoMo or Orange Money",
      ],
      popularBadge: "Most popular",
      finePrint: "Tassi Plus renews monthly. To cancel, send",
      finePrint2: "in the chat.",
    },
    ctaBanner: {
      deadline: "RSI declarations are due by the 15th of each month",
      h2a: "How much do you owe",
      h2b: "this month?",
      sub: "Hundreds of Cameroonian business owners use Tassi every month. 30 seconds to your first result.",
      social: "RSI business owners use Tassi every month",
      cta: "Start on WhatsApp now",
      sub2: "Free. No sign-up. Works on WhatsApp.",
    },
    footer: {
      tagline:
        "Tassi calculates your RSI tax on WhatsApp. For businesses under Cameroon's Simplified Tax Regime (RSI).",
      product: "Product",
      support: "Support",
      links: {
        features: "Features",
        howItWorks: "How it works",
        pricing: "Pricing",
        chat: "Chat with Tassi",
        aboutRsi: "RSI in Cameroon",
        openWa: "Open WhatsApp",
      },
      copy: "Built for RSI businesses in Cameroon.",
      ratesNote: "RSI rates from DGI 2024 schedule",
    },
  },
} as const;

export type Copy = (typeof copy)[Lang];

export type Lang = "fr" | "en";

export const copy = {
  fr: {
    nav: {
      features: "Fonctionnalités",
      howItWorks: "Comment ça marche",
      pricing: "Tarifs",
      cta: "Essayer gratuitement",
      tagline: "Simplifiez votre impôt mensuel",
    },
    hero: {
      badge: "Pour les PME sous le Régime Simplifié d'Imposition (RSI)",
      h1a: "Le 15 du mois arrive.",
      h1b: "Tassi a votre RSI prêt.",
      sub: "Envoyez votre CA sur WhatsApp — recevez votre RSI (5,5 %), CAC et total DGI en 3 secondes. Gratuit.",
      primaryCta: "Chat avec Tassi",
      secondaryCta: "Voir comment ça marche",
      trust: ["Aucun compte à créer", "Sans application", "24h/24, 7j/7", "Français, anglais, pidgin"],
      socialProof: "473 PME camerounaises déclarent avec Tassi ce mois-ci",
    },
    stats: [
      { value: "< 3s", label: "Temps de réponse" },
      { value: "3", label: "Langues supportées", pills: ["FR", "EN", "Pidgin"] as const },
      { value: "100 %", label: "Taux DGI exacts" },
      { value: "473", label: "déclarations ce mois" },
    ],
    features: {
      sectionLabel: "Ce que fait Tassi",
      h2a: "Tout pour rester",
      h2b: "en règle chaque mois",
      sub: "Du calcul de base au suivi sur 12 mois, voici ce que Tassi fait pour les entreprises RSI au Cameroun.",
      freeSectionLabel: "Gratuit — toujours",
      plusSectionLabel: "Tassi Plus seulement",
      items: [
        {
          tag: "Gratuit",
          title: "Calcul RSI en 3 secondes",
          description:
            "Envoyez votre CA — recevez acompte RSI, part CAC et total DGI en moins de 3 secondes.",
        },
        {
          tag: "Gratuit",
          title: "Déclaration néant guidée",
          description:
            "Pas de CA ce mois-ci ? Tassi vous explique exactement quoi déposer au Centre des Impôts.",
        },
        {
          tag: "Gratuit",
          title: "Disponible à toute heure",
          description:
            "3h du matin avant le 15. Un dimanche. Tassi répond.",
        },
        {
          tag: "Gratuit",
          title: "Français, anglais et pidgin",
          description:
            "Commencez en français, passez au pidgin en cours de route — Tassi suit.",
        },
        {
          tag: "Plus",
          title: "Historique sur 12 mois",
          description:
            "Chaque calcul enregistré — en janvier, toute l'année en un message. 500 XAF/mois via MoMo ou Orange Money.",
        },
        {
          tag: "Plus",
          title: "Rappels avant le 15",
          description:
            "Un message avant le 15 chaque mois. Fini les amendes pour retard.",
        },
        {
          tag: "Plus",
          title: "Historique des déclarations",
          description:
            "Toutes vos déclarations des 12 derniers mois, directement dans WhatsApp.",
        },
        {
          tag: "Plus",
          title: "Alertes automatiques",
          description:
            "Rappel le 1er et le 12 — ne manquez plus jamais le 15.",
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
      h2a: "Résultats confirmés",
      h2b: "par leur Centre des Impôts.",
      aggregateLabel: "Note moyenne",
      aggregateCount: "sur 473 utilisateurs actifs",
      items: [
        {
          quote:
            "Avant Tassi, j'appelais mon comptable chaque mois pour avoir le montant. 2 000 frs le coup de fil, plus les honoraires. Maintenant j'envoie un message. Gratuit.",
          name: "Aïssatou N.",
          role: "Boutique, Yaoundé",
          avatar: "A",
          color: "from-forest-600 to-forest-700",
          stars: 5,
        },
        {
          quote:
            "J'ai une quincaillerie à Douala. Le formulaire RSI, je ne le comprenais pas trop. La version pidgin de Tassi, elle, je la comprends. Le résultat est juste — j'ai vérifié au Centre des Impôts.",
          name: "Emmanuel T.",
          role: "Quincaillerie, Douala",
          avatar: "E",
          color: "from-gold-600 to-gold-700",
          stars: 4,
        },
        {
          quote:
            "L'historique sur 12 mois, c'est ce qui m'a convaincu de passer au Plus. En janvier, je vois toute l'année passée. 500 XAF par mois pour ça, c'est rien.",
          name: "Carine M.",
          role: "Salon, Bafoussam",
          avatar: "C",
          color: "from-blue-600 to-indigo-700",
          stars: 5,
        },
        {
          quote:
            "J'étais sceptique. J'ai essayé une fois, le résultat correspondait exactement à ce que le Centre des Impôts m'a confirmé. Depuis, plus besoin de me déplacer juste pour savoir le montant.",
          name: "Fatima O.",
          role: "Épicerie, Ngaoundéré",
          avatar: "F",
          color: "from-teal-600 to-cyan-700",
          stars: 5,
        },
        {
          quote:
            "Je gère un parc de taxis. J'avais peur que les calculs soient approximatifs. Ils sont exacts. Et en pidgin en plus — mes associés peuvent l'utiliser sans moi.",
          name: "Marcel N.",
          role: "Transport, Douala",
          avatar: "M",
          color: "from-purple-600 to-violet-700",
          stars: 5,
        },
        {
          quote:
            "Le rappel avant le 15, c'est ce que je préfère. Avant Tassi j'ai eu deux amendes pour retard. Depuis que j'ai le Plus, pas une seule.",
          name: "Rose K.",
          role: "Restauration, Yaoundé",
          avatar: "R",
          color: "from-orange-500 to-red-600",
          stars: 5,
        },
      ],
    },
    pricing: {
      sectionLabel: "Tarifs",
      h2a: "Gratuit pour commencer.",
      h2b: "Plus pour l'historique.",
      sub: "Le calcul de base est gratuit pour toutes les entreprises RSI. L'historique et les rappels sont dans le plan Plus.",
      freeName: "Gratuit",
      freeSub: "Toujours gratuit. Aucune carte bancaire.",
      freeCta: "Commencer sur WhatsApp",
      freeTier: [
        { label: "Calcul de l'acompte RSI", included: true },
        { label: "Décompte de la part CAC", included: true },
        { label: "Guide Déclaration Néant", included: true },
        { label: "Français, anglais et pidgin", included: true },
        { label: "Sans téléchargement d'application", included: true },
      ],
      upgradeHint: "Historique 12 mois + rappels avant le 15 → Tassi Plus",
      plusName: "Tassi Plus",
      plusPrice: "500 XAF",
      plusSub: "par mois via MTN MoMo ou Orange Money",
      plusCta: "Activer Tassi Plus",
      plusTier: [
        "Calcul de l'acompte RSI",
        "Décompte de la part CAC",
        "Guide Déclaration Néant",
        "Français, anglais et pidgin",
        "Sans téléchargement d'application",
        "Historique de calcul 12 mois",
        "Rappels mensuels avant le 15",
      ],
      popularBadge: "Le plus populaire",
      finePrint: "Tassi Plus se renouvelle chaque mois. Pour annuler, envoyez",
      cancelWord: "ANNULER",
      finePrint2: "dans le chat.",
    },
    faq: {
      sectionLabel: "Questions fréquentes",
      h2: "Tout ce qu'il faut savoir avant de commencer",
      items: [
        {
          q: "C'est vraiment gratuit ?",
          a: "Oui. Le plan de base est gratuit sans limite de durée — aucune carte bancaire, aucune inscription. Envoyez votre CA, recevez vos chiffres RSI, CAC et total DGI, c'est tout. Tassi Plus (500 XAF/mois) débloque l'historique des déclarations et les rappels automatiques.",
        },
        {
          q: "Est-ce que les calculs sont officiellement reconnus ?",
          a: "Oui. Tassi applique le barème officiel DGI : 5,5 % du CA mensuel pour l'acompte RSI, plus 10 % de ce montant pour la part CAC. Ce sont exactement les mêmes chiffres que votre Centre des Impôts vérifie.",
        },
        {
          q: "Mes données sont-elles conservées quelque part ?",
          a: "Pour le plan Gratuit, rien n'est enregistré. Chaque calcul est traité et oublié. Pour Tassi Plus, votre historique est conservé pour vous permettre de le consulter. Vous pouvez demander la suppression à tout moment en envoyant SUPPRIMER dans le chat.",
        },
        {
          q: "J'ai déjà un comptable. Pourquoi utiliser Tassi ?",
          a: "Tassi ne remplace pas un comptable. Il répond à un besoin différent : savoir en 3 secondes combien vous devez ce mois-ci, sans attendre un appel ni payer 2 000 frs pour un chiffre que vous pouvez calculer vous-même.",
        },
        {
          q: "Tassi est-il disponible la nuit ou le weekend ?",
          a: "Oui. Tassi fonctionne sur WhatsApp, qui ne ferme jamais. Un dimanche à 3h du matin ou un jour férié, la réponse arrive en moins de 3 secondes.",
        },
        {
          q: "Mon chiffre d'affaires change chaque mois. Est-ce un problème ?",
          a: "Non. Envoyez simplement le montant du mois en cours. Tassi recalcule à chaque fois sans historique ni configuration préalable.",
        },
      ],
      ctaLabel: "Posez votre question à Tassi",
      ctaSub: "Sans inscription. Directement sur WhatsApp.",
    },
    ctaBanner: {
      deadline: "Les déclarations RSI sont dues avant le 15 de chaque mois",
      h2a: "Le 15 ne vous attend pas.",
      h2b: "Tassi, lui, est prêt.",
      sub: "Rose avait eu deux amendes de retard. Depuis Tassi Plus — plus une seule.",
      social: "commerçants RSI en règle grâce à Tassi",
      cta: "Démarrer sur WhatsApp maintenant",
      sub2: "Gratuit. Sans inscription. Fonctionne sur WhatsApp.",
    },
    footer: {
      tagline: "Plus jamais de doute sur votre montant RSI avant le 15.",
      product: "Produit",
      support: "Support",
      legal: "Légal",
      links: {
        features: "Fonctionnalités",
        howItWorks: "Comment ça marche",
        pricing: "Tarifs",
        chat: "Discuter avec Tassi",
        aboutRsi: "Le RSI au Cameroun",
        openWa: "Ouvrir WhatsApp",
        privacy: "Politique de confidentialité",
        terms: "Conditions d'utilisation",
        dgi: "Barème DGI 2024",
      },
      copy: "© 2026 Tassi. Tous droits réservés.",
      ratesNote: "Barème RSI selon le code DGI 2024",
    },
    founderNote: {
      sectionLabel: "De la fondatrice",
      h2: "Pourquoi j'ai créé Tassi",
      quote: "J'ai regardé mon oncle perdre de l'argent chaque mois — pas parce qu'il gérait mal son commerce, mais parce qu'il n'arrivait pas à suivre ses obligations fiscales. Date manquée. Montant mal calculé. Amende. J'ai interrogé des dizaines de commerçants RSI au Cameroun. Le même problème, partout. J'ai créé Tassi pour qu'ils aient enfin un outil aussi simple que WhatsApp.",
      name: "Eileen Leila",
      role: "Fondatrice & CEO, Tassi",
    },
  },
  en: {
    nav: {
      features: "Features",
      howItWorks: "How it works",
      pricing: "Pricing",
      cta: "Try for free",
      tagline: "Simplify Your Monthly Tax",
    },
    hero: {
      badge: "For businesses under Cameroon's Simplified Tax Regime (RSI)",
      h1a: "The 15th is coming.",
      h1b: "Tassi has your RSI ready.",
      sub: "Send your monthly revenue on WhatsApp — get your RSI (5.5%), CAC, and total DGI due in seconds. Free.",
      primaryCta: "Chat with Tassi",
      secondaryCta: "See how it works",
      trust: ["No account needed", "No app to install", "Available 24/7", "French, English, Pidgin"],
      socialProof: "473 Cameroonian businesses file with Tassi this month",
    },
    stats: [
      { value: "< 3s", label: "Response time" },
      { value: "3", label: "Supported languages", pills: ["FR", "EN", "Pidgin"] as const },
      { value: "100 %", label: "Exact DGI rates" },
      { value: "473", label: "declarations this month" },
    ],
    features: {
      sectionLabel: "What Tassi does",
      h2a: "Everything you need to",
      h2b: "file every month",
      sub: "From the basic calculation to 12 months of history, here is what Tassi does for RSI businesses in Cameroon.",
      freeSectionLabel: "Free — always",
      plusSectionLabel: "Tassi Plus only",
      items: [
        {
          tag: "Free",
          title: "RSI calculated in 3 seconds",
          description:
            "Send your revenue — get your RSI acompte, CAC share, and total DGI due in under 3 seconds.",
        },
        {
          tag: "Free",
          title: "Zero-return filing",
          description:
            "No revenue this month? Tassi tells you exactly what to file at the Centre des Impôts.",
        },
        {
          tag: "Free",
          title: "Open whenever you need it",
          description:
            "3am before the 15th. A Sunday. Tassi responds.",
        },
        {
          tag: "Free",
          title: "French, English, or Pidgin",
          description:
            "Start in French, switch to Pidgin mid-conversation — Tassi keeps up.",
        },
        {
          tag: "Plus",
          title: "12 months of history",
          description:
            "Every calculation saved — in January, your whole year is one message away. 500 XAF/month via MoMo or Orange Money.",
        },
        {
          tag: "Plus",
          title: "Reminders before the 15th",
          description:
            "A message before the 15th every month. No more late-filing fines.",
        },
        {
          tag: "Plus",
          title: "Declaration History",
          description:
            "All your declarations from the last 12 months, right inside WhatsApp.",
        },
        {
          tag: "Plus",
          title: "Automatic Reminders",
          description:
            "Reminders on the 1st and 12th — never miss the 15th again.",
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
      h2a: "Results confirmed",
      h2b: "by their Centre des Impôts.",
      aggregateLabel: "Average rating",
      aggregateCount: "from 473 active users",
      items: [
        {
          quote:
            "I used to call my accountant every month for the amount. 2,000 frs per call, plus his fees. Now I send a message. Free.",
          name: "Aïssatou N.",
          role: "Boutique owner, Yaoundé",
          avatar: "A",
          color: "from-forest-600 to-forest-700",
          stars: 5,
        },
        {
          quote:
            "I have a hardware shop in Douala. The RSI form never made sense to me. The Pidgin version of Tassi does. I checked the result at the Centre des Impôts — it was correct.",
          name: "Emmanuel T.",
          role: "Hardware shop, Douala",
          avatar: "E",
          color: "from-gold-600 to-gold-700",
          stars: 4,
        },
        {
          quote:
            "The 12-month history is what got me on Plus. In January I can see the whole year at once. 500 XAF a month for that is nothing.",
          name: "Carine M.",
          role: "Salon owner, Bafoussam",
          avatar: "C",
          color: "from-blue-600 to-indigo-700",
          stars: 5,
        },
        {
          quote:
            "I was sceptical. Tried it once — the result matched exactly what the Centre des Impôts confirmed. No more driving in just to find out the amount.",
          name: "Fatima O.",
          role: "Grocery shop, Ngaoundéré",
          avatar: "F",
          color: "from-teal-600 to-cyan-700",
          stars: 5,
        },
        {
          quote:
            "I run a taxi park. I was worried the figures would be rough estimates. They are exact. And in Pidgin too — my partners can use it without me.",
          name: "Marcel N.",
          role: "Transport, Douala",
          avatar: "M",
          color: "from-purple-600 to-violet-700",
          stars: 5,
        },
        {
          quote:
            "The reminder before the 15th is what I love most. Before Tassi I got two late-filing fines. Since switching to Plus, not a single one.",
          name: "Rose K.",
          role: "Restaurant, Yaoundé",
          avatar: "R",
          color: "from-orange-500 to-red-600",
          stars: 5,
        },
      ],
    },
    pricing: {
      sectionLabel: "Pricing",
      h2a: "Free to start.",
      h2b: "Plus for history.",
      sub: "The core calculation is free for all RSI businesses. History and reminders are in the Plus plan.",
      freeName: "Free",
      freeSub: "Always free. No credit card.",
      freeCta: "Start on WhatsApp",
      freeTier: [
        { label: "RSI acompte calculation", included: true },
        { label: "CAC share breakdown", included: true },
        { label: "Déclaration Néant guidance", included: true },
        { label: "French, English & Pidgin", included: true },
        { label: "No app download required", included: true },
      ],
      upgradeHint: "12-month history + reminders before the 15th → Tassi Plus",
      plusName: "Tassi Plus",
      plusPrice: "500 XAF",
      plusSub: "per month via MTN MoMo or Orange Money",
      plusCta: "Activate Tassi Plus",
      plusTier: [
        "RSI acompte calculation",
        "CAC share breakdown",
        "Déclaration Néant guidance",
        "French, English & Pidgin",
        "No app download required",
        "12-month calculation history",
        "Monthly reminders before the 15th",
      ],
      popularBadge: "Most popular",
      finePrint: "Tassi Plus renews monthly. To cancel, send",
      cancelWord: "CANCEL",
      finePrint2: "in the chat.",
    },
    faq: {
      sectionLabel: "Common questions",
      h2: "Everything you need to know before you start",
      items: [
        {
          q: "Is it really free?",
          a: "Yes. The basic plan is free with no time limit — no credit card, no account. Send your revenue, get your RSI, CAC, and total DGI figures. Done. Tassi Plus (500 XAF/month) unlocks declaration history and automatic reminders.",
        },
        {
          q: "Are the calculations officially recognised?",
          a: "Yes. Tassi applies the official DGI rates: 5.5% of monthly revenue for the RSI acompte, plus 10% of that for the CAC share — the exact figures your Centre des Impôts checks.",
        },
        {
          q: "Is my data stored anywhere?",
          a: "On the Free plan, nothing is saved. Each calculation is processed and discarded. On Tassi Plus, your history is kept so you can retrieve it. You can request deletion at any time by sending DELETE in the chat.",
        },
        {
          q: "I already have an accountant. Why use Tassi?",
          a: "Tassi is not a replacement for an accountant. It answers a different need: knowing in 3 seconds how much you owe this month, without waiting for a call or paying 2,000 XAF for a number you can calculate yourself.",
        },
        {
          q: "Is Tassi available at night or on weekends?",
          a: "Yes. Tassi runs on WhatsApp, which never closes. A Sunday at 3am or a public holiday — the answer comes back in under 3 seconds.",
        },
        {
          q: "My revenue changes every month. Does that matter?",
          a: "Not at all. Just send this month's figure. Tassi recalculates from scratch every time — no history or setup needed.",
        },
      ],
      ctaLabel: "Ask Tassi your question",
      ctaSub: "No account needed. Just WhatsApp.",
    },
    ctaBanner: {
      deadline: "RSI declarations are due by the 15th of each month",
      h2a: "The 15th won't wait.",
      h2b: "Tassi already has your answer.",
      sub: "Rose had two late-filing fines before Tassi Plus. Not one since.",
      social: "RSI business owners filing on time with Tassi",
      cta: "Start on WhatsApp now",
      sub2: "Free. No sign-up. Works on WhatsApp.",
    },
    footer: {
      tagline: "Never wonder if you got the number right again.",
      product: "Product",
      support: "Support",
      legal: "Legal",
      links: {
        features: "Features",
        howItWorks: "How it works",
        pricing: "Pricing",
        chat: "Chat with Tassi",
        aboutRsi: "RSI in Cameroon",
        openWa: "Open WhatsApp",
        privacy: "Privacy policy",
        terms: "Terms of use",
        dgi: "DGI 2024 RSI schedule",
      },
      copy: "© 2026 Tassi. All rights reserved.",
      ratesNote: "RSI rates from DGI 2024 schedule",
    },
    founderNote: {
      sectionLabel: "From the founder",
      h2: "Why I built Tassi",
      quote: "I watched my uncle lose money every month — not because he mismanaged his shop, but because he couldn't keep up with his tax filings. Missed deadline. Wrong amount. Fine. I interviewed dozens of RSI business owners across Cameroon. The same problem, everywhere. I built Tassi so they'd finally have a tool as simple as WhatsApp.",
      name: "Eileen Leila",
      role: "Founder & CEO, Tassi",
    },
  },
} as const;

export type Copy = (typeof copy)[Lang];

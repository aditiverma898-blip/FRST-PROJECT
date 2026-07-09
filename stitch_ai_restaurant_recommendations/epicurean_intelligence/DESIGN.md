---
name: Epicurean Intelligence
colors:
  surface: '#fcf9f8'
  surface-dim: '#dcd9d9'
  surface-bright: '#fcf9f8'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f6f3f2'
  surface-container: '#f0eded'
  surface-container-high: '#eae7e7'
  surface-container-highest: '#e5e2e1'
  on-surface: '#1b1b1b'
  on-surface-variant: '#5b403f'
  inverse-surface: '#313030'
  inverse-on-surface: '#f3f0ef'
  outline: '#8f6f6e'
  outline-variant: '#e4bebc'
  surface-tint: '#bb162c'
  primary: '#b7122a'
  on-primary: '#ffffff'
  primary-container: '#db313f'
  on-primary-container: '#fffbff'
  inverse-primary: '#ffb3b1'
  secondary: '#705d00'
  on-secondary: '#ffffff'
  secondary-container: '#fcd400'
  on-secondary-container: '#6e5c00'
  tertiary: '#006762'
  on-tertiary: '#ffffff'
  tertiary-container: '#00837c'
  on-tertiary-container: '#f3fffd'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdad8'
  primary-fixed-dim: '#ffb3b1'
  on-primary-fixed: '#410007'
  on-primary-fixed-variant: '#92001c'
  secondary-fixed: '#ffe16d'
  secondary-fixed-dim: '#e9c400'
  on-secondary-fixed: '#221b00'
  on-secondary-fixed-variant: '#544600'
  tertiary-fixed: '#8ef4eb'
  tertiary-fixed-dim: '#71d7cf'
  on-tertiary-fixed: '#00201e'
  on-tertiary-fixed-variant: '#00504c'
  background: '#fcf9f8'
  on-background: '#1b1b1b'
  surface-variant: '#e5e2e1'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  container-max: 1280px
  edge-margin: 32px
  edge-margin-mobile: 20px
  gutter: 24px
  stack-lg: 32px
  stack-md: 16px
  stack-sm: 8px
---

## Brand & Style

This design system establishes a premium, AI-driven restaurant discovery experience that balances technological sophistication with the visceral warmth of culinary exploration. The brand personality is **helpful, professional, and food-focused**, acting as a discerning digital concierge for the modern epicurean.

The visual style is **Corporate / Modern** with a refined, high-end finish. It utilizes generous whitespace to create an "airy" and professional atmosphere, ensuring that high-quality food photography remains the focal point. Subtle transitions and polished micro-interactions convey the intelligence of the underlying AI, while the warm color palette keeps the experience inviting and appetizing.

## Colors

The palette is anchored by a vibrant, warm red that stimulates appetite and signals the brand's heritage. This is balanced against a pristine white background and functional light gray panels to maintain a clean, organized structure.

- **Primary (#E23744):** Used for key actions, brand touchpoints, and active states.
- **Surface:** Pure white (#FFFFFF) for the main canvas, with light gray (#F8F8F8) used for secondary panels, grouping elements, and background depth.
- **Typography (#1C1C1C):** High-contrast dark charcoal ensures WCAG AA readability against all surface levels.
- **Rank Accents:** Specific metallic tones are reserved for discovery ranking (#1 Gold, #2 Silver, #3 Bronze) to denote prestige and exclusivity.

## Typography

The typography system utilizes **Inter** for its exceptional legibility and systematic, modern feel. The hierarchy is strictly enforced to guide users through complex restaurant data without cognitive overload.

Headlines use tighter letter spacing and heavier weights to create a sense of authority. Body text is optimized for long-form descriptions and menu items with a generous line height. For mobile, headline sizes are scaled down to ensure word-wrap integrity on smaller viewports while maintaining their visual weight.

## Layout & Spacing

This design system employs a **Fixed Grid** philosophy on desktop and a **Fluid Grid** on mobile. The layout is intentionally "airy" to allow the food content to breathe.

- **Desktop:** 12-column grid with a 1280px max-width, 24px gutters, and 32px outer margins.
- **Tablet:** 8-column grid with 24px gutters and 24px outer margins.
- **Mobile:** 4-column fluid grid with 16px gutters and 20px outer margins.

Spacing follows a consistent 8px scale. A 32px vertical rhythm (stack-lg) is used between major sections to maintain a professional, premium feel. 24px is the standard padding for card containers and content groupings.

## Elevation & Depth

Visual hierarchy is established through **Tonal Layers** supplemented by **Ambient Shadows**.

1.  **Level 0 (Background):** Pure #FFFFFF.
2.  **Level 1 (Panels):** #F8F8F8 with a subtle 1px inner border (#EDEDED) to define boundaries without adding visual weight.
3.  **Level 2 (Cards/Floating Elements):** White surfaces with a soft, multi-layered shadow (0px 4px 20px rgba(0,0,0,0.05)).
4.  **Interaction State:** On hover, Level 2 elements should "lift" using a more pronounced shadow (0px 12px 30px rgba(0,0,0,0.08)) and a slight -4px Y-axis translation.

Shadows must never be harsh; they should appear as soft ambient light to maintain the clean, professional aesthetic.

## Shapes

The shape language is consistently **Rounded**, reflecting a friendly and modern personality. 

- **Standard Elements (Buttons, Inputs, Small Cards):** 0.5rem (8px) corner radius.
- **Large Containers (Major Result Cards, Modals):** 1rem (16px) corner radius.
- **Interactive Accents (Filter Chips, Search Bars):** Pill-shaped (Full radius) to distinguish them from structural content.

This curvature softens the data-heavy nature of the platform, making the AI recommendations feel more approachable.

## Components

### Buttons & Chips
- **Primary Button:** Solid #E23744 with white text. 8px radius. High-affordance.
- **Filter Chips:** Light gray background (#F8F8F8) with 1px border. On selection, background becomes #1C1C1C with white text. Pill-shaped.

### Cards
Restaurant cards are the core component. They feature high-quality imagery at the top, a 16px radius, and 24px internal padding. Rank badges are positioned in the top-left corner using a circular "coin" style with metallic gradients for Gold, Silver, and Bronze.

### Form Controls
- **Inputs & Dropdowns:** 8px radius, #F8F8F8 background, and a subtle 1px border. Focus states use a 2px #E23744 stroke.
- **Sliders:** Minimalist tracks in light gray with a primary red thumb for range selection (e.g., price or distance).

### Rank Badges
Rankings use a sophisticated metallic palette.
- **Gold (#1):** White text on #D4AF37 background.
- **Silver (#2):** Dark text on #C0C0C0 background.
- **Bronze (#3):** White text on #CD7F32 background.

### AI Insight Panel
A specialized component for "AI Recommendations." Uses a very subtle gradient background (Primary Red at 5% opacity to transparent) with a unique icon to signify AI-generated content.
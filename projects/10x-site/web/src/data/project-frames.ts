/* Real 10x Visuals project photography, hosted on the live WordPress media
   library (see wiki/projects/10x-website.md) rather than shipped under
   assets/ — same captions and client attribution already shipped on
   index.html. A REA/Construction split was tried here and reverted at
   Hunter's request: splitting only 5 and 3 photos across two categories
   left each carousel with too few, too-wide cards, which bled ugly
   rotated-edge slivers into view at the screen sides. One combined set of
   all eight avoids that and is simply what he wants here — categorisation
   lives in the client roster section instead. */

const MEDIA_BASE = "https://10xvisuals.com.au/wp-content/uploads/2026/08/"

export type Frame = { src: string; alt: string }

export const ALL_FRAMES: Frame[] = [
  { src: `${MEDIA_BASE}hero-stonehaven-1400.jpg`, alt: "Stonehaven at 47 Somerset Drive, photographed from the air in late afternoon light." },
  { src: `${MEDIA_BASE}work-stonehaven-1400.jpg`, alt: "Stonehaven, the front elevation at 47 Somerset Drive, symmetrical under a clear sky." },
  { src: `${MEDIA_BASE}work-salisbury-1400.jpg`, alt: "Kennedys Lane, a completed build delivered by Salisbury Building Projects, seen from above." },
  { src: `${MEDIA_BASE}work-davenport-1400.jpg`, alt: "Davenport, a refined hillside residence marketed by PRD Burleigh, looking out over the pool." },
  { src: `${MEDIA_BASE}work-elysium-1400.jpg`, alt: "Elysium, a completed large scale apartment development delivered by Shape Construction." },
  { src: `${MEDIA_BASE}work-sol-1400.jpg`, alt: "SOL by Skye Development Group, the completed canal side compound lit at night." },
  { src: `${MEDIA_BASE}work-broncos-1400.jpg`, alt: "The refurbished Broncos Leagues Club interior, delivered by Ashley Cooper Construction." },
  { src: `${MEDIA_BASE}hero-branding-1400.jpg`, alt: "A refined living space at Stonehaven, photographed for Whitefox." },
]

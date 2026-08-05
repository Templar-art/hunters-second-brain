import { useRef, useState } from "react"
import {
  AnimatePresence,
  motion,
  useReducedMotion,
  useScroll,
  useTransform,
} from "framer-motion"
import type { ShowcaseProperty } from "@/data/showcase-properties"

/* 10x Visuals portfolio demo: Framer Motion techniques in one
   self-contained widget, over real Bespoke Estate Agents listings.
   1. Shared-element (layoutId) morph from grid card -> detail hero.
   2. AnimatePresence enter/exit between grid and detail.
   3. Spring-staggered gallery reveal inside the detail view.
   4. Scroll-scrubbed video (northview only) tied to scroll position.
   No router — "detail view" is local state, matching this app's existing
   no-Node-server, static-HTML-plus-React-island architecture.
   (Cards were originally a magnetic cursor-tilt hover — dropped per
   feedback; a plain scale-up hover reads cleaner and the click-to-expand
   morph is the part worth keeping.) */

function PropertyCard({
  property,
  onOpen,
}: {
  property: ShowcaseProperty
  onOpen: () => void
}) {
  return (
    <motion.button
      type="button"
      onClick={onOpen}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.99 }}
      transition={{ type: "spring", stiffness: 300, damping: 25 }}
      className="tdx:group tdx:relative tdx:block tdx:w-full tdx:text-left tdx:cursor-pointer tdx:outline-none tdx:focus-visible:ring-2 tdx:focus-visible:ring-white/70 tdx:rounded-2xl"
    >
      <div className="tdx:relative tdx:aspect-[4/5] tdx:overflow-hidden tdx:rounded-2xl tdx:bg-night">
        <motion.img
          layoutId={`cover-${property.id}`}
          src={property.cover}
          alt={property.name}
          className="tdx:h-full tdx:w-full tdx:object-cover tdx:transition-transform tdx:duration-500 tdx:group-hover:scale-105"
        />
        <div className="tdx:absolute tdx:inset-0 tdx:bg-gradient-to-t tdx:from-black/70 tdx:via-black/10 tdx:to-transparent" />
        <span className="tdx:absolute tdx:top-4 tdx:left-4 tdx:rounded tdx:bg-white/92 tdx:px-3 tdx:py-1.5 tdx:text-[0.64rem] tdx:font-semibold tdx:uppercase tdx:tracking-[0.14em] tdx:text-night">
          {property.status}
        </span>
        <div className="tdx:absolute tdx:bottom-0 tdx:left-0 tdx:right-0 tdx:p-5">
          <motion.h3
            layoutId={`title-${property.id}`}
            className="tdx:font-serif tdx:text-2xl tdx:font-light tdx:text-ivory"
          >
            {property.name}
          </motion.h3>
          <p className="tdx:mt-1 tdx:text-[0.7rem] tdx:uppercase tdx:tracking-[0.2em] tdx:text-ivory/60">
            {property.location}
          </p>
        </div>
      </div>
    </motion.button>
  )
}

function ScrollFilm({ src }: { src: string }) {
  const reduceMotion = useReducedMotion()
  const containerRef = useRef<HTMLDivElement>(null)
  const videoRef = useRef<HTMLVideoElement>(null)
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start end", "end start"],
  })

  useTransform(scrollYProgress, (p) => {
    const v = videoRef.current
    if (!v || reduceMotion || !Number.isFinite(v.duration)) return
    v.currentTime = Math.min(Math.max(p, 0), 1) * v.duration
  })

  return (
    <div ref={containerRef} className="tdx:relative tdx:h-[220vh]">
      <div className="tdx:sticky tdx:top-0 tdx:h-screen tdx:overflow-hidden tdx:rounded-2xl">
        <video
          ref={videoRef}
          src={src}
          muted
          playsInline
          preload="auto"
          autoPlay={reduceMotion ? true : false}
          loop={reduceMotion ? true : false}
          className="tdx:h-full tdx:w-full tdx:object-cover"
        />
        <div className="tdx:absolute tdx:inset-x-0 tdx:bottom-0 tdx:bg-gradient-to-t tdx:from-black/60 tdx:to-transparent tdx:p-6">
          <p className="tdx:text-[0.68rem] tdx:uppercase tdx:tracking-[0.22em] tdx:text-ivory/70">
            Scroll to walk through
          </p>
        </div>
      </div>
    </div>
  )
}

function SpringGallery({ photos, alt }: { photos: string[]; alt: string }) {
  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={{ visible: { transition: { staggerChildren: 0.09 } } }}
      className="tdx:grid tdx:grid-cols-2 tdx:sm:grid-cols-3 tdx:gap-3"
    >
      {photos.map((src, i) => (
        <motion.img
          key={src}
          src={src}
          alt={`${alt} photo ${i + 1}`}
          variants={{
            hidden: { opacity: 0, y: 28, scale: 0.96 },
            visible: {
              opacity: 1,
              y: 0,
              scale: 1,
              transition: { type: "spring", stiffness: 260, damping: 24 },
            },
          }}
          className="tdx:aspect-[4/3] tdx:w-full tdx:rounded-xl tdx:object-cover"
        />
      ))}
    </motion.div>
  )
}

function PropertyDetail({
  property,
  onClose,
}: {
  property: ShowcaseProperty
  onClose: () => void
}) {
  return (
    <motion.div
      role="dialog"
      aria-modal="true"
      aria-label={property.name}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="tdx:fixed tdx:inset-0 tdx:z-[80] tdx:overflow-y-auto tdx:bg-night"
    >
      <button
        type="button"
        onClick={onClose}
        aria-label="Close"
        className="tdx:fixed tdx:top-5 tdx:right-5 tdx:z-10 tdx:flex tdx:h-11 tdx:w-11 tdx:items-center tdx:justify-center tdx:rounded-full tdx:bg-white/10 tdx:text-2xl tdx:leading-none tdx:text-ivory tdx:outline-none tdx:focus-visible:ring-2 tdx:focus-visible:ring-white/70"
      >
        &times;
      </button>

      <div className="tdx:relative tdx:h-[70vh] tdx:w-full tdx:overflow-hidden">
        <motion.img
          layoutId={`cover-${property.id}`}
          src={property.cover}
          alt={property.name}
          className="tdx:h-full tdx:w-full tdx:object-cover"
        />
        <div className="tdx:absolute tdx:inset-0 tdx:bg-gradient-to-t tdx:from-night tdx:via-black/10 tdx:to-transparent" />
        <div className="tdx:absolute tdx:bottom-0 tdx:left-0 tdx:right-0 tdx:p-8 tdx:sm:p-12">
          <span className="tdx:rounded tdx:bg-white/92 tdx:px-3 tdx:py-1.5 tdx:text-[0.64rem] tdx:font-semibold tdx:uppercase tdx:tracking-[0.14em] tdx:text-night">
            {property.status}
          </span>
          <motion.h2
            layoutId={`title-${property.id}`}
            className="tdx:mt-4 tdx:font-serif tdx:text-4xl tdx:sm:text-6xl tdx:font-light tdx:text-ivory"
          >
            {property.name}
          </motion.h2>
        </div>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.25, duration: 0.5 }}
        className="tdx:mx-auto tdx:max-w-4xl tdx:px-6 tdx:py-12 tdx:sm:px-8"
      >
        <p className="tdx:max-w-[62ch] tdx:text-ivory/80">{property.blurb}</p>
        <div className="tdx:mt-8 tdx:flex tdx:gap-8">
          {property.stats.map((s) => (
            <div key={s.label}>
              <div className="tdx:font-serif tdx:text-3xl tdx:font-light tdx:text-ivory">
                {s.value}
              </div>
              <div className="tdx:mt-1 tdx:text-[0.64rem] tdx:uppercase tdx:tracking-[0.16em] tdx:text-ivory/50">
                {s.label}
              </div>
            </div>
          ))}
        </div>

        {property.film && (
          <div className="tdx:mt-14">
            <ScrollFilm src={property.film} />
          </div>
        )}

        <div className="tdx:mt-14">
          <SpringGallery photos={property.gallery} alt={property.name} />
        </div>
      </motion.div>
    </motion.div>
  )
}

export default function PropertyShowcase({
  properties,
}: {
  properties: ShowcaseProperty[]
}) {
  const [activeId, setActiveId] = useState<string | null>(null)
  const active = properties.find((p) => p.id === activeId) ?? null

  return (
    <div className="tdx:relative">
      <div className="tdx:grid tdx:gap-6 tdx:sm:grid-cols-3">
        {properties.map((property) => (
          <PropertyCard
            key={property.id}
            property={property}
            onOpen={() => setActiveId(property.id)}
          />
        ))}
      </div>

      <AnimatePresence>
        {active && (
          <PropertyDetail property={active} onClose={() => setActiveId(null)} />
        )}
      </AnimatePresence>
    </div>
  )
}

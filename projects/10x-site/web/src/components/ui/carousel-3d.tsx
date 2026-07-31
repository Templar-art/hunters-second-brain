"use client"

/* Filed as carousel-3d.tsx, not the pasted registry's 3d-carousel.tsx:
   Tailwind v4's content scanner silently skips filenames that start
   with a digit, so nothing in this file was being picked up at all
   under the original name — confirmed by bisecting against a sibling
   test file that scanned fine. Renamed rather than worked around. */

import { memo, useEffect, useLayoutEffect, useMemo, useState } from "react"
import {
  AnimatePresence,
  motion,
  useAnimation,
  useMotionValue,
  useTransform,
} from "framer-motion"

export const useIsomorphicLayoutEffect =
  typeof window !== "undefined" ? useLayoutEffect : useEffect

type UseMediaQueryOptions = {
  defaultValue?: boolean
  initializeWithValue?: boolean
}

const IS_SERVER = typeof window === "undefined"

export function useMediaQuery(
  query: string,
  {
    defaultValue = false,
    initializeWithValue = true,
  }: UseMediaQueryOptions = {}
): boolean {
  const getMatches = (query: string): boolean => {
    if (IS_SERVER) {
      return defaultValue
    }
    return window.matchMedia(query).matches
  }

  const [matches, setMatches] = useState<boolean>(() => {
    if (initializeWithValue) {
      return getMatches(query)
    }
    return defaultValue
  })

  const handleChange = () => {
    setMatches(getMatches(query))
  }

  useIsomorphicLayoutEffect(() => {
    const matchMedia = window.matchMedia(query)
    handleChange()

    matchMedia.addEventListener("change", handleChange)

    return () => {
      matchMedia.removeEventListener("change", handleChange)
    }
  }, [query])

  return matches
}

/* Real 10x Visuals project photography, reused from assets/ rather than
   stock imagery — same captions already shipped on the pages that use
   these frames (index.html, branding.html, content-creation.html). */
const projectFrames = [
  { src: "assets/hero-stonehaven-1400.jpg", alt: "Stonehaven at 47 Somerset Drive, photographed from the air in late afternoon light." },
  { src: "assets/work-stonehaven-1400.jpg", alt: "Stonehaven, the front elevation at 47 Somerset Drive, symmetrical under a clear sky." },
  { src: "assets/work-bespoke-1400.jpg", alt: "A prestige Gold Coast listing photographed for Bespoke Estate Agents." },
  { src: "assets/work-davenport-1400.jpg", alt: "Davenport, a refined hillside residence marketed by PRD Burleigh, looking out over the pool." },
  { src: "assets/work-elysium-1400.jpg", alt: "Elysium, a completed large scale apartment development delivered by Shape Construction." },
  { src: "assets/work-sol-1400.jpg", alt: "SOL by Skye Development Group, the completed canal side compound lit at night." },
  { src: "assets/work-broncos-1400.jpg", alt: "The refurbished Broncos Leagues Club interior, delivered by Ashley Cooper Construction." },
  { src: "assets/hero-branding-1400.jpg", alt: "A refined living space at Stonehaven, photographed for Whitefox." },
]

const duration = 0.15
const transition = { duration, ease: [0.32, 0.72, 0, 1] as const, filter: "blur(4px)" }
const transitionOverlay = { duration: 0.5, ease: [0.32, 0.72, 0, 1] as const }

const Carousel = memo(
  ({
    handleClick,
    controls,
    cards,
    isCarouselActive,
  }: {
    handleClick: (imgUrl: string, index: number) => void
    controls: any
    cards: { src: string; alt: string }[]
    isCarouselActive: boolean
  }) => {
    const isScreenSizeSm = useMediaQuery("(max-width: 640px)")
    const cylinderWidth = isScreenSizeSm ? 1100 : 1800
    const faceCount = cards.length
    const faceWidth = cylinderWidth / faceCount
    const radius = cylinderWidth / (2 * Math.PI)
    const rotation = useMotionValue(0)
    const transform = useTransform(
      rotation,
      (value) => `rotate3d(0, 1, 0, ${value}deg)`
    )

    return (
      <div
        className="tdx:flex tdx:h-full tdx:items-center tdx:justify-center tdx:bg-night"
        style={{
          perspective: "1000px",
          transformStyle: "preserve-3d",
          willChange: "transform",
        }}
      >
        <motion.div
          drag={isCarouselActive ? "x" : false}
          className="tdx:relative tdx:flex tdx:h-full tdx:origin-center tdx:cursor-grab tdx:justify-center tdx:active:cursor-grabbing"
          style={{
            transform,
            rotateY: rotation,
            width: cylinderWidth,
            transformStyle: "preserve-3d",
          }}
          onDrag={(_, info) =>
            isCarouselActive &&
            rotation.set(rotation.get() + info.offset.x * 0.05)
          }
          onDragEnd={(_, info) =>
            isCarouselActive &&
            controls.start({
              rotateY: rotation.get() + info.velocity.x * 0.05,
              transition: {
                type: "spring",
                stiffness: 100,
                damping: 30,
                mass: 0.1,
              },
            })
          }
          animate={controls}
        >
          {cards.map((card, i) => (
            <motion.div
              key={`key-${card.src}-${i}`}
              className="tdx:absolute tdx:flex tdx:h-full tdx:origin-center tdx:items-center tdx:justify-center tdx:rounded-xl tdx:bg-night tdx:p-2"
              style={{
                width: `${faceWidth}px`,
                transform: `rotateY(${
                  i * (360 / faceCount)
                }deg) translateZ(${radius}px)`,
              }}
              onClick={() => handleClick(card.src, i)}
            >
              <motion.img
                src={card.src}
                alt={card.alt}
                layoutId={`img-${card.src}`}
                className="tdx:pointer-events-none tdx:w-full tdx:rounded-xl tdx:object-cover tdx:aspect-square"
                initial={{ filter: "blur(4px)" }}
                layout="position"
                animate={{ filter: "blur(0px)" }}
                transition={transition}
              />
            </motion.div>
          ))}
        </motion.div>
      </div>
    )
  }
)

function ThreeDPhotoCarousel() {
  const [activeImg, setActiveImg] = useState<string | null>(null)
  const [isCarouselActive, setIsCarouselActive] = useState(true)
  const controls = useAnimation()
  const cards = useMemo(() => projectFrames, [])

  const handleClick = (imgUrl: string) => {
    setActiveImg(imgUrl)
    setIsCarouselActive(false)
    controls.stop()
  }

  const handleClose = () => {
    setActiveImg(null)
    setIsCarouselActive(true)
  }

  return (
    <motion.div layout className="tdx:relative">
      <AnimatePresence mode="sync">
        {activeImg && (
          <motion.div
            initial={{ opacity: 0, scale: 0 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0 }}
            layoutId={`img-container-${activeImg}`}
            layout="position"
            onClick={handleClose}
            className="tdx:fixed tdx:inset-0 tdx:bg-black tdx:bg-opacity-10 tdx:flex tdx:items-center tdx:justify-center tdx:z-50 tdx:m-5 tdx:md:m-36 tdx:lg:mx-[19rem] tdx:rounded-3xl"
            style={{ willChange: "opacity" }}
            transition={transitionOverlay}
          >
            <motion.img
              layoutId={`img-${activeImg}`}
              src={activeImg}
              className="tdx:max-w-full tdx:max-h-full tdx:rounded-lg tdx:shadow-lg"
              initial={{ scale: 0.5 }}
              animate={{ scale: 1 }}
              transition={{
                delay: 0.5,
                duration: 0.5,
                ease: [0.25, 0.1, 0.25, 1],
              }}
              style={{
                willChange: "transform",
              }}
            />
          </motion.div>
        )}
      </AnimatePresence>
      <div className="tdx:relative tdx:h-[500px] tdx:w-full tdx:overflow-hidden">
        <Carousel
          handleClick={handleClick}
          controls={controls}
          cards={cards}
          isCarouselActive={isCarouselActive}
        />
      </div>
    </motion.div>
  )
}

export { ThreeDPhotoCarousel }

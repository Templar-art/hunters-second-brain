"use client"

/* Filed as carousel-3d.tsx, not the pasted registry's 3d-carousel.tsx:
   Tailwind v4's content scanner silently skips filenames that start
   with a digit, so nothing in this file was being picked up at all
   under the original name — confirmed by bisecting against a sibling
   test file that scanned fine. Renamed rather than worked around. */

import { memo, useEffect, useLayoutEffect, useRef, useState } from "react"
import {
  AnimatePresence,
  animate,
  motion,
  useAnimation,
  useMotionValue,
  useTransform,
} from "framer-motion"
import type { Frame } from "@/data/project-frames"

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

const duration = 0.15
const transition = { duration, ease: [0.32, 0.72, 0, 1] as const, filter: "blur(4px)" }
const transitionOverlay = { duration: 0.5, ease: [0.32, 0.72, 0, 1] as const }

const Carousel = memo(
  ({
    handleClick,
    controls,
    cards,
    isCarouselActive,
    rotation,
  }: {
    handleClick: (index: number, el: HTMLElement) => void
    controls: any
    cards: Frame[]
    isCarouselActive: boolean
    rotation: ReturnType<typeof useMotionValue<number>>
  }) => {
    const isScreenSizeSm = useMediaQuery("(max-width: 640px)")
    const cylinderWidth = isScreenSizeSm ? 1100 : 1800
    const faceCount = cards.length
    const faceWidth = cylinderWidth / faceCount
    const radius = cylinderWidth / (2 * Math.PI)
    const transform = useTransform(
      rotation,
      (value) => `rotate3d(0, 1, 0, ${value}deg)`
    )

    /* Arrow keys step the ring one card at a time — the drag gesture has
       no keyboard equivalent otherwise, so a keyboard user could never
       reach the cards hidden behind the front face. Drives `rotation`
       via animate() rather than controls.start({rotateY}) — verified by
       bisection that from a plain keydown handler (outside any drag
       callback) animate() reliably reaches the same MotionValue that
       `transform` above derives from. */
    const rotateByStep = (dir: 1 | -1) => {
      const step = 360 / faceCount
      animate(rotation, rotation.get() + dir * step, {
        type: "spring", stiffness: 100, damping: 30, mass: 0.1,
      })
    }

    return (
      <div
        className="tdx:flex tdx:h-full tdx:items-center tdx:justify-center tdx:bg-night"
        style={{
          perspective: "1000px",
          transformStyle: "preserve-3d",
          willChange: "transform",
        }}
        onKeyDown={(e) => {
          if (e.key === "ArrowLeft") { e.preventDefault(); rotateByStep(-1) }
          else if (e.key === "ArrowRight") { e.preventDefault(); rotateByStep(1) }
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
              /* Slowed the release momentum — 0.05 read as a hard flick
                 sending the ring spinning; 0.015 carries through gently
                 instead. */
              rotateY: rotation.get() + info.velocity.x * 0.015,
              transition: {
                type: "spring",
                stiffness: 100,
                damping: 40,
                mass: 0.1,
              },
            })
          }
          animate={controls}
        >
          {cards.map((card, i) => (
            <motion.div
              key={`key-${card.src}-${i}`}
              role="button"
              tabIndex={0}
              aria-label={`Expand: ${card.alt}`}
              className="tdx:absolute tdx:flex tdx:h-full tdx:origin-center tdx:items-center tdx:justify-center tdx:rounded-xl tdx:bg-night tdx:p-2 tdx:cursor-pointer tdx:outline-none tdx:focus-visible:ring-2 tdx:focus-visible:ring-white/70"
              style={{
                width: `${faceWidth}px`,
                transform: `rotateY(${
                  i * (360 / faceCount)
                }deg) translateZ(${radius}px)`,
              }}
              onClick={(e) => handleClick(i, e.currentTarget)}
              onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === " ") {
                  e.preventDefault()
                  handleClick(i, e.currentTarget)
                }
              }}
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

function ThreeDPhotoCarousel({ frames }: { frames: Frame[] }) {
  const [activeIndex, setActiveIndex] = useState<number | null>(null)
  const [isCarouselActive, setIsCarouselActive] = useState(true)
  const controls = useAnimation()
  const rotation = useMotionValue(0)
  const cards = frames
  const activeCard = activeIndex !== null ? cards[activeIndex] : null
  const returnFocusRef = useRef<HTMLElement | null>(null)
  const closeBtnRef = useRef<HTMLButtonElement | null>(null)

  const handleClick = (index: number, el: HTMLElement) => {
    returnFocusRef.current = el
    setActiveIndex(index)
    setIsCarouselActive(false)
    controls.stop()
  }

  const handleClose = () => {
    setActiveIndex(null)
    setIsCarouselActive(true)
    returnFocusRef.current?.focus()
  }

  /* Mirrors the site's own project lightbox (assets/prestige.js):
     focus moves into the overlay on open, Escape closes, focus returns
     to the tile that opened it. */
  useEffect(() => {
    if (activeIndex === null) return
    closeBtnRef.current?.focus()
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") { e.preventDefault(); handleClose() }
    }
    document.addEventListener("keydown", onKeyDown)
    return () => document.removeEventListener("keydown", onKeyDown)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeIndex])

  return (
    <motion.div layout className="tdx:relative">
      <AnimatePresence mode="sync">
        {activeCard && (
          <motion.div
            initial={{ opacity: 0, scale: 0 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0 }}
            layoutId={`img-container-${activeCard.src}`}
            layout="position"
            onClick={handleClose}
            role="dialog"
            aria-modal="true"
            aria-label={activeCard.alt}
            className="tdx:fixed tdx:inset-0 tdx:bg-black tdx:bg-opacity-10 tdx:flex tdx:items-center tdx:justify-center tdx:z-50 tdx:m-5 tdx:md:m-36 tdx:lg:mx-[19rem] tdx:rounded-3xl"
            style={{ willChange: "opacity" }}
            transition={transitionOverlay}
          >
            <button
              ref={closeBtnRef}
              type="button"
              aria-label="Close"
              onClick={(e) => { e.stopPropagation(); handleClose() }}
              className="tdx:absolute tdx:top-4 tdx:right-4 tdx:z-10 tdx:text-white tdx:text-2xl tdx:leading-none tdx:w-10 tdx:h-10 tdx:flex tdx:items-center tdx:justify-center tdx:rounded-full tdx:bg-black/30 tdx:outline-none tdx:focus-visible:ring-2 tdx:focus-visible:ring-white/70"
            >
              &times;
            </button>
            <motion.img
              layoutId={`img-${activeCard.src}`}
              src={activeCard.src}
              alt={activeCard.alt}
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
          rotation={rotation}
        />
      </div>
    </motion.div>
  )
}

export { ThreeDPhotoCarousel }
